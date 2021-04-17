import os
from FolToCnfConverter import FolToCnfConverter
from Sentence import Sentence
from FOLResolver import FOLResolver
from Predicate import Predicate
import constant
import copy
import time

class Homework:
    def __init__(self):
        self.num_queries = None
        self.queries = None
        self.num_kb_sentences = None
        self.sentences = None
        self.kb = set()
        self.kb_hash = {}

    def remove_spaces(self, sentence: str):
        """Remove all spaces to make further processing easy.

        Args:
            sentence (str): Either a query or sentence in KB.
        """
        return sentence.rstrip().replace(' ', '').replace('\t', '')

    def setup_inputs(self):
        input_path = os.path.join(os.getcwd(), 'input.txt')
        with open(input_path, 'r') as f:
            self.num_queries = int(f.readline().rstrip())
            self.queries = []
            self.sentences = []
            self.kb_sentences = set()
            for i in range(self.num_queries):
                query = f.readline().rstrip()
                query = self.remove_spaces(query)
                self.queries.append(Predicate(query))
            self.num_kb_sentences = int(f.readline().rstrip())
            for i in range(self.num_kb_sentences):
                kb_sentence = f.readline().rstrip()
                kb_sentence = self.remove_spaces(kb_sentence)
                self.sentences.append(kb_sentence)

    def make_kb(self):
        fol_to_cnf_obj = FolToCnfConverter()
        for sentence in self.sentences:
            cnf_sentence = fol_to_cnf_obj.convert_sentence(sentence)
            sentence_obj = Sentence(cnf_sentence)
            sentence_obj.add_to_KB(self.kb, self.kb_hash)
    
    def run_queries(self):
        results = []
        for query_predicate_obj in self.queries:
            fol_resolver = FOLResolver()
            query_predicate_obj.negate()
            query_sentence = Sentence(query_predicate_obj.get_pred_str())
            query_args = query_predicate_obj.get_arguments()
            kb = copy.deepcopy(self.kb)
            kb_hash = copy.deepcopy(self.kb_hash)
            result = fol_resolver.resolve(kb, kb_hash, query_sentence)
            if result:
                results.append("TRUE")
            else:
                results.append("FALSE")
        ofp = open("output.txt","w")
        ofp.writelines("\n".join(results))
        ofp.close()

def main():
    start_time = time.time()
    h = Homework()
    h.setup_inputs()
    h.make_kb()
    h.run_queries()
    end_time = time.time()
    print(" Time for execution : ", end_time - start_time)

if __name__ == "__main__":
    main()