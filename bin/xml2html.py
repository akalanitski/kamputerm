#!/usr/bin/env python3

import argparse
import html
import sys
import xml.sax
import xml.sax.handler


class KamputermSaxHandler(xml.sax.handler.ContentHandler):

    def __init__(self, output, no_header):
        xml.sax.handler.ContentHandler.__init__(self)
        self.num = 0
        self.text = ''
        self.reset()
        self.kind = ''
        self.out = output
        self.no_header = no_header

    def reset(self):
        self.keys = []
        self.synonyms = []
        self.beDefinition = '−'
        self.byDefinition = '−'
        self.mtDefinition = '−'
        self.rmDefinition = '−'

    def startDocument(self):
        if self.no_header == False:
            self.out.write('<html><head>')
            self.out.write('<meta http-equiv="Content-Type" content="text/html;charset=utf8" />')
            #self.out.write('<style>')
            #for line in open('../css/article-style.css'):
            #    self.out.write(line)
            #self.out.write('</style>')
            self.out.write('</head><body>')
        self.out.write('<table border="1" cellspacing="0" cellpadding="4">')
        self.out.write('<tr><th>Тэрмін</th><th>Сынонім</th><th>Пераклад (школьны правапіс)</th>')
        self.out.write('<th>Пераклад (класічны правапіс)</th><th>Сустрэчы</th><th>Каметар</th>')

    def endDocument(self):
        self.out.write('</table>')
        if self.no_header == False:
            self.out.write('</body></html>')

    def startElement(self, name, attrs):
        if name != 'definition':
            return
        if 'kind' in attrs.getNames():
            self.kind = attrs.getValue('kind')
        else:
            self.kind = 'al'

    def endElement(self, name):
        if name == 'article':
            #TODO start
            self.num += 1
            if 'на перагляд' in self.rmDefinition.lower():
                self.out.write('<tr bgcolor="yellow"><td>' + str(self.num) + '</td><td>')
            elif 'з перакладу' in self.rmDefinition.lower():
                self.out.write('<tr bgcolor="green"><td>' + str(self.num) + '</td><td>')
            else:
                self.out.write('<tr><td>' + str(self.num) + '</td><td>')
            for key in self.keys:
                self.out.write(key)
                self.out.write('<br>')
            self.out.write('</td><td>')
            if len(self.synonyms) > 0:
                for synonym in self.synonyms:
                    self.out.write(synonym)
                    self.out.write('<br>')
            else:
                self.out.write('−')
            self.out.write('</td><td>')
            self.out.write(self.byDefinition)
            self.out.write('</td><td>')
            self.out.write(self.beDefinition)
            self.out.write('</td><td>')
            self.out.write(self.mtDefinition)
            self.out.write('</td><td>')
            self.out.write(self.rmDefinition)
            self.out.write('</tr>')
            #TODO end
            self.reset()
        elif name == 'key':
            self.keys.append(html.escape(self.text.strip(' \n\t')))
        elif name == 'synonym':
            self.synonyms.append(self.text.strip(' \n\t'))
        elif name == 'definition':
            definition = self.text.strip(' \n\t')
            definition = definition.replace('<em>', '<em style="color: green;">')
            if self.kind == 'be':
                self.beDefinition = definition
            if self.kind == 'by':
                self.byDefinition = definition
            if self.kind == 'mt':
                self.mtDefinition = definition
            if self.kind == 'rm':
                self.rmDefinition = definition
            if self.kind == 'al':
                self.beDefinition = definition
                self.byDefinition = definition
        self.text = ''

    def characters(self, chars):
        self.text += chars

def parseArguments():
    parser = argparse.ArgumentParser(description='Convert a stardict textual file to an html table')
    parser.add_argument('input', metavar='FILENAME', nargs='?', default='-', help='input file name. If missing then reads stdin')
    parser.add_argument('-o', '--output', default='-', metavar='FILENAME', help='output file name. If it don\'t enumerate then writes to stdout')
    parser.add_argument('--no-header', action='store_true', help='write without general html-tags (like html, head, body)')
    args = parser.parse_args()
    if args.input == '-':
        args.input = sys.stdin
    else:
        args.input = open(args.input, 'r', encoding='utf8')
    if args.output == '-':
        args.output = sys.stdout
    else:
        args.output = open(args.output, 'w', encoding='utf8')
    return args

def main():
    args = parseArguments()
    xml.sax.parse(args.input, KamputermSaxHandler(args.output, args.no_header))

if __name__ == '__main__':
    main()
