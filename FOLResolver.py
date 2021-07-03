import constant
import os
from collections import defaultdict
class FOLResolver:

    def __init__(self):
        self.all_sentences = set()
        self.all_new_inferrences = []

    def get_all_new_inferrences(self):
        return self.all_new_inferrences

    def check_for_subset(self, new_sentences):
        """Check if the newly inferred sentences already exist in the KB.

        Args:
            new_sentence (list): List of newly inferred sentences from FOL Full resolution.
        """
        for sentence in new_sentences:
            if sentence.get_sentence_str() not in self.all_sentences:
                return False
        return True
    
    def get_newly_inferred_sentences(self, new_sentences):
        """
        Get list of sentences which was not in the original KB.
        Args:
            new_sentences (list): List of Sentence objects which was inferred by FOL Full Resolution Rule
        """
        new_inferred_sentences = []
        for sentence in new_sentences:
            if sentence.get_sentence_str() not in self.all_sentences:
                new_inferred_sentences.append(sentence)
                self.all_new_inferrences.append(sentence)
        return new_inferred_sentences

    def initialize_all_sentences(self, kb):
        """Initialize the all_sentences set with all sentences in KB.
        This will make lookup with the inferred sentences during resolution easy.

        Args:
            kb (set): Set of sentences in KB
        """
        for sentence in kb:
            self.all_sentences.add(sentence.get_sentence_str())

    def update_new_sentences(self, inferred_sentences, new_sentences):
        """
            Check if sentence was previously discovered, if not add it.
        Args:
            inferred_sentences (set): Set of inferred sentences from all possible unifications in current iteration.
            new_sentences (set): All new sentences ever discovered in current step.
        """
        for sentence in inferred_sentences:
            is_sentence_present = False
            for new_sentence in new_sentences:
                if sentence.get_sentence_str() == new_sentence.get_sentence_str():
                    is_sentence_present = True
                    break
            if not is_sentence_present:
                new_sentences.add(sentence)
        return new_sentences

    def resolve(self, kb, kb_hashed, query):
        """Perform Resolution for query in KB.

        Args:
            kb (set): Set of sentences in KB.
            kb_hashed (dict): Each predicate is mapped to a set of all sentences with the predicate. 
            query (object): Query a Sentence class Object
        """
        self.all_sentences.clear()
        query.add_to_KB(kb, kb_hashed)
        self.initialize_all_sentences(kb)
        while True:
            new_sentences = set()
            for sentence1 in kb:
                if len(sentence1.get_predicates()) > 1:
                    continue
                resolving_clauses = sentence1.get_sentences_in_kb(kb_hashed)
                for sentence2 in resolving_clauses:
                    if sentence1.get_sentence_str() == sentence2.get_sentence_str():
                        continue
                    inferred_sentences = sentence1.resolve(sentence2)
                    if inferred_sentences == False:
                        return True
                    new_sentences = self.update_new_sentences(inferred_sentences, new_sentences)

            if self.check_for_subset(new_sentences):
                return False
            new_inferrences = self.get_newly_inferred_sentences(new_sentences)
            for sentence in new_inferrences:
                sentence.add_to_KB(kb, kb_hashed)
                self.all_sentences.add(sentence.get_sentence_str())