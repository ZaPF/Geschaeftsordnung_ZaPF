# Geschäftsordnung für Plenen der ZaPF

Dieses Repository enthält die Quelldateien für die Geschäftsordnung für Plenen der ZaPF.

## Homepage

* <https://zapf.wiki/Geschäftsordnung_für_Plenen_der_ZaPF>

## Kontakt

* [Ständiger Ausschuss der Physik-Fachschaften – kurz StAPF](http://zapfev.de/zapf/stapf)
  * E-Mail: **stapf@zapf.in**

## Wegweiser

Die `master` branch enthält die offiziele Variante der Geschäftsordnung in
Markdown. Aus dieser können mit pandoc die Versionen in
[HTML](./versions/go.html) und [LaTeX](./versions/go.tex) und daraus die
[PDF-Version](./versions/go.pdf) sowie die Version in
[Mediawiki-Markup](./versions/go.wiki) generiert werden.

Die Versionen werden immer nach einer ZaPF, auf deren Abschlussplenum die GO
geändert wurde, nachdem diese als [Pull
Requests](https://github.com/ZaPF/Geschaeftsordnung_ZaPF/pulls) gemergt wurden
und [der Änderungsvermerkt](./go.md#Anhang%3A%20Versionshistorie%20%7B-%7D)
hinzugefügt wurde, neu generiert.

Um die Versionen neu zu generieren führt man den Befehl
```bash
make -C util
```
aus. Was dabei passiert, kann man im [Makefile](./util/Makefile) sehen.

Ein Beispiel für einen Commit, in dem der Änderungsvemerkt hinzugefügt wird und
die neu generierten Versionen hinzugefügt werden, ist
[dieser](https://github.com/ZaPF/Geschaeftsordnung_ZaPF/commit/4e34bc2ec9dd602ff18582e4c71fd553f4ffb640).
