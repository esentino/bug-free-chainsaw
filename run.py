from chainsaw.chain import Board

n = Board('example/game1.yaml')
n.solve_board()
print(n)

n = Board('example/game2.yaml')
n.solve_board()
print(n)