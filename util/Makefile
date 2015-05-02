# Dies ist das Makefile um die verschiedenen Publikationsversionen der Satzung
# der ZaPF

all: html tex pdf

html: ../go.rst
	rst2html ../go.rst > ../versions/go.html

tex: ../go.rst
	rst2latex --documentclass=scrartcl --documentoptions=12pt,oneside --stylesheet=./preamble.tex --embed-stylesheet --latex-preamble= ../go.rst > ../versions/go.tex

pdf: ../versions/go.tex
	pdflatex -output-directory ../versions go.tex
	pdflatex -output-directory ../versions go.tex
	rm ../versions/go.{log,aux,out}

clean:
	rm ../versions/*
