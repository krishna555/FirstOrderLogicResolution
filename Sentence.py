from Predicate import Predicate
import constant
import copy

class Sentence:
    """
        2 Properties for every sentence:
        1. Set of all Predicate objects.
        2. String representation of the Sentence.
    """
    def __init__(self, sentence=None):
        if sentence:
            predicates = sentence.split(constant.OR)
            self.predicates = set()
            for predicate in predicates:
                self.predicates.add(Predicate(predicate))
            self.sentence_str = sentence
        else:
            self.predicates = None
            self.sentence_str = None

    def get_predicates(self):
        return self.predicates
    
    def get_sentence_str(self):
        return self.sentence_str

    def add_to_KB(self, kb, kb_hashed):
        """Add the current sentence to a KB and its hash too.

        Args:
            kb (set): Set of sentences
            kb_hashed (dict): Dictionary with predicate as the key and set of sentences as value.
        """
        kb.add(self)
        for predicate in self.predicates:
            predicate_name = predicate.get_name()
            if predicate_name in kb_hashed:
                kb_hashed[predicate_name].add(self)
            else:
                kb_hashed[predicate_name] = set([self])

    def init_from_predicates(self, predicates):
        """Initialize Sentences from Predicates

        Args:
            predicates : List of Predicate class objects
        """
        self.predicates = predicates
        sentences = set()
        for predicate in predicates:
            sentences.add(predicate.get_pred_str())
        self.sentence_str = '|'.join(sentences)

    def is_only_constant_args(self, predicate):
        """Check if there are only constants in the arguments for the predicate

        Args:
            predicate (Object): Predicate Class Object
        """
        args = predicate.get_arguments()

        for arg in args:
            if not (arg and arg[0].isupper()):
                return False
        return True
        
    def get_result_from_unification(self, all_unifications, sentence2, removed_predicates):
        """We will substitute the variables in the original sentence and sentence2.
        Finally, we will select only those substituted predicates that do not have an instance in the other sentence.

        Args:
            all_unifications (dict): Dictionary of all possible unifications
            sentence2 (object): Object of sentence class
            removed_predicates (set): Set of all predicates removed via unification.
        """
        deep_copy_self_predicates = copy.deepcopy(self.predicates)
        deep_copy_sentence_predicates = copy.deepcopy(sentence2.predicates)
        all_predicates = []
        for predicate in deep_copy_self_predicates:
            if predicate.get_pred_str() in removed_predicates:
                removed_predicates.remove(predicate.get_pred_str())
                continue
            # Do all unifications.
            predicate.substitution(all_unifications)
            all_predicates.append(predicate)

        for predicate in deep_copy_sentence_predicates:
            if predicate.get_pred_str() in removed_predicates:
                continue
            predicate.substitution(all_unifications)
            all_predicates.append(predicate)
        return all_predicates

    def resolve(self, sentence):
        """
            Resolve 2 sentences
            1. Return False when a contradiction is inferred.
            2. Return Inferred statements otherwise

        Args:
            sentence (object): Sentence Object with which resolution must happen
        """
        inferred = set()

        all_unifications = {}
        removed_predicates = set()
        for predicate_1 in self.predicates:
            for predicate_2 in sentence.predicates:
                unification = False
                if (predicate_1.is_negative ^ predicate_2.is_negative) and \
                    (predicate_1.name == predicate_2.name):
                    unification = predicate_1.unify_with_predicate(predicate_2)
                if unification == False:
                    continue
                else:
                    unification_keys = set(unification.keys())
                    all_unifications_keys = set(all_unifications.keys())
                    if unification_keys and unification_keys.issubset(all_unifications_keys):
                        continue

                    all_unifications.update(unification)
                    removed_predicates.add(predicate_1.get_pred_str())
                    removed_predicates.add(predicate_2.get_pred_str())
                    break

        if not removed_predicates:
            # No new inferred sentences. No resolution happened.
            return None
        new_sentence = Sentence()
        resolved_predicates = self.get_result_from_unification(all_unifications, sentence, removed_predicates)
        if len(resolved_predicates) == 0:
            return False
        new_sentence.init_from_predicates(resolved_predicates)

        return new_sentence
    
    def get_sentences_in_kb(self, kb_hashed):
        """ Get statements with which the current sentence may resolve.

        Args:
            kb_hashed (dict): Dictionary of predicate key to sentences where in the predicate occurs. 

        Returns:
            set: set of sentences where in the predicate occurs in KB.
        """
        sentences = set()
        for predicate in self.predicates:
            if predicate.get_name() in kb_hashed:
                sentences = sentences.union(kb_hashed[predicate.get_name()])
        return sentences