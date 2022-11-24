from utils import brand_names


class Leaf:
    # A Leaf node classifies data.

    def __init__(self, rows):
        self.predictions = brand_names(rows)
