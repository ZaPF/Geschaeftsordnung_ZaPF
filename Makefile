#
# Dies ist das 'Makefile' um die Geschäftsordnung für Plenen der ZaPF aus der LaTeX-Datei zu erstellen.
#
# Es hilft bei der Erstellung der Geschäftsordnung alS PDF-Datei (sowie als Mediawiki / Markdown Dateien)

# Zur Erstellung einfach in einer Linux/Mac Kommandozeile den folgenden Befehl eingeben:
# make all

# Alle Zieldateien erstellen: PDF, Mediawiki und Markdown:
#all: GO.pdf GO.mediawiki.txt GO.markdown.txt
all: GO.pdf GO.mediawiki.txt

# Die einzelnen Zieldateien werden wie folgt erstellt:
GO.pdf: GO.tex
	pdflatex GO.tex
	pdflatex GO.tex

GO.mediawiki.txt: GO.tex
	pandoc -f latex -t mediawiki -o GO.mediawiki.txt GO.tex
	### Korrekturen an der Mediawiki-Version:
	### * Zeilen mit eingerücktem Text würden im Wiki als <code> dargestellt:
	#sed -i 's/^ //g' GO.mediawiki.txt
	## Benötigt leider doch noch einige 'Handarbeit':
	## Entfernen von {header_go}
	## Entfernen des alles umschließenden <blockquote> Tags
	## Einfügen von  ----  sowie == Kommentare == vor dem <references /> Tag

#GO.markdown.txt: GO.tex
#	pandoc -f latex -t markdown -o GO.markdown.txt GO.tex
#	### Korrekturen an der Markdown-Version für Veröffentlichung
#	###  auf https://vmp.ethz.ch/zapfwiki/index.php/Gesch%C3%A4ftsordnung_f%C3%BCr_Plenen_der_ZaPF
#	### * Überschriften weiter Einrücken
#	### * und Leerzeilen entfernen ( ';' trennt sed Befehle voneinenader )
#	#sed -i 's/^# /### /g;/^$$/d' GO.markdown.txt

# delete temporary files and products of the .tex source file
.PHONY : clean
clean:
	@-rm -rf *~ *.mediawiki.txt *markdown.txt *.toc *.aux *.log *.dvi *.ps *.pdf



