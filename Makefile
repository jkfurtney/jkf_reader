MAIN = booklet
PDF  = $(MAIN).pdf
IMPOSED = $(MAIN)-imposed.pdf

.PHONY: all imposed clean

# Compile content PDF (run twice for page numbers/TOC)
all: $(PDF)

$(PDF): $(MAIN).tex
	pdflatex -interaction=nonstopmode $(MAIN).tex
	pdflatex -interaction=nonstopmode $(MAIN).tex

# Impose pages for booklet printing (requires pdfbook2)
imposed: $(PDF)
	pdfbook2 --paper=letterpaper $(PDF)

clean:
	rm -f *.aux *.log *.out *.toc $(PDF) $(IMPOSED)
