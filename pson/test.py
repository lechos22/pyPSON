import unittest
from pson import *


class TestLexer(unittest.TestCase):
    def test(self):
        self.assertEqual([i for i in Lexer('3.14')], [('FP', 3.14)])


class TestParser(unittest.TestCase):
    def test(self):
        self.assertEqual(Parser(Lexer('3.14')).result, 3.14)


class TestDumper(unittest.TestCase):
    def test_escape(self):
        self.assertEqual(Dumper.escape('\\'), '\\\\')
        self.assertEqual(Dumper.escape('\n'), '\\n')
        self.assertEqual(Dumper.escape('\t'), '\\t')
        self.assertEqual(Dumper.escape('\x00'), '\\x00')

    def test_dumps(self):
        from math import inf, nan
        self.assertEqual(dumps(123), '123')
        self.assertEqual(dumps(3.14), '3.14')
        self.assertEqual(dumps(-2), '-2')
        self.assertEqual(dumps(-3.14), '-3.14')
        self.assertEqual(dumps('text'), '"text"')
        self.assertEqual(dumps('\\'), '"\\\\"')
        self.assertEqual(dumps(inf), 'inf')
        self.assertEqual(dumps(-inf), '-inf')
        self.assertEqual(dumps(nan), 'nan')
        self.assertEqual(dumps(None), 'null')
        self.assertEqual(dumps([1, 2, 3, 4, 5]), '[1 2 3 4 5]')
        self.assertEqual(dumps((1, 2, 3)), '[1 2 3]')
        self.assertEqual(dumps({1, 2, 3}), '[1 2 3]')
        self.assertEqual(dumps({'pi': 3.14, 'e': 2.72, 'phi': 1.62}), '(pi=3.14 e=2.72 phi=1.62)')


if __name__ == '__main__':
    unittest.main()
