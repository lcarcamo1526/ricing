-- Grammar correction via the same script the Hyprland keybinds use.
-- Works on the visual selection, or the whole buffer in normal mode.
--   <Leader>gg  fix grammar (LLM, en/es/fr, C1 register)
--   <Leader>gl  fix typos only (offline LanguageTool)

local function run(cmd, lines)
  local input = table.concat(lines, "\n")
  local out = vim.system(cmd, { stdin = input, text = true }):wait()
  if out.code ~= 0 then
    vim.notify("grammar: " .. (out.stderr or "failed"), vim.log.levels.ERROR)
    return nil
  end
  return out.stdout
end

-- Replace the given range with the corrected text.
local function fix(engine, mode)
  local buf = 0
  local srow, erow

  if mode == "visual" then
    -- '< and '> are only set after leaving visual mode.
    vim.cmd("normal! \27")
    srow = vim.fn.line("'<") - 1
    erow = vim.fn.line("'>")
  else
    srow, erow = 0, vim.api.nvim_buf_line_count(buf)
  end

  local lines = vim.api.nvim_buf_get_lines(buf, srow, erow, false)
  if #lines == 0 then return end

  local script = vim.fn.expand("~/.config/hypr/scripts/grammar-stdin")
  local result = run({ script, engine }, lines)
  if not result then return end

  result = result:gsub("\n$", "")
  vim.api.nvim_buf_set_lines(buf, srow, erow, false, vim.split(result, "\n"))
end

return {
  "AstroNvim/astrocore",
  ---@type AstroCoreOpts
  opts = {
    mappings = {
      n = {
        ["<Leader>g"] = { desc = "Grammar" },
        ["<Leader>gg"] = { function() fix("llm", "buffer") end, desc = "Fix grammar (buffer)" },
        ["<Leader>gl"] = { function() fix("offline", "buffer") end, desc = "Fix typos (buffer)" },
      },
      v = {
        ["<Leader>g"] = { desc = "Grammar" },
        ["<Leader>gg"] = { function() fix("llm", "visual") end, desc = "Fix grammar (selection)" },
        ["<Leader>gl"] = { function() fix("offline", "visual") end, desc = "Fix typos (selection)" },
      },
    },
  },
}
