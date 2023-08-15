from random import randint as random_int

def random_matrix_int(rows=4, cols=4, min_value=1, max_value=9)->list:
    """
    Returns a matrix of random values.
    """
    return [[random_int(min_value, max_value) for _ in range(cols)] for _ in range(rows)]

class Random:
  def __init__(self, rows=4, columns=4, max_value=9, min_value=1) -> None:
    self.rows = rows
    self.columns = columns
    self.max_value = max_value
    self.min_value = min_value
    self.matrix = random_matrix_int(self.rows, self.columns, self.min_value, self.max_value)

  def __str__(self) -> str:
    return f"Random Matrix of {self.rows} rows and {self.columns} columns"

  def __repr__(self) -> str:
    return f"Random({self.rows}, {self.columns}, {self.max_value}, {self.min_value})"

  def pretty_print(self):
    """
    Prints the matrix in a pretty format.
    """
    for row in self.matrix:
      print(*row)
  
  def get_item(self, x, y):
    """
    Returns the value at the given index
    """
    if x < 0 or y < 0 or x >= self.rows or y >= self.columns:
      raise IndexError("Index out of range")
    return self.matrix[x][y]
