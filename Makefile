#
# Makefile, um die Geschäftsordnung für Plenen der ZaPF von der LaTeX-Datei zu erstellen.
#

all: GO

GO:
	pdflatex GO.tex

.PHONY : clean
clean:
	@-rm *.pdf *.aux *.log *.out
