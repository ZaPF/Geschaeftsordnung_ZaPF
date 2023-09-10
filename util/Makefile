# Dies ist das Makefile um die verschiedenen Publikationsversionen der Satzung
# der ZaPF

all: html wiki tex pdf

html: ../go.md
	pandoc --standalone --metadata-file=./metadata.yml --number-sections --output=../versions/go.html ../go.md

tex: ../go.md
	pandoc --standalone --metadata-file=./metadata.yml --number-sections --to=latex --output=../versions/go.tex ../go.md

pdf: ../versions/go.tex
	pdflatex -output-directory ../versions go.tex
	pdflatex -output-directory ../versions go.tex
	rm -f ../versions/go.{log,aux,out}

wiki: ../go.md
	pandoc --to=mediawiki --lua-filter=remove-attr.lua --output=../versions/go.wiki ../go.md

clean:
	rm ../versions/*
