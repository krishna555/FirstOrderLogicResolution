from FOLResolverBeta import FOLResolverBeta
from Predicate import Predicate
from Sentence import Sentence
import unittest
class FOLResolverTest(unittest.TestCase):
    def setUp(self):
        self.fol_resolver = None

    def test_simple_contradiction(self):
        query = "A(Bob)"
        predicate_1_str = "~A(x)"
        predicate_1_obj = Predicate(predicate_1_str)
        sentence = Sentence(predicate_1_str)
        kb = set([sentence])
        kb_hashed = {}
        kb_hashed["~" + predicate_1_obj.get_name()] = set([sentence])
        query_sentence = Sentence(query)

        self.fol_resolver = FOLResolverBeta()
        self.assertTrue(self.fol_resolver.resolve_beta(kb, kb_hashed, query_sentence))

    def test_cyclic_kb_no_contradiction(self):
        query = "A(Bob)"
        sentence_1_str = "~A(x)|B(x)"
        sentence_2_str = "~B(x)|A(x)"
        predicate_1_obj = Predicate(sentence_1_str)
        predicate_2_obj = Predicate(sentence_2_str)
        sentence_1 = Sentence(sentence_1_str)
        sentence_2 = Sentence(sentence_2_str)
        kb = set()
        kb_hashed = {}
        sentence_1.add_to_KB(kb, kb_hashed)
        sentence_2.add_to_KB(kb, kb_hashed)
        query_sentence = Sentence(query)
        
        self.fol_resolver = FOLResolverBeta()
        self.assertFalse(self.fol_resolver.resolve_beta(kb, kb_hashed, query_sentence))


if __name__ == '__main__':
    unittest.main()