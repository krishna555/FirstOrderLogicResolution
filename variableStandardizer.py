from collections import defaultdict
import constant
from Predicate import Predicate
class VariableStandardizer:
    def __init__(self):
        self.variable_dict = defaultdict(int)
    
    def standardize(self, sentence: str) -> None:
        """Replace sentence variables with standardized Representation

        Args:
            sentence (str): CNF Sentence
        """
        predicate_arr = sentence.split(constant.OR)
        lowercase_args = []
        predicates = []
        for predicate in predicate_arr:
            predicate_obj = Predicate(predicate)
            predicates.append(predicate_obj)
            predicate_args = predicate_obj.get_arguments()
            for arg in predicate_args:
                if arg and arg[0].islower():
                    lowercase_args.append(arg)
        
        standard_variable_map = {}
        for arg in lowercase_args:
            if arg not in standard_variable_map:
                self.variable_dict[arg] += 1
            standard_variable_map[arg] = arg + "_" + str(self.variable_dict[arg])
        
        for predicate in predicates:
            predicate_args = predicate.get_arguments()
            argument_list = []
            for arg in predicate_args:
                if arg not in standard_variable_map:
                    argument_list.append(arg)
                else:
                    argument_list.append(standard_variable_map[arg])
            predicate.set_arguments(argument_list)

        return constant.OR.join([predicate_obj.pred_str for predicate_obj in predicates])