
def random_matrix(rows=4, cols=4, min_value=1, max_value=9)->list:
    """
    Returns a matrix of random values.
    """
    import random
    return [[random.randint(min_value, max_value) for _ in range(cols)] for _ in range(rows)]

class Random:
  def __init__(self, rows=4, columns=4, max_value=9, min_value=1) -> None:
    self.rows = rows
    self.columns = columns
    self.max_value = max_value
    self.min_value = min_value
    self.matrix = random_matrix(self.rows, self.columns, self.min_value, self.max_value)
  def pretty_print(self):
    """
    Prints the matrix in a pretty format.
    """
    for row in self.matrix:
      print(*row)
