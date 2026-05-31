#!/usr/bin/env python3
"""Generate impose.tex with correct saddle-stitch booklet ordering."""
import re, subprocess, sys

with open('booklet.log') as f:
    log = f.read()
m = re.search(r'Output written on booklet\.pdf \((\d+) pages', log)
if not m:
    sys.exit('ERROR: could not read page count from booklet.log')

actual = int(m.group(1))
total = actual + (4 - actual % 4) % 4  # pad to multiple of 4

# Saddle-stitch order for portrait duplex (flip on long edge):
# Sheet i (0-indexed): front=[total-2i, 2i+1], back=[2i+2, total-2i-1]
pages = []
for i in range(total // 4):
    pages += [total - 2*i, 2*i + 1,     # front of sheet
              2*i + 2, total - 2*i - 1]  # back of sheet

def slot(p):
    return str(p) if p <= actual else '{}'

page_list = ','.join(slot(p) for p in pages)

tex = r"""\documentclass{article}
\usepackage[paperwidth=8.5in,paperheight=11in,margin=0pt]{geometry}
\usepackage{pdfpages}
\begin{document}
\includepdf[pages={""" + page_list + r"""},nup=2x1,delta=0 0]{booklet.pdf}
\end{document}
"""

with open('impose.tex', 'w') as f:
    f.write(tex)

result = subprocess.run(['pdflatex', '-interaction=nonstopmode', 'impose.tex'])
sys.exit(result.returncode)
