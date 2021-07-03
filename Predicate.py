import constant
class Predicate:
    """
        Define a predicate to have the following properties:
        1. name: Name of the predicate
        2. pred_str: String representation of the original Predicate
        3. is_negative: Is the predicate negated
        4. arguments: Arguments supplied to the predicate upon creation.

    Note: When Sentences are passed here it should not have spaces/tabs etc 
        Brothers(John,Jim) is valid.
        Brothers(John, Jim) is not valid.
    """

    def __init__(self, predicate):
        """
        Expected Predicate Form: Brothers(x, John)

        Args:
            predicate (string): String representing the predicate.
        """
        split_args_from_pred = predicate.split("(")
        self.is_negative = False
        self.name = split_args_from_pred[0]
        self.pred_str = predicate

        if self.name and self.name[0] == constant.NOT_OP:
            self.is_negative = True
            self.name = self.name[1:]

        eliminate_closing = split_args_from_pred[1][:-1]
        self.arguments = eliminate_closing.split(",")
    
    def get_name(self):
        return self.name
    
    def get_pred_str(self):
        return self.pred_str
    
    def get_is_negative(self):
        return self.is_negative

    def get_arguments(self):
        return self.arguments

    def get_string(self):
        return (constant.NOT_OP * self.is_negative) + self.name + "(" + ','.join(self.arguments) + ')'

    def set_arguments(self, arguments):
        """Can be used to set new arguments to the Predicate

        Args:
            arguments (list): List of Strings corresponding to the arguments of the Predicate.
        """
        self.arguments = arguments
        self.update_pred_str()

    def negate(self):
        """Negate the Predicate String
        """
        self.is_negative = not self.is_negative
        self.update_pred_str()
    
    def update_pred_str(self):
        self.pred_str = (constant.NOT_OP * self.is_negative) + self.name + "(" + ','.join(self.arguments) + ')'
    
    def unify_with_predicate(self, predicate):
        """
            Return a substitution if unification is possible otherwise return False
        Args:
            predicate (Object): Object of class Predicate with which unification must be done.
        """
        if self.name == predicate.get_name() and len(self.arguments) == len(predicate.get_arguments()):
            sub = {}
            return self.unify(self.arguments, predicate.get_arguments(), sub)
        else:
            return False

    def unify(self, pred1_args, pred2_args, sub):
        """
        Unify 2 predicates and return a valid substitution.

        Args:
            self: Self variable needed for unit tests.
            pred1_args (string): Current Predicate Arguments.
            pred2_args (string): The other Predicate Arguments
            sub (dict): Dictionary of a valid substitution
        """
        if sub == False:
            return False
        elif pred1_args == pred2_args:
            return sub
        elif isinstance(pred1_args, str) and pred1_args.islower():
            return self.unify_var(pred1_args, pred2_args, sub)
        elif isinstance(pred2_args, str) and pred2_args.islower():
            return self.unify_var(pred2_args, pred1_args, sub)
        elif isinstance(pred1_args, list) and isinstance(pred2_args, list):
            if pred1_args and pred2_args:
                return self.unify(pred1_args[1:], pred2_args[1:], self.unify(pred1_args[0], pred2_args[0], sub))
            else:
                return sub
        else:
            return False
        
    def unify_var(self, var, x, sub):
        if var in sub:
            return self.unify(sub[var], x, sub)
        elif x in sub:
            return self.unify(var, sub[x], sub)
        else:
            sub[var] = x
            return sub
    
    def substitution(self, sub):
        """Method to substitute arguments with the values in substitution object "sub"

        Args:
            sub (dict): A valid substitution.
        """

        if sub:
            for ind, arg in enumerate(self.arguments):
                if arg in sub:
                    self.arguments[ind] = sub[arg]
            self.update_pred_str()
        return self