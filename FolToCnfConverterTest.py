import unittest
from FolToCnfConverter import FolToCnfConverter
class FolToCnfConverterTest(unittest.TestCase):
    def setUp(self):
        self.cnf = None
    
    def test_convert_sentence(self):
        test_sentence = "Sibling(x,y)&Sibling(y,z)=>Sibling(x,z)"
        expected_sentence = "~Sibling(x,y)|~Sibling(y,z)|Sibling(x,z)"
        self.cnf = FolToCnfConverter()
        result_sentence = self.cnf.convert_sentence(test_sentence)
        self.assertEqual(result_sentence, expected_sentence)

    def test_convert_sentence_2(self):
        test_sentence = "Mother(m,c)&Sibling(c,d)=>Mother(m,d)"
        expected_sentence = "~Mother(m,c)|~Sibling(c,d)|Mother(m,d)"
        self.cnf = FolToCnfConverter()
        result_sentence = self.cnf.convert_sentence(test_sentence)
        self.assertEqual(result_sentence, expected_sentence)

if __name__ == '__main__':
    unittest.main()