MAIN = booklet
PDF  = $(MAIN).pdf

.PHONY: all imposed clean

# Compile content PDF (run twice for page numbers/TOC)
all: $(PDF) imposed

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

# Impose pages for booklet printing
imposed: $(PDF)
	python3 impose.py
	mv impose.pdf booklet-book.pdf

clean:
	rm -f *.aux *.log *.out *.toc $(PDF) booklet-book.pdf impose.tex
