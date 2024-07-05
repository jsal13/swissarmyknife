set shell := ["zsh", "-cu"]

default:
    just --list

tools:
    du -d 3 | sed -nE 's/.\/tools\/(.*)\/(.*)/\1 \2/p' | awk '{ print $2 " :: "  $3}' | sort

generate name:
    @echo 'Generating ./{{name}} folder...'
    @cp -R ./_tool_template './{{name}}'
    @sed -i -e 's/TOOL_NAME/{{name}}/g' './{{name}}/README.md'