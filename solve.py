import sys
import pycosat

DEFAULT_N = 8

def get_n():
  if len(sys.argv) >= 2:
    return int(sys.argv[1])
  else:
    return DEFAULT_N


def encode_cell(r, c, n):
  return r * n + c + 1


def decode_cell(id, n):
  id = id - 1
  return (id // n, id % n)  


def generate_cnf_formula(n):
  clauses = []

  for row in range(n):
    clauses.append([encode_cell(row, column, n) for column in range(n)])

  for row in range(n):
    for column1 in range(n):
      for column2 in range(column1):
        clauses.append([-encode_cell(row, column1, n), -encode_cell(row, column2, n)])

  for column in range(n):
    for row1 in range(n):
      for row2 in range(row1):
        clauses.append([-encode_cell(row1, column, n), -encode_cell(row2, column, n)])

  def on_one_diagonal(row1, column1, row2, column2):
    return abs(row1 - row2) == abs(column1 - column2)

  for row1 in range(n):
    for column1 in range(n):
      for row2 in range(row1):
        for column2 in range(n):
          if on_one_diagonal(row1, column1, row2, column2):
            clauses.append([-encode_cell(row1, column1, n), -encode_cell(row2, column2, n)])
  
  return clauses


def print_solution(result, n):
  board = [['.' for _ in range(n)] for _ in range(n)]
  for literal in result:
    if literal > 0:
      (row, column) = decode_cell(literal, n)
      board[row][column] = 'Q'
  for row in range(n):
    for column in range(n):
      print(board[row][column], end = '')
    print()         


n = get_n()
result = pycosat.solve(generate_cnf_formula(n))

if result == "UNSAT":
  print("There is no solution for n = ", n)
else:
  print_solution(result, n)
  