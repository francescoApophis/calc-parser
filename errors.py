from typing import Union



class Err:
    def __init__(self, msg: str) -> None:
        self.msg = msg
        self.report()
    def report(self):
        print('ERROR:', self.msg)
        exit(1)

class NotEnoughErr(Err):
    def __init__(self, what:str, idx:Union[int, None] = None, expr:Union[str, None] = None) -> None:
        arrow = " " * (idx + 1) + "^" if idx is not None else ""
        location = f"at index: {idx}\n'{expr}'\n{arrow}" if idx is not None else ""

        self.msg = f"Not enough {what} " + location
        super().__init__(self.msg)

class NotImplementedErr(Err):
    def __init__(self, what:str) -> None:
        self.msg = f"{what.capitalize()} not implemented yet"
        super().__init__(self.msg)

class NotSupportedErr(Err):
    def __init__(self, what: str) -> None:
        self.msg = f"{what.capitalize()} not supported"
        super().__init__(self.msg)

class InvalidSymErr(Err):
    def __init__(self, what: str, idx:int, expr: str) -> None:
        arrow = " " * (idx + 1) + "^"
        self.msg = f"Invalid symbol '{what}' at index: {idx}\n'{expr}'\n{arrow}"
        super().__init__(self.msg)

class ParenthesesErr(Err):
    def __init__(self, what:str, idx:int, expr: str) -> None:
        arrow = " " * (idx + 1) + "^"
        self.msg = f"No {what} between parentheses at index: {idx}\n'{expr}'\n{arrow}"
        super().__init__(self.msg)

class MismatchedParenthesesErr(Err):
    def __init__(self, parenthesis: str, amount:int) -> None:
        self.msg = f"Mismatched parenthesis, {amount} missing '{parenthesis}' parenthesis"
        super().__init__(self.msg)




