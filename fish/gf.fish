function gf --description 'Fix grammar from stdin or a file (auto-detects en/es/fr)'
    set -l ft /usr/bin/fasttext
    set -l fm /usr/share/languagetool/fasttext/lid.176.bin
    if test (count $argv) -gt 0
        languagetool -adl --fasttextbinary $ft --fasttextmodel $fm --apply $argv 2>/dev/null
    else
        languagetool -adl --fasttextbinary $ft --fasttextmodel $fm --apply - 2>/dev/null
    end
end
