import unittest
from Predicate import Predicate

class PredicateTest(unittest.TestCase):
    def setUp(self):
        self.p = None
    
    def test_not_negated_predicate(self):
        test_pred = "Brothers(John,x)"
        test_arguments = ["John", "x"]
        test_pred_name = "Brothers"

        self.p = Predicate(test_pred)
        self.assertEqual(test_pred, self.p.get_pred_str())
        self.assertEqual(test_arguments, self.p.get_arguments())
        self.assertEqual(test_pred_name, self.p.get_name())
        self.assertFalse(self.p.get_is_negative())

    def test_negated_predicate(self):
        test_pred = "~Brothers(John,x)"
        test_arguments = ["John", "x"]
        test_pred_name = "Brothers"

        self.p = Predicate(test_pred)
        self.assertEqual(test_pred, self.p.get_pred_str())
        self.assertEqual(test_arguments, self.p.get_arguments())
        self.assertEqual(test_pred_name, self.p.get_name())
        self.assertTrue(self.p.get_is_negative())

    def test_string_representation_not_negative(self):
        test_pred = "Brothers(John,x)"
        self.p = Predicate(test_pred)
        self.assertEqual(self.p.get_string(), test_pred)

    def test_string_representation_negative(self):
        test_pred = "~Brothers(John,x)"
        self.p = Predicate(test_pred)
        self.assertEqual(self.p.get_string(), test_pred)

    def test_negation_for_not_negative(self):
        test_pred = "Brothers(John, x)"
        self.p = Predicate(test_pred)
        self.p.negate()
        self.assertEqual(self.p.get_string(), "~" + test_pred)

    def test_negation_for_negative(self):
        test_pred = "~Brothers(John, x)"
        self.p = Predicate(test_pred)
        self.p.negate()
        self.assertEqual(self.p.get_string(), test_pred[1:])

    def test_unification_for_positive_preds(self):
        test_pred1 = "Brothers(John,x)"
        test_pred2 = "Brothers(John,Jim)"
        expected_sub = {"x": "Jim"}
        self.p = Predicate(test_pred1)
        p2 = Predicate(test_pred2)
        result_sub = self.p.unify_with_predicate(p2)
        self.assertEqual(expected_sub, result_sub)

    def test_impossible_unification_wrong_predicate(self):
        test_pred1 = "Brothers(John,x)"
        test_pred2 = "Father(John,Jim)"
        self.p = Predicate(test_pred1)
        p2 = Predicate(test_pred2)
        result_sub = self.p.unify_with_predicate(p2)
        self.assertFalse(result_sub)
    
    def test_impossible_unification_wrong_length(self):
        test_pred1 = "Brothers(John,x)"
        test_pred2 = "Brothers(John,Jim,Jack)"
        self.p = Predicate(test_pred1)
        p2 = Predicate(test_pred2)
        result_sub = self.p.unify_with_predicate(p2)
        self.assertFalse(result_sub)
    
    def test_impossible_unification_wrong_args(self):
        test_pred1 = "Train(Come,Hayley)"
        test_pred2 = "~Train(y,Ares)"
        self.p = Predicate(test_pred1)
        p2 = Predicate(test_pred2)
        result_sub = self.p.unify_with_predicate(p2)
        self.assertEqual(result_sub, False)

    def test_unification_for_negative_preds(self):
        test_pred1 = "~Brothers(John,x)"
        test_pred2 = "~Brothers(John,Jim)"
        expected_sub = {"x": "Jim"}
        self.p = Predicate(test_pred1)
        p2 = Predicate(test_pred2)
        result_sub = self.p.unify_with_predicate(p2)
        self.assertEqual(expected_sub, result_sub)

    def test_unification_for_multiple_preds(self):
        test_pred1 = "~Brothers(John,x,y,z)"
        test_pred2 = "~Brothers(John,Jim,Jack,Tom)"
        expected_sub = {"x": "Jim", "y": "Jack", "z": "Tom"}
        self.p = Predicate(test_pred1)
        p2 = Predicate(test_pred2)
        result_sub = self.p.unify_with_predicate(p2)
        self.assertEqual(expected_sub, result_sub)

    def test_substitution_for_positive_pred(self):
        test_pred1 = "Brothers(John,x)"
        sub = {"x": "Jim"}
        expected_pred1 = "Brothers(John,Jim)"

        self.p = Predicate(test_pred1)
        self.p.substitution(sub)
        self.assertEqual(self.p.get_string(), expected_pred1)

    def test_substitution_for_multiple_preds(self):
        test_pred1 = "~Brothers(John,x,y,z)"
        sub = {"x": "Jim", "y": "Jack", "z": "Tom"}
        expected_pred1 = "~Brothers(John,Jim,Jack,Tom)"

        self.p = Predicate(test_pred1)
        self.p.substitution(sub)
        self.assertEqual(self.p.get_string(), expected_pred1)


if __name__ == '__main__':
    unittest.main()