#!/usr/bin/env python3
"""Convert a plain-text poem to a LaTeX verse block."""

import sys
import re


def convert(text):
    raw_lines = text.splitlines()

    # Strip trailing blank lines
    while raw_lines and not raw_lines[-1].strip():
        raw_lines.pop()

    # Group into stanzas (split on blank lines)
    stanzas = []
    current = []
    for line in raw_lines:
        if line.strip() == "":
            if current:
                stanzas.append(current)
                current = []
        else:
            current.append(line)
    if current:
        stanzas.append(current)

    out = []
    for s_idx, stanza in enumerate(stanzas):
        last_stanza = (s_idx == len(stanzas) - 1)
        for l_idx, line in enumerate(stanza):
            last_line = (l_idx == len(stanza) - 1)

            # Detect and convert leading whitespace to \vin tokens
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            # One \vin per 4 spaces (or part thereof) of indentation
            vin_count = (indent + 3) // 4 if indent > 0 else 0
            prefix = r"\vin " * vin_count

            # Escape bare % and & that aren't already escaped
            body = re.sub(r'(?<!\\)%', r'\\%', stripped)
            body = re.sub(r'(?<!\\)&', r'\\&', body)

            if last_line and last_stanza:
                out.append(f"{prefix}{body}")          # last line: no suffix
            elif last_line:
                out.append(f"{prefix}{body}\\\\!")     # end of stanza
                out.append("")                          # blank line between stanzas
            else:
                out.append(f"{prefix}{body}\\\\")      # mid-stanza line

    return "\n".join(out)


def main():
    if len(sys.argv) < 2:
        print("Usage: poem2latex.py <input.txt>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        text = f.read()

    print(convert(text))


if __name__ == "__main__":
    main()
