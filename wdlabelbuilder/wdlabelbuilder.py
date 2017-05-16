# -*- coding: UTF-8 -*-
"""
WDLabelBuilder creates labels, descriptions and aliases for Wikidata items
based on existing labels for those items. It then creates a file containing
QuickStatements compatible statements.
It's also possible to change the output format to json.

"""

from __future__ import print_function
from string import ascii_lowercase
import argparse
import json
import os
import sys

try:
    from simplelinkedlist import Node, LinkedList
except ImportError:
    from wdlabelbuilder.simplelinkedlist import Node, LinkedList


class WDLabelBuilder():

    def __init__(self, args, output_stream=sys.stdout):
        self.lang = args.language
        self.timeseries = args.timeseries
        self.output_json = args.json
        self.output_url = args.url
        self.qnumber_title = self.parse(args.qtitle)
        self.label_title = self.parse(args.ltitle)
        self.prefix = self.parse(args.prefix)
        self.suffix = self.parse(args.suffix)
        self.get_output_type(args)
        if output_stream:
            self.output_stream = output_stream
        else:
            self.output_stream = None
        if self.output_json:
            self.output_filename = 'output.json'
        else:
            self.output_filename = 'output'
        self.ll = LinkedList()
        self.read_json(args.filename)

    def parse(self, value):
        if sys.version_info.major > 2:
            return value
        else:
            return unicode(value, encoding='utf-8')

    def get_output_type(self, args):
        '''
        Store strings that are used in the output file
        to specify the type of each item.
        '''
        if args.label:
            self.output_type = ('L', 'label')
        elif args.description:
            self.output_type = ('D', 'description')
        elif args.alias:
            self.output_type = ('A', 'alias')
        else:
            self.output_type = None

    def generate_file(self):
        ''' Decide if the output file is json or qs file. '''
        if self.output_json:
            self.write_to_json_file()
        elif self.output_url:
            self.output_as_url()
        else:
            self.write_to_qs_file()

    def read_json(self, filename):
        ''' Read data from json file. '''
        if not os.path.isfile(filename):
            print('Failed to find the file:', filename)
            sys.exit(1)
        try:
            with open(filename, 'r') as infile:
                items = json.load(infile)
        except ValueError as ve:
            print('Failed to read json file:', filename)
            print(ve)
            sys.exit(1)
        if not items:
            print('Failed to read items from file.')
            sys.exit(1)
        try:
            for item in items:
                node = Node(self.get_qnumber_from_url(
                    item[self.qnumber_title]), item[self.label_title])
                self.ll.add_node(node)
        except KeyError:
            print('Failed to find one or more of the json titles.')
            print('  Expected "' + self.qnumber_title +
                  '" and "' + self.label_title + '".')
            print('  Found "' + list(item)[0] +
                  '" and "' + list(item)[1] + '" instead.')
            sys.exit(1)

    def get_qnumber_from_url(self, url_string):
        ''' Parse qnumber from Wikidata url. '''
        return ''.join(url_string.split('/')[-1:])

    def get_new_label(self, node):
        ''' Generate new label, description or alias for an item. '''
        new_label = ''
        if self.prefix:
            new_label += self.prefix
        if self.timeseries:
            new_label += ' ' + str(node.point_in_time)
        if self.suffix:
            new_label += ' ' + self.suffix
        if not new_label:
            new_label = node.label
        return new_label.strip()

    def output_as_url(self):
        ''' Output the results as a QuickStatements 2 url. '''
        url = 'https://tools.wmflabs.org/quickstatements/#v1='
        node = self.ll.head
        count = 0
        tab = '%09'
        quote = '%22'
        newline = '%0A'
        while node:
            new_label = self.get_new_label(node)
            url += node.qnumber + tab + self.output_type[0] + self.lang
            url += tab + quote + new_label + quote + newline
            node = node.next
            count += 1
        url = url.replace(' ', '%20')
        print(count, 'items processed.')
        print('NOTICE: When opening the url in a browser, ' +
              'it might take a moment for the page to load.')
        if url[-3:] == newline:
            url = url[:-3].encode('utf-8')
        else:
            url = url.encode('utf-8')
        print(url, file=self.output_stream)

    def save_to_file(self, outfile):
        count = 0
        node = self.ll.head
        while node:
            line = node.qnumber + self.ll.TAB + self.output_type[0]\
                + self.lang + self.ll.TAB
            new_label = self.get_new_label(node)
            line += '"' + new_label + '"' + '\n'
            outfile.write(line.encode('utf-8'))
            count += 1
            node = node.next
        return count

    def write_to_qs_file(self):
        ''' Write labels, aliases and descriptions to QuickStatements file. '''
        if sys.version_info.major > 2:
            save_type = 'wb'
        else:
            save_type = 'w'
        if self.output_stream != sys.stdout:
            count = self.save_to_file(self.output_stream)
        else:
            with open(self.output_filename, save_type) as outfile:
                count = self.save_to_file(outfile)
        print(count, 'lines saved to file.')

    def write_to_json_file(self):
        ''' Write labels, aliases and descriptions to json file. '''
        count = 0
        node = self.ll.head
        data = []
        while node:
            new_label = self.get_new_label(node)
            line = {}
            line[self.qnumber_title] = node.qnumber
            line[self.output_type[1]] = new_label
            line['lang'] = self.lang
            data.append(line)
            count += 1
            node = node.next
        if self.output_stream != sys.stdout:
            json.dump(data, self.output_stream, ensure_ascii=True,
                      separators=(',', ': '))
        else:
            with open(self.output_filename, 'w') as outfile:
                json.dump(data, outfile, ensure_ascii=True,
                          indent=4, separators=(',', ': '))
        print(count, 'lines saved to file.')


def process_arguments(input_args=None, output_filename=''):
    ''' Generate help page and process user arguments. '''
    parser = argparse.ArgumentParser(
        description='Create labels, descriptions and aliases ' +
        'for Wikidata items based on existing labels for those items.')
    parser.add_argument(
        'language', help='Language of the label/alias/description ' +
        'you are adding. Use Wikimedia abbreviations (e.g. "en", "fr").')
    parser.add_argument(
        'filename', help='Input json filepath.')
    type_group = parser.add_mutually_exclusive_group()
    type_group.add_argument(
        '-l', '--label', action='store_true', help='Generate labels')
    type_group.add_argument(
        '-a', '--alias', action='store_true', help='Generate aliases')
    type_group.add_argument(
        '-d', '--description', action='store_true',
        help='Generate descriptions')
    parser.add_argument(
        '-t', '--timeseries', action='store_true',
        help='Use numbers, such as years from labels in ' +
        'the input json to create labels in another language.')
    parser.add_argument(
        '-p', '--prefix', default='',
        help='Prefix of the label/alias/description')
    parser.add_argument(
        '-s', '--suffix', default='',
        help='Suffix of the label/alias/description')
    parser.add_argument(
        '-q', '--qtitle', default='item',
        help='Title of the qnumber field in the json file. Default is "item".')
    parser.add_argument(
        '-n', '--ltitle', default='itemLabel',
        help='Title of the label field in the json file. ' +
        'Default is "itemLabel".')
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        '-j', '--json', action='store_true',
        help='Export results as a json instead of QuickStatements commands.')
    output_group.add_argument(
        '-u', '--url', action='store_true',
        help='Export results as a QuickStatements 2 url.')
    if input_args:
        args = parser.parse_args(input_args)
    else:
        args = parser.parse_args()
    if not args.label and not args.alias and not args.description:
        raise parser.error(
            'Missing required value: label, alias or description.')
    qs_file = WDLabelBuilder(args, output_filename)
    qs_file.generate_file()

if __name__ == '__main__':
    process_arguments()
