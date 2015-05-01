#!/usr/bin/env python2

#Copyright (c) 2010 Juri Hamburg (Mediawiki support)
#Copyright (c) 2007-2010 Kumar McMillan (code.google.com/p/wikir)
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#of the Software, and to permit persons to whom the Software is furnished to do
#so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.



# Values for Mediawiki import/export xml here.
#CONTRIBUTOR = None

import sys
import re
from optparse import OptionParser

from docutils.nodes import SparseNodeVisitor, paragraph, title_reference, emphasis
from docutils import nodes
from docutils.writers import Writer
from docutils.core import publish_string, publish_doctree

from xml.dom.minidom import Document


class FmtHelper:

    def splitCamelCase(self, camelcase):
        """
        Splits camelcased word into multiple words.
        """
        return re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z]))', ' ', camelcase).strip()



class WikiWriter(Writer):

    def __init__(self, visitor):
        self.visitor = visitor
        Writer.__init__(self)

    def translate(self):
        if self.visitor == 'mediawiki':
            visitor = MediaWikiVisitor(self.document)
        elif self.visitor == 'googlewiki':
            visitor = GoogleWikiVisitor(self.document)

        self.document.walkabout(visitor)
        self.output = visitor.astext()
        self.preformat = False


class GoogleWikiVisitor(SparseNodeVisitor):

    def __init__(self, document):
        SparseNodeVisitor.__init__(self, document)
        self.list_depth = 0
        self.list_item_prefix = None
        self.indent = self.old_indent = ''
        self.output = []
        self.preformat = False

    def astext(self):
        output = []
        for out in self.output:
            if out is not None:
                output.append(out)
        return ''.join(output)

    def visit_Text(self, node):
        data = node.astext()
        if not self.preformat:
            data = data.lstrip('\n\r')
            data = data.replace('\r', '')
            data = data.replace('\n', ' ')
        self.output.append(data)

    def visit_bullet_list(self, node):
        self.list_depth += 1
        self.list_item_prefix = (' ' * self.list_depth) + '* '

    def depart_bullet_list(self, node):
        self.list_depth -= 1
        if self.list_depth == 0:
            self.list_item_prefix = None
        else:
            (' ' * self.list_depth) + '* '
        self.output.append('\n\n')

    def visit_list_item(self, node):
        self.old_indent = self.indent
        self.indent = self.list_item_prefix

    def depart_list_item(self, node):
        self.indent = self.old_indent

    def visit_literal_block(self, node):
        self.output.extend(['{{{', '\n'])
        self.preformat = True

    def depart_literal_block(self, node):
        self.output.extend(['\n', '}}}', '\n\n'])
        self.preformat = False

    def visit_paragraph(self, node):
        self.output.append(self.indent)

    def depart_paragraph(self, node):
        self.output.append('\n\n')
        if self.indent == self.list_item_prefix:
            # we're in a sub paragraph of a list item
            self.indent = ' ' * self.list_depth

    def visit_reference(self, node):
        if node.has_key('refuri'):
            href = node['refuri']
        elif node.has_key('refid'):
            href = '#' + node['refid']
        else:
            href = None
        self.output.append('[' + href + ' ')

    def depart_reference(self, node):
        self.output.append(']')

    def visit_subtitle(self, node):
        self.output.append('=== ')

    def depart_subtitle(self, node):
        self.output.append(' ===\n\n')
        self.list_depth = 0
        self.indent = ''

    def visit_title(self, node):
        self.output.append('== ')

    def depart_title(self, node):
        self.output.append(' ==\n\n')
        self.list_depth = 0
        self.indent = ''

    def visit_title_reference(self, node):
        self.output.append("`")

    def depart_title_reference(self, node):
        self.output.append("`")

    def visit_emphasis(self, node):
        self.output.append('*')

    def depart_emphasis(self, node):
        self.output.append('*')

    def visit_literal(self, node):
        self.output.append('`')

    def depart_literal(self, node):
        self.output.append('`')

class MediaWikiVisitor(GoogleWikiVisitor):
    """visits RST nodes and transforms into MediaWiki syntax.
    """
    def visit_literal_block(self, node):
        self.output.append('<pre>')
        self.preformat = True

    def depart_literal_block(self, node):
        self.output.extend(['</pre>', '\n'])
        self.preformat = False

    def visit_emphasis(self, node):
        self.output.append('\'\'')

    def depart_emphasis(self, node):
        self.output.append('\'\'')

    def visit_strong(self, node):
        self.output.append('\'\'\'')

    def depart_strong(self, node):
        self.output.append('\'\'\'')

    def visit_literal(self, node):
        self.output.append('<code>')

    def depart_literal(self, node):
        self.output.append('</code>')

    def _visit_list(self, node, bullet):
        self.list_depth += 1
        self.list_item_prefix = bullet * self.list_depth

    def _depart_list(self, node, bullet):
        next_node = node.next_node()
        self.list_depth -= 1
        if self.list_depth == 0:
            self.list_item_prefix = None
        else:
            self.list_item_prefix = bullet * self.list_depth
        output_sep = True
        if isinstance(next_node, nodes.list_item):
            if self.list_depth > 0:
                output_sep = False
        if output_sep:
            self.output.append('\n\n')

    def visit_bullet_list(self, node):
        self._visit_list(node, "*")

    def depart_bullet_list(self, node):
        self._depart_list(node, '*')

    def visit_enumerated_list(self, node):
        self._visit_list(node, "#")

    def depart_enumerated_list(self, node):
        self._depart_list(node, '#')

    def visit_term(self, node):
        self.output.append('; ')

    def depart_term(self, node):
        self.output.append('\n')

    def visit_definition(self, node):
        self.output.append(': ')

    def visit_paragraph(self, node):
        self.output.append(self.indent)

    def depart_paragraph(self, node):
        if self.indent == self.list_item_prefix:
            self.output.append('\n')
        else:
            self.output.append('\n\n')

        if self.indent == self.list_item_prefix:
            # we're in a sub paragraph of a list item
            self.indent = ' ' * self.list_depth

    def visit_image(self, node):
        atts = node.attributes.copy()
        atts['src'] = atts['uri']
        del atts['uri']
        if not atts.has_key('alt'):
            atts['alt'] = atts['src']
        self.output.extend(['[[File:', atts['src'], '|', atts['alt'], ']]'])

    def depart_image(self, node):
        self.output.append('\n\n')

    def visit_block_quote(self, node):
        self.output.append('<blockquote>')

    def depart_block_quote(self, node):
        self.output.extend(['</blockquote>', '\n'])

    def visit_comment(self, node):
        self.output.append('<!-- ')

    def depart_comment(self, node):
        self.output.extend([' --!>', '\n'])

    def visit_title_reference(self, node):
        pass

    def depart_title_reference(self, node):
        pass


class MediawikiXMLWrapper():
    """
    Creates a minimal XML import/export header for Mediawiki document
    and wraps a text.
    """

    def wrapInMinimalHeader(self, title, text):
        """
        Wraps the text into  a minimal header and returns it as
        string
        """
        doc = Document()

        #create elements
        elMwiki       = doc.createElement("mediawiki")
        elPage        = doc.createElement("page")
        elTitle       = doc.createElement("title")
        elRev         = doc.createElement("revision")
        elText        = doc.createElement("text")

        textstr     = doc.createTextNode(text)
        titlestr    = doc.createTextNode(title)

        doc.appendChild(elMwiki)
        elMwiki.setAttribute("xmlns", "http://www.mediawiki.org/xml/export-0.4/")
        elMwiki.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        elMwiki.setAttribute("xsi:schemaLocation",
                "http://www.mediawiki.org/xml/export-0.4/ http://www.mediawiki.org/xml/export-0.4.xsd")
        elMwiki.setAttribute("version", "0.4")
        elMwiki.setAttribute("xml:lang", "de")


        elMwiki.appendChild(elPage)
        elPage.appendChild(elTitle)
        elPage.appendChild(elRev)
        elRev.appendChild(elText)
        elText.appendChild(textstr)
        elTitle.appendChild(titlestr)


        return doc.toxml() #don't prettify


def main(source, writer='mediawiki', mediaxml=False, docTitle=None):
    settings_overrides = {
        #'halt_level': 2,
        'report_level': 5,
        #'input_encoding': 'utf-8',
        #'output_encoding': 'utf-8',
    }


    kw = {};
    kw.setdefault('writer', WikiWriter(visitor=writer))
    kw.setdefault('settings_overrides', {})
    kw['settings_overrides'].update(settings_overrides)

    output = source
    fh = FmtHelper()


    #markup conversion
    output = publish_string(output, **kw)

    #xml wrap
    if mediaxml:
        if not docTitle:
            doctreedom = publish_doctree(source).asdom()
            titlenodes = []
            titlenodes = doctreedom.getElementsByTagName('title')
            titlenodes.reverse()
            while not docTitle and titlenodes:
                t = titlenodes.pop()
                docTitle = t.childNodes[0].nodeValue
                try:
                    docTitle = docTitle.encode('utf-8')
                except:
                    pass

        if docTitle:
            mwrap = MediawikiXMLWrapper()
            #mediawiki allows no camelcased syntax for titles on export?
            docTitle = fh.splitCamelCase(docTitle.strip())
            docTitle = docTitle.title()
            output = mwrap.wrapInMinimalHeader(docTitle, output)
        else:
            sys.stderr.write('No title found. Omitting XML.\n')

    print output



if __name__ == '__main__':


    usage       = "usage: %prog [options] arg"
    optparser   = OptionParser(usage)
    validwriters= ('mediawiki', 'googlewiki')

    source          = None
    writer          = None
    mediaXML        = False
    doctitle        = None
    readOK          = False
    titleFromFile   = False

    optparser.add_option("-w", "--writer",
                        default="mediawiki",
                        action="store",
                        type="string",
                        help="writer to be used: mediawiki or googlewiki, "
                             "[default: %default]")


    optparser.add_option("-x", "--mediawiki-xml-export",
                        action="store_true",
                        dest="mediaxml",
                        default=False,
                        help="Wrap document into XML structure for mediawiki import."
                        )

    optparser.add_option("-t", "--title",
                        action="store",
                        default=None,
                        dest="doctitle",
                        type="string",
                        help="Set title to be used in XML structure for mediawiki import."
                                " If title not set: title is set to the first title node"
                                " of the restructured document."
                                " If -f is set, this option will be ignored."
                        )

    optparser.add_option("-f", "--title-from-filename",
                        action="store_true",
                        default=False,
                        dest="titleFromFile",
                        help="Set title to be used in XML structure for mediawiki import"
                                " to the filename of used source file."
                                " Takes precedence to -t. Of course that won't work with"
                                " stdin as source."
                        )



    (options, args) = optparser.parse_args()

    doctitle = options.doctitle

    if len(args) >=1:
        try:
            if options.titleFromFile:
                doctitle = args[0].split(".")[0]
            f = open(args[0], 'r')
            source = f.read()
            readOK = True
            f.close()
        except IOError, what:
            (errno, strerror) = what
            sys.stderr.write("IO Error number", errno, "(%s)\n" % strerror)
            sys.exit(1)


    if not options.writer or options.writer not in validwriters:
        sys.stderr.write("%s: Not a valid writer specified.\n" % options.writer)
        sys.exit(1)

    if not source and not readOK:
        source = sys.stdin.read()
    elif not source and readOK:
        source = ''
        #sys.stderr.write("no input to process.\n")
        #sys.exit(1)

    main(source, options.writer, options.mediaxml, docTitle=doctitle)
