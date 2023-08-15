import generators

if __name__ == "__main__":
  rand_matrix = generators.Random(12, 12)
  print(rand_matrix.get_item(11, 11))
  rand_matrix.pretty_print()