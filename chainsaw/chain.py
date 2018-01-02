import yaml


class Field:
    def __init__(self, col, row, probability=0):
        self.probability = probability
        self.col = col
        self.row = row

    def __repr__(self):
        return "Field({}, {}, {})".format(self.col, self.row,
                                          self.probability)

class Board:

    def __init__(self, filename):
        with open(filename) as stream:
            result = yaml.load(stream)
            self.x_lines = result['xaxis']['lines']
            self.y_lines = result['yaxis']['lines']
            self.x_lenght = len(self.x_lines)
            self.y_lenght = len(self.y_lines)
            self.board_field = [
                            [Field(col, row) for row in range(self.y_lenght)]
                            for col in range(self.x_lenght)]
    def __repr__(self):
        return "Board({}, {}) with fields {}".format(self.x_lenght,
                                                     self.y_lenght,
                                                     self.board_field)