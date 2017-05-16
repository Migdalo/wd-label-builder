import wdlabelbuilder.wdlabelbuilder as wdlabelbuilder
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class WDLabelBuilderTests(unittest.TestCase):

    def test_timeseries_label_qs(self):
        expected = 'Q2052948	Lfi	"eduskuntavaalit 1907"\n' +\
                   'Q1853901	Lfi	"eduskuntavaalit 1908"\n' +\
                   'Q1571365	Lfi	"eduskuntavaalit 1909"\n' +\
                   'Q1852888	Lfi	"eduskuntavaalit 1910"\n' +\
                   'Q1571375	Lfi	"eduskuntavaalit 1911"\n'
        commands = ['-l', '-t', '-p', 'eduskuntavaalit',
                    'fi', './tests/query.json']
        outfile = StringIO()
        wdlabelbuilder.process_arguments(commands, outfile)
        self.assertMultiLineEqual(outfile.getvalue(), expected)
        outfile.close()

    def test_timeseries_description_qs(self):
        expected = 'Q2052948	Dfi	"eduskuntavaalit 1907"\n' +\
                   'Q1853901	Dfi	"eduskuntavaalit 1908"\n' +\
                   'Q1571365	Dfi	"eduskuntavaalit 1909"\n' +\
                   'Q1852888	Dfi	"eduskuntavaalit 1910"\n' +\
                   'Q1571375	Dfi	"eduskuntavaalit 1911"\n'
        commands = ['-d', '-t', '-p', 'eduskuntavaalit',
                    'fi', './tests/query.json']
        outfile = StringIO()
        wdlabelbuilder.process_arguments(commands, outfile)
        self.assertMultiLineEqual(outfile.getvalue(), expected)
        outfile.close()

    def test_timeseries_alias_qs(self):
        expected = 'Q2052948	Afi	"eduskuntavaalit 1907"\n' +\
                   'Q1853901	Afi	"eduskuntavaalit 1908"\n' +\
                   'Q1571365	Afi	"eduskuntavaalit 1909"\n' +\
                   'Q1852888	Afi	"eduskuntavaalit 1910"\n' +\
                   'Q1571375	Afi	"eduskuntavaalit 1911"\n'
        commands = ['-a', '-t', '-p', 'eduskuntavaalit',
                    'fi', './tests/query.json']
        outfile = StringIO()
        wdlabelbuilder.process_arguments(commands, outfile)
        self.assertMultiLineEqual(outfile.getvalue(), expected)
        outfile.close()

    def test_url_output(self):
        expected = 'https://tools.wmflabs.org/quickstatements/#v1=' +\
                   'Q2052948%09Len%09%22Finnish%20parliamentary%20election,' +\
                   '%201907%22%0AQ1853901%09Len%09%22Finnish%20parliamentary' +\
                   '%20election,%201908%22%0AQ1571365%09Len%09%22Finnish' +\
                   '%20parliamentary%20election,%201909%22%0AQ1852888%09Len' +\
                   '%09%22Finnish%20parliamentary%20election,%201910%22' +\
                   '%0AQ1571375%09Len%09%22Finnish%20parliamentary%20election,%201911%22\n'.encode('utf-8')
        commands = ['-u', '-l', 'en', './tests/query.json']
        outfile = StringIO()
        wdlabelbuilder.process_arguments(commands, outfile)
        self.assertMultiLineEqual(outfile.getvalue(), expected)
        outfile.close()

    def test_timeseries_labe_json(self):
        expected = '[{"lang": "fi","item": "Q2052948","label": "eduskuntavaalit 1907"},'+\
            '{"lang": "fi","item": "Q1853901","label": "eduskuntavaalit 1908"},'+\
            '{"lang": "fi","item": "Q1571365","label": "eduskuntavaalit 1909"},'+\
            '{"lang": "fi","item": "Q1852888","label": "eduskuntavaalit 1910"},'+\
            '{"lang": "fi","item": "Q1571375","label": "eduskuntavaalit 1911"}]'
        commands = ['-l', '-t', '-j', '-p', 'eduskuntavaalit',
                    'fi', './tests/query.json']
        outfile = StringIO()
        wdlabelbuilder.process_arguments(commands, outfile)
        self.assertMultiLineEqual(outfile.getvalue(), expected)
        outfile.close()

    def test_wrong_input_json_titles(self):
        ''' Input an empty json file, expect SystemExit. '''
        commands = ['-l', 'fi', '-q', 'asd', '-n', 'asd', './tests/query.json']
        with self.assertRaises(SystemExit):
            args = wdlabelbuilder.process_arguments(commands)

    def test_empty_input_file(self):
        ''' Input an empty json file, expect SystemExit. '''
        commands = ['-l', 'fi', 'empty.json']
        with self.assertRaises(SystemExit):
            args = wdlabelbuilder.process_arguments(commands)

    def test_wrong_input_filepath(self):
        ''' Input a wrong input filepath, expect SystemExit. '''
        commands = ['-l', 'fi', 'woefichtr.json']
        with self.assertRaises(SystemExit):
            args = wdlabelbuilder.process_arguments(commands)

    def test_no_lda(self):
        ''' Input arguments without -l, -d or -a, expect SystemExit. '''
        commands = ['fi', 'query.json']
        with self.assertRaises(SystemExit):
            args = wdlabelbuilder.process_arguments(commands)


if __name__ == '__main__':
    unittest.main()