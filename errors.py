class NoOperatorFoundError(Exception):
    def __init__(self):
        self.message = "Input is just number, no operation to perform"
        super().__init__(self.message)

class MissingOperandError(Exception):
    def __init__(self, a, b ):
        self.message = f"Missing operand between '{a}' and '{b}" 
        super().__init__(self.message)
