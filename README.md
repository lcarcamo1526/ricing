# ricing

Personal desktop configuration: Hyprland, a Corne split keyboard, and a
grammar-correction toolchain wired into every place text gets typed.

## Layout

| Path | What |
|------|------|
| `hyprland/scripts/` | grammar correction scripts |
| `hyprland/config/` | keybindings |
| `keyboard/corne/` | Vial layout for the Corne |
| `nvim/` | AstroNvim grammar plugin |
| `kitty/` | terminal config, keyboard text selection |
| `nchat/` | nchat spell-check hook |
| `fish/` | shell config and the `gf` helper |
| `shell/` | session-wide environment |

## Grammar correction

One prompt and model behind several entry points. Targets a C1 register,
replaces calques with idiomatic equivalents, and reports a short "pattern
worth learning" note with each fix.

| Where | Trigger | Engine |
|-------|---------|--------|
| GUI apps / browser | `Super+Y` / `Super+U` | LLM / offline |
| Corne | outer-left thumb + `F` / `D` | LLM / offline |
| nchat compose | `Alt+$` | LLM |
| Neovim | `<Leader>gg` / `<Leader>gl` | LLM / offline |
| Shell pipe | `grammar-stdin llm` | either |

**Engines**

- **LLM** — `anthropic/claude-haiku-5.5` via OpenRouter, falling back to
  `openai/gpt-oss-20b`. Requests set `provider.data_collection: "deny"`.
  Fixes grammar, redundancy and idiom. ~1.2s.
- **Offline** — a local LanguageTool server with fastText language
  detection (en/es/fr). Typos and grammar only; it cannot restructure a
  sentence. ~300ms, no network.

### Setup

```sh
# offline engine
sudo pacman -S languagetool fasttext
sudo curl -L -o /usr/share/languagetool/fasttext/lid.176.bin \
  https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
sudo systemctl enable --now languagetool

# synthetic key events for clipboard-based entry points
systemctl --user enable --now ydotool

# LLM engine
echo 'sk-or-v1-...' > ~/.config/hypr/scripts/.openrouter-key
chmod 600 ~/.config/hypr/scripts/.openrouter-key
```

The key file is gitignored and must never be committed.

## Corne

6-column Corne on Vial. Both layer keys sit on the left thumbs so every
layer is held with one hand and typed with the other.

- `Shift+Backspace` → Delete; `Ctrl+Shift+Backspace` → delete word right
- Layer 1 (middle thumb): vim arrows on `HJKL`, word jump on `N`/`M`
- Layer 2 (outer thumb): window focus and movement, workspaces, grammar keys

Layer 2 sends `Super+arrow` rather than `Super+HJKL`, which would collide
with Hyprland's `Super+L` lock-screen binding.
