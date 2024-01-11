class NoOperatorFoundError(Exception):
    def __init__(self):
        super().__init__("Input is just number, no operation to perform")
        
