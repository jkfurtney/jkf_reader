# jkf_reader — LaTeX Poetry Booklet

A LaTeX project for printing poetry as saddle-stitched booklets (signatures).
The physical format is 8.5×11 paper folded along the long axis, producing
4.25×11 pages — tall and thin.

## Build

```bash
make          # → booklet.pdf  (content at final page size)
make imposed  # → booklet-book.pdf  (imposed for duplex printing, requires pdfpages)
make clean
```

`make` will fail with an error if any verse line produces an overfull hbox.

**Known limitation — silent runovers:** memoir's verse environment does its
own "runover" line wrapping (a typographic feature) that bypasses LaTeX's
normal overfull-hbox system entirely. Long lines wrap silently with no
warning in the log. The current `make` check does NOT catch these. If a
line visually wraps in the PDF, the fix is to shorten the line or reduce
the font size — not to widen the margins.

**Possible future fix:** wrap each verse line in a `\VL{...}` macro that
uses `\sbox`/`\wd` to measure the line against `\linewidth` and writes
a `VERSE LINE TOO WIDE` marker to the log, then grep for it in the Makefile.
`poem2latex.py` would need to emit `\VL{text}\\` instead of `text\\`.

Install deps (if needed): `sudo apt install texlive-latex-extra texlive-extra-utils`

## Printing

Print `booklet-book.pdf` duplex, **flip on long edge**. Fold and saddle-stitch
(staple through spine). Aim for 8 or 16 pages per signature.

## Adding poems

### Quickstart: poem text in i.txt

1. Paste the plain-text poem into `i.txt` (overwrite whatever is there)
2. Run the converter and review the output:
   ```bash
   python3 poem2latex.py i.txt
   ```
3. In `booklet.tex`, find the last `\clearpage` before `\end{document}` and add:
   ```latex
   \clearpage

   % ── Poem title ──────────────────────────────────────────────
   \poemtitle{Title Here}
   \poemauthor{Author Name}

   \begin{verse}
   <paste converter output here>
   \end{verse}
   ```
4. If the poem's first lines are a title/author/epigraph (as with Browning's
   Childe Roland), strip those from the verse block and use `\poemtitle` /
   `\poemauthor` instead.
5. `make` to check for overfull lines, then `make imposed` for the print PDF.

### The converter script

`poem2latex.py` converts a plain-text poem to a LaTeX verse block:

```bash
python3 poem2latex.py mypoem.txt
```

It handles:
- `\\` line endings within stanzas
- `\\!` + blank line at stanza breaks
- Leading whitespace → `\vin` tokens (one per 4 spaces)
- Escapes `%` and `&`

Paste the output into `booklet.tex` wrapped in `\begin{verse}...\end{verse}`.

### Poem template in booklet.tex

```latex
% ── Poem title ──────────────────────────────────────────────
\poemtitle{Title Here}

\begin{verse}
First line of poem,\\
second line of poem.\\!

Second stanza begins here,\\
and ends here.
\end{verse}

\clearpage
```

### Known gotcha: single vs double backslash

Every line in a verse block must end with `\\`. A single `\` at end of line
is a control-space — it silently merges the line with the next one rather than
breaking. This is easy to introduce when manually editing lines that end with a
curly apostrophe (`'`). The `poem2latex.py` script generates `\\` correctly;
the bug only appears with manual edits.

## LaTeX verse cheatsheet

| Syntax | Effect |
|---|---|
| `line text\\` | line break |
| `last stanza line\\!` | line break + stanza gap |
| `\vin text` | indent one level (continuation line) |
| `\poemtitle{...}` | formatted poem title (memoir class) |

## Source poems

- Tennyson, "Ulysses"
- Browning, "Childe Roland to the Dark Tower Came"
- Blake, "The Tyger"
- Shakespeare, "Tomorrow, and tomorrow, and tomorrow" (Macbeth)
- Shakespeare, "To be, or not to be" (Hamlet)
- Shakespeare, "Get thee to a nunnery" (Hamlet)
- Byron, "She Walks in Beauty"
- Shelley, "Ozymandias"
- Shakespeare, "Friends, Romans, countrymen" (Julius Caesar)
- Tennyson, "The Lotos-eaters"

All pre-1928, public domain in the US.

Pre-1928 works are public domain in the US. For clean plain-text sources use
Project Gutenberg (`gutenberg.org`), not modern scholarly editions (which may
have their own copyright on editorial matter).

## Fonts

Currently uses Latin Modern (`lmodern`) — the scalable version of Computer
Modern, required for `microtype` font expansion. To switch to a different
serif, uncomment/add a font package before `\usepackage[T1]{fontenc}`, e.g.:

```latex
\usepackage{ebgaramond}
```

## Pushing to GitHub

SSH keys are not configured in this environment. Push via the gh CLI token:

```bash
TOKEN=$(gh auth token) && git push https://x-access-token:${TOKEN}@github.com/jkfurtney/jkf_reader.git master
```
