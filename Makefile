MAIN = booklet
PDF  = $(MAIN).pdf
IMPOSED = $(MAIN)-imposed.pdf

.PHONY: all imposed clean

# Compile content PDF (run twice for page numbers/TOC)
all: $(PDF)

$(PDF): $(MAIN).tex
	pdflatex -interaction=nonstopmode $(MAIN).tex
	pdflatex -interaction=nonstopmode $(MAIN).tex
	@if grep -q 'Overfull \\hbox' $(MAIN).log; then \
		echo ""; \
		echo "ERROR: wrapped lines detected:"; \
		grep 'Overfull \\hbox' $(MAIN).log; \
		rm -f $(PDF); \
		exit 1; \
	fi

# Impose pages for booklet printing (requires pdfbook2)
imposed: $(PDF)
	pdfbook2 --paper=letterpaper $(PDF)

clean:
	rm -f *.aux *.log *.out *.toc $(PDF) $(IMPOSED)
