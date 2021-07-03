import unittest
from Sentence import Sentence
from Predicate import Predicate
from collections import defaultdict

class SentenceTest(unittest.TestCase):
    def setUp(self):
        self.s = None
    
    # @unittest.skip
    def test_add_to_kb(self):
        
        # Setup KB, KB_Hashed
        predicate = "Brothers(John,x)"
        predicate_obj = Predicate(predicate)
        placeholder_sentence = Sentence(predicate)
        kb = set([placeholder_sentence])
        kb_hashed = {}
        kb_hashed[predicate_obj.get_name()] = set([Sentence(predicate)])

        cnf_sentence = "Man(Jack)"
        cnf_sentence_name = cnf_sentence.split("(")[0]
        self.s = Sentence(cnf_sentence)
        self.s.add_to_KB(kb, kb_hashed)

        self.assertTrue(self.s in kb_hashed[cnf_sentence_name])
        self.assertTrue(self.s in kb)

    # @unittest.skip
    def test_init_from_predicates(self):
        # Setup 2 Predicates
        predicate_1 = "Brothers(John,x)"
        predicate_obj_1 = Predicate(predicate_1)
        predicate_2 = "Man(John)"
        predicate_obj_2 = Predicate(predicate_2)
        predicates_list = [predicate_obj_1, predicate_obj_2]

        s3 = Sentence()
        s3.init_from_predicates(predicates_list)

        exp_1 = predicate_1 + "|" + predicate_2
        exp_2 = predicate_2 + "|" + predicate_1
        test_result = s3.get_sentence_str()
        
        self.assertTrue((test_result == exp_1) or (test_result == exp_2))
    
    # @unittest.skip
    def test_simple_resolution(self):
        new_sentence = "A(Bob)"
        new_sent_obj = Sentence(new_sentence)
        test_sentence = "~A(x)|B(x,y)"
        expected_inference = "B(Bob,y)"

        self.s = Sentence(test_sentence)
        inferred_sentences = self.s.resolve(new_sent_obj)
        test_result = None
        for sentence in inferred_sentences:
            test_result = sentence
        self.assertTrue(test_result.sentence_str == expected_inference)

    # @unittest.skip
    def test_inference_self(self):
        new_sentence = "T(C)"
        new_sent_obj = Sentence(new_sentence)
        test_sentence = "~T(x)|T(C)"
        expected_inference = "T(C)"

        self.s = Sentence(test_sentence)
        inferred = self.s.resolve(new_sent_obj)
        test_result = None
        for sentence in inferred:
            test_result = sentence
        self.assertTrue(test_result.sentence_str == expected_inference)

    def test_inference_no_more_pending_subs_beta(self):
        new_sentence = "A(Bob)"
        new_sentence_obj = Sentence(new_sentence)
        test_sentence = "~A(Bob)|B(C)"
        expected_sentence = "B(C)"

        self.s = Sentence(test_sentence)
        inferred = self.s.resolve_beta(new_sentence_obj)
        self.assertEqual(inferred.sentence_str, expected_sentence)

    # @unittest.skip
    def test_inference_substitution_does_not_matter(self):
        new_sentence = "A(x)"
        new_sentence_obj = Sentence(new_sentence)
        test_sentence = "~A(x)|B(C)"
        expected_sentence = "B(C)"

        self.s = Sentence(test_sentence)
        inferred_sentences = self.s.resolve(new_sentence_obj)
        test_result = None
        for sentence in inferred_sentences:
            test_result = sentence
        self.assertEqual(test_result.sentence_str, expected_sentence)

    # def test_sample_substitution(self):
    #     """A(x) ^ B(y) => C(z)
    #     ~A(x) v ~B(y) v C(z)
    #     C(Bob) ^ A(z) => B(x)
    #     ~C(Bob) v ~A(z) v B(x)
    #     """
    #     new_sentence = "~A(x)|~B(y)|C(z)"
    #     new_sentence_obj = Sentence(new_sentence)
    #     test_sentence = "~C(Bob)|~A(z)|B(x)"
    #     expected_sentence = "B(C)"

    #     self.s = Sentence(test_sentence)
    #     inferred = self.s.resolve(new_sentence_obj)
    #     print(inferred.sentence_str)
    #     self.assertEqual(True, True)

    # @unittest.skip
    def test_inference_substitution_does_not_matter2(self):
        new_sentence = "~AB(x,y,z,t)|BB(SE)"
        new_sentence_obj = Sentence(new_sentence)
        test_sentence = "AB(y2,y2,S,S)"
        expected_sentence = "BB(SE)"

        self.s = Sentence(test_sentence)
        inferred = self.s.resolve(new_sentence_obj)
        test_result = None
        for sentence in inferred:
            test_result = sentence
        self.assertEqual(test_result.sentence_str, expected_sentence)

    # @unittest.skip
    def test_simple_resolution2(self):
        new_sentence = "~Ready(Hayley)|~Ready(Teddy)"
        new_sent_obj = Sentence(new_sentence)
        test_sentence = "Ready(Hayley)"
        expected_inference = "~Ready(Teddy)"

        self.s = Sentence(test_sentence)
        inferred = self.s.resolve(new_sent_obj)
        test_result = None
        for sentence in inferred:
            test_result = sentence            
        self.assertTrue(test_result.get_sentence_str() == expected_inference)

    def test_simple_resolution3(self):
        new_sentence = "~Take(x_4,JediPill)|Take(x_4,AntiSith)"
        new_sent_obj = Sentence(new_sentence)
        test_sentence = "Take(Bob,JediPill)"
        expected_inference = "Take(Bob,AntiSith)"

        self.s = Sentence(test_sentence)
        inferred = self.s.resolve_beta(new_sent_obj)
        print(inferred.sentence_str)     
        self.assertTrue(inferred.get_sentence_str() == expected_inference)

    # @unittest.skip
    def test_no_unification_resolution(self):
        new_sentence = "A(Bob)"
        new_sent_obj = Sentence(new_sentence)
        test_sentence = "~C(x)|B(x,y)"

        s1 = Sentence(test_sentence)
        inferred = s1.resolve(new_sent_obj)
        self.assertTrue(len(inferred) == 0)

    # @unittest.skip
    # def test_multiple_unifications_single_variable(self):
    #     new_sentence = "~Start(Hayley)|~Start(Teddy)|~Healthy(Hayley)"
    #     new_sent_obj = Sentence(new_sentence)
    #     test_sentence = "~Vaccinated(x)|Start(x)"
    #     expected_sentence = "~Healthy(Hayley)|~Start(Teddy)|~Vaccinated(Hayley)"
    #     s2 = Sentence(test_sentence)
    #     inferred = new_sent_obj.resolve(s2)
    #     print(inferred.sentence_str)
    #     self.assertTrue(expected_sentence == inferred.get_sentence_str)

    # @unittest.skip
    def test_contradiction_resolution(self):
        new_sentence="A(Bob)"
        test_sentence="~A(x)"
        new_sent_obj = Sentence(new_sentence)

        s2 = Sentence(test_sentence)
        inferred = s2.resolve(new_sent_obj)
        self.assertFalse(inferred)

    def test_simple_standardized_resolution(self):
        new_sentence="~T(Kim)"
        test_sentence="T(x_1)|~P(u_1)"
        new_sent_obj = Sentence(new_sentence)
        expected_sentence = "~P(u_1)"
        s2 = Sentence(test_sentence)
        inferred = s2.resolve(new_sent_obj)
        result = None
        for x in inferred:
            result = x.sentence_str
        self.assertEqual(result,expected_sentence)

    def test_contradiction_resolution2_beta(self):
        new_sentence="~Learn(Come,Hayley)|~Train(Come,Hayley)|~Healthy(Hayley)"
        test_sentence="Healthy(Hayley)"
        new_sent_obj = Sentence(new_sentence)

        s2 = Sentence(test_sentence)
        inferred = s2.resolve_beta(new_sent_obj)
        print(inferred.sentence_str)
        self.assertTrue(inferred.sentence_str)

    def test_contradiction_resolution_double_preds_beta(self):
        new_sentence="~A(Bob)|~B(Bob)"
        test_sentence="A(x)|B(x)"
        new_sent_obj = Sentence(new_sentence)
        expected_sentence = "~A(Bob)|A(Bob)"
        s2 = Sentence(test_sentence)
        inferred = s2.resolve_beta(new_sent_obj)
        self.assertTrue(inferred.sentence_str)


    # @unittest.skip
    def test_get_from_kb_relevant_sentences(self):
        # Setup KB, KB_Hashed
        predicate_1 = "A(John,x)"
        predicate_1_obj = Predicate(predicate_1)
        predicate_2 = "~C(y)"
        predicate_2_obj = Predicate(predicate_2)
        predicate_3 = "~C(John)"
        predicate_3_obj = Predicate(predicate_3)

        kb_hashed = {}
        kb_hashed[predicate_1_obj.get_name()] = set([Sentence(predicate_1)])

        # Predicate 2 and 3 share the same name "C"
        kb_hashed["~" + predicate_2_obj.get_name()] = set([Sentence(predicate_2)])
        kb_hashed["~" + predicate_3_obj.get_name()].add(Sentence(predicate_3))

        test_sentence = "C(x)"
        self.s = Sentence(test_sentence)
        related_sentences = self.s.get_sentences_in_kb(kb_hashed)
        result = set()
        for sentence in related_sentences:
            result.add(sentence.sentence_str)
        self.assertTrue(result == set([predicate_2, predicate_3]))

    def test_factor_sentence(self):
        test_sentence = "P(u)|P(v)|T(z)"
        self.s = Sentence(test_sentence)
        self.s.factor_sentence()
        expected_res = ["P(u)|T(z)", "P(v)|T(z)", "T(z)|P(u)", "T(z)|P(v)"]
        self.assertTrue(self.s.sentence_str in expected_res)

    def test_factor_sentence_2(self):
        test_sentence = "~Parent(x,p)|~Parent(x,w)|~Parent(a,b)|~Parent(c,d)|Sibling(p,w)"
        self.s = Sentence(test_sentence)
        self.s.factor_sentence()
        print(self.s.sentence_str)
        expected_res = ["P(u)|T(z)", "P(v)|T(z)", "T(z)|P(u)", "T(z)|P(v)"]
        self.assertTrue(True)

    def test_remove_from_kb(self):
        # Setup KB, KB_Hashed
        predicate = "Brothers(John,x)"
        predicate_obj = Predicate(predicate)
        placeholder_sentence = Sentence(predicate)
        kb = set([placeholder_sentence])
        kb_hashed = {}
        kb_hashed[predicate_obj.get_name()] = set([Sentence(predicate)])

        cnf_sentence = "Man(Jack)"
        cnf_sentence_name = cnf_sentence.split("(")[0]
        self.s = Sentence(cnf_sentence)
        self.s.add_to_KB(kb, kb_hashed)

        self.s.remove_from_kb(kb, kb_hashed)
        self.assertTrue(self.s not in kb_hashed[cnf_sentence_name])
        self.assertTrue(self.s not in kb)
if __name__ == '__main__':
    unittest.main()