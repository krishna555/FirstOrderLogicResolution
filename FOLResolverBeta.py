import constant
import os
from collections import defaultdict
from Sentence import Sentence
import copy
import time

class FOLResolverBeta:

    def __init__(self):
        self.all_sentences = set()

    def initialize_all_sentences(self, kb):
        """Initialize the all_sentences set with all sentences in KB.
        This will make lookup with the inferred sentences during resolution easy.

        Args:
            kb (set): Set of sentences in KB
        """
        for sentence in kb:
            self.all_sentences.add(sentence)

    def check_sentence_in_all_sentences(self, sentence):
        """Check if a sentence is in all_sentences list

        Args:
            sentence (Object): Object of Sentence Class.
        """

        for s1 in self.all_sentences:
            if s1.sentence_str == sentence.sentence_str:
                return True
        return False

    def is_sentence_True(self, sentence):
        predicates = sentence.get_predicates()
        predicates_arr = [(predicate.pred_str, predicate) for predicate in predicates]
        d = defaultdict(int)
        for predicate in predicates:
            d[predicate.pred_str] = 1
        removed_predicates = set()
        for (predicate_str, predicate) in predicates_arr:
            is_negative = predicate.is_negative
            opposite_sign = "" if is_negative else "~"
            abs_pred_str = predicate_str.replace("~", "")
            opposite_predicate = opposite_sign + abs_pred_str
            if opposite_predicate in d:
                return True
        return False

    def dfs(self, kb, kb_hashed, curr_sentence, level):
        if time.time() - self.start_time >= 10:
            return False
        resolving_sentences = curr_sentence.get_sentences_in_kb(kb_hashed)
        resolving_sentences_ordered = [(len(x.get_predicates()), x) for x in resolving_sentences]
        resolving_sentences_ordered = sorted(resolving_sentences_ordered, key=lambda x: x[0])

        for sentence_tup in resolving_sentences_ordered:
            if time.time() - self.start_time >= 10:
                return False
            sent_len, sentence = sentence_tup
            if curr_sentence.sentence_str == sentence.sentence_str:
                continue
            inferred = curr_sentence.resolve_beta(sentence)
            if inferred == False:
                return True
            if inferred is not None:
                inferred.factor_sentence()
                if self.is_sentence_True(inferred):
                    continue
                if len(inferred.get_predicates()) == 0:
                    continue
                if self.check_sentence_in_all_sentences(inferred):
                    continue
                inferred.add_to_KB(kb, kb_hashed)
                self.all_sentences.add(inferred)
                res = self.dfs(kb, kb_hashed, inferred, level + 1)
                inferred.remove_from_kb(kb, kb_hashed)
                self.all_sentences.remove(inferred)
                if time.time() - self.start_time >= 10:
                    return False
                if res:
                    return True
        return False

    def resolve_beta(self, kb, kb_hashed, query):
        """Perform Resolution for query in KB.

        Args:
            kb (set): Set of sentences in KB.
            kb_hashed (dict): Each predicate is mapped to a set of all sentences with the predicate. 
            query (object): Query a Sentence class Object
        """
        self.start_time = time.time()
        self.all_sentences.clear()
        query.add_to_KB(kb, kb_hashed)
        self.initialize_all_sentences(kb)

        for sentence in kb:
            if time.time() - self.start_time >= 10:
                return False
            kb2 = copy.deepcopy(kb)
            kb_hashed2 = copy.deepcopy(kb_hashed)
            self.all_sentences.clear()
            self.initialize_all_sentences(kb2)
            res = self.dfs(kb2, kb_hashed2, sentence, 0)
            if res == True:
                return res
        return False