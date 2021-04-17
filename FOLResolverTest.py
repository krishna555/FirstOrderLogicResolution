from FOLResolver import FOLResolver
from Predicate import Predicate
from Sentence import Sentence
import unittest
class FOLResolverTest(unittest.TestCase):
    def setUp(self):
        self.fol_resolver = None
    
    def test_any_predicate_with_constants_true(self):
        predicate_str = "A(Bob)"
        sentence = Sentence(predicate_str)
        self.fol_resolver = FOLResolver()
        self.assertTrue(self.fol_resolver.any_predicate_with_constants(sentence))

    def test_any_predicate_with_constants_false(self):
        predicate_str = "A(x)"
        sentence = Sentence(predicate_str)
        self.fol_resolver = FOLResolver()
        self.assertFalse(self.fol_resolver.any_predicate_with_constants(sentence))

    def test_simple_contradiction(self):
        query = "A(Bob)"
        predicate_1_str = "~A(x)"
        predicate_1_obj = Predicate(predicate_1_str)
        sentence = Sentence(predicate_1_str)
        kb = set([sentence])
        kb_hashed = {}
        kb_hashed[predicate_1_obj.get_name()] = set([sentence])
        query_sentence = Sentence(query)

        self.fol_resolver = FOLResolver()
        self.assertTrue(self.fol_resolver.resolve(kb, kb_hashed, query_sentence))

    def test_cyclic_kb_no_contradiction(self):
        query = "A(Bob)"
        predicate_1_str = "~A(x)|B(x)"
        predicate_2_str = "~B(x)|A(x)"
        predicate_1_obj = Predicate(predicate_1_str)
        predicate_2_obj = Predicate(predicate_2_str)
        sentence_1 = Sentence(predicate_1_str)
        sentence_2 = Sentence(predicate_2_str)
        kb = set([sentence_1, sentence_2])
        kb_hashed = {}
        kb_hashed[predicate_1_obj.get_name()] = set([sentence_1, sentence_2])
        query_sentence = Sentence(query)
        
        self.fol_resolver = FOLResolver()
        self.assertFalse(self.fol_resolver.resolve(kb, kb_hashed, query_sentence))
if __name__ == '__main__':
    unittest.main()