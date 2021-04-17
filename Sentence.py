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
        
    def resolve(self, sentence):
        """
            Resolve 2 sentences
            1. Return False when a contradiction is inferred.
            2. Return Inferred statements otherwise

        Args:
            sentence (object): Sentence Object with which resolution must happen
        """
        inferred = set()
        for predicate_1 in self.predicates:
            for predicate_2 in sentence.predicates:
                unification = False
                if (predicate_1.is_negative ^ predicate_2.is_negative) and \
                    (predicate_1.name == predicate_2.name):
                    unification = predicate_1.unify_with_predicate(predicate_2)
                if unification == False:
                    continue
                else:
                    # rest_predicates_sentence_1 = list(filter(lambda y: False if y == predicate_1 else True, self.predicates))
                    rest_predicates_sentence_1 = []
                    rest_predicates_sentence_2 = []
                    for predicate in self.predicates:
                        if predicate.get_pred_str() != predicate_1.get_pred_str():
                            rest_predicates_sentence_1.append(predicate)
                    
                    for predicate in sentence.predicates:
                        if predicate.get_pred_str() != predicate_2.get_pred_str():
                            rest_predicates_sentence_2.append(predicate)
                    # rest_predicates_sentence_2 = list(filter(lambda y: False if y == predicate_2 else True, sentence.predicates))
                    if not rest_predicates_sentence_1 and not rest_predicates_sentence_2:
                        # print(self.get_sentence_str())
                        # print(sentence.sentence_str)
                        return False
                    other_predicates = []
                    for predicate in rest_predicates_sentence_1:
                        # Do Deep copy here because otherwise u will mutate the original Predicate object.
                        # We want to add new sentences that are inferred not mutate existing ones.
                        deep_copy_predicate = copy.deepcopy(predicate)
                        other_predicates.append(deep_copy_predicate.substitution(unification))
                    for predicate in rest_predicates_sentence_2:
                        deep_copy_predicate = copy.deepcopy(predicate)
                        other_predicates.append(deep_copy_predicate.substitution(unification))
                    new_sentence = Sentence()
                    new_sentence.init_from_predicates(set(other_predicates))
                    inferred.add(new_sentence)
        return inferred
    
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