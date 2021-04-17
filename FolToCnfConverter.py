import constant
from Predicate import Predicate
class FolToCnfConverter:
    def convert_sentence(self, sentence: str):
        """Convert a FOL sentence to its cnf equivalent.

        Args:
            sentence (str): FOL of the form p1 & p2 & .... pn => q where p[i] and q are atomic sentences.
        """
        sentence_parts = sentence.split(constant.IMPLICATION)
        if len(sentence_parts) == 1:
            # Single Literal so nothing to do.
            return sentence

        antecedent = sentence_parts[0]
        consequent = sentence_parts[1]

        preds = antecedent.split(constant.AND)
        predicates = []
        for pred_str in preds:
            predicates.append(Predicate(pred_str))
        
        # Begin Conversion
        for predicate in predicates:
            predicate.negate()
        
        cnf_lhs = "|".join([x.get_pred_str() for x in predicates])
        cnf = cnf_lhs + "|" + consequent

        return cnf