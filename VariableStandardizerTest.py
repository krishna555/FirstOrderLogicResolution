import unittest
from variableStandardizer import VariableStandardizer
from Predicate import Predicate

class VariableStandardizerTest(unittest.TestCase):
    def setUp(self):
        self.vs = None

    def test_standardization_cnf_1(self):
        test_sentence =  "~A(x)|B(x)"
        expected_sentence = "~A(x_1)|B(x_1)"
        self.vs = VariableStandardizer()

        self.assertEqual(self.vs.standardize(test_sentence), expected_sentence)

    def test_standardization_cnf_multiple(self):
        kb_sentence_1 =  "~A(x)|B(x)"
        kb_sentence_2 =  "~A(x)|B(x)"
        kb_sentence_3 =  "~A(x)|B(x)"
        kb_sentence_4 =  "~A(x)|B(x)"
        kb_sentence_5 =  "~A(x)|B(x)"
        kb_sentence_6 =  "~A(x)|B(x)"
        kb_sentence_7 =  "~A(x)|B(x)"
        self.vs = VariableStandardizer()
        self.vs.standardize(kb_sentence_1)
        self.vs.standardize(kb_sentence_2)
        self.vs.standardize(kb_sentence_3)
        self.vs.standardize(kb_sentence_4)
        self.vs.standardize(kb_sentence_5)
        self.vs.standardize(kb_sentence_6)
        self.vs.standardize(kb_sentence_7)

        test_sentence = "~A(x)|C(y)|B(z)"
        expected_sentence = "~A(x_8)|C(y_1)|B(z_1)"
        test_result = self.vs.standardize(test_sentence)

        self.assertEqual(test_result, expected_sentence)

if __name__ == '__main__':
    unittest.main()