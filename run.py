from chainsaw.chain import Board

n = Board('example/game1.yaml')
n.solve_board()
n.print_board()

n = Board('example/game2.yaml')
n.solve_board()
n.print_board()