from dragnote.domain import Harmony


class Compare:
    def __init__(self, left: Harmony, right: Harmony):
        self.left = left
        self.right = right

    def is_equal(self) -> bool:
        return self.left == self.right
