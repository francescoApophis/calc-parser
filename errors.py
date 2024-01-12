class NoOperatorFoundError(Exception):
    def __init__(self):
        self.message = "Input is just number, no operation to perform"
        super().__init__(self.message)

class MissingOperandError(Exception):
    def __init__(self, idx, a = None, b = None):
        empty = ""
        # a/b are none if except occurred at either start or end of str
        self.message = f"Missing operand between '{empty if a is None else a}' and '{empty if b is None else b}' at index {idx}" 
        super().__init__(self.message)

class EmptyParenthesisError(Exception):
    def __init__(self, idx):
        self.message = f"Empty parenthesis at index '{idx}'" 
        super().__init__(self.message)

class  OppositeParenthesisError(Exception):
    def __init__(self, idx):
        self.message = f"Opposite parenthesis with no operator between at index '{idx}'" 
        super().__init__(self.message)


class MismatchedParenthesisError(Exception):
    def __init__(self, a, b):
        type_par = "(" if a > b else ")"
        excess_par = a-b if a > b else b - a
        self.message = f"Mismatched parenthesis: {excess_par} too many '{type_par}' parenthesis" 
        super().__init__(self.message)

