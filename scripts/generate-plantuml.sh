#!/usr/bin/env bash
set -e

for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.puml$' | grep -v 'c4-lib/'); do
    echo "Generating SVG for $file"

    java -Dplantuml.allowincludeurl=true \
        -jar "$HOME/.local/share/plantuml/plantuml.jar" \
        -DRELATIVE_INCLUDE="." \
        -tsvg "$file"

    svg_file="${file%.puml}.svg"
    # ensure trailing newline so end-of-file-fixer doesn't loop
    [ -n "$(tail -c1 "$svg_file")" ] && echo >> "$svg_file"
    git add "$svg_file"
done
