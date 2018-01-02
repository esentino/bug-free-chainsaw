import yaml


class Field:
    def __init__(self, col, row, marked=False, probability=0):
        self.probability = probability
        self.col = col
        self.row = row
        self.marked = marked

    def __repr__(self):
        return "Field({}, {}, {}, {})".format(self.col, self.row,
                                              self.probability, self.marked)


class Board:
    """Board class."""

    def __init__(self, filename):
        with open(filename) as stream:
            result = yaml.load(stream)
            self.x_lines = result['xaxis']['lines']
            self.y_lines = result['yaxis']['lines']
            self.x_lenght = len(self.x_lines)
            self.y_lenght = len(self.y_lines)
            self.board_field = [
                [
                    Field(col, row)
                    for row in range(self.y_lenght)
                ]
                for col in range(self.x_lenght)
            ]
            """ Hyperpythonic resolution totally unreadable
            self.count = sum(
                [sum([value for value in column]) for column in self.x_lines]
            )
            """
            self.count = 0
            for column in self.x_lines:
                for value in column:
                    self.count += value

    def __repr__(self):
        return """
            Board({}, {}) with fields:
            {} and lines:
            x {},
            y {}""".format(self.x_lenght, self.y_lenght, self.board_field, 
                           self.x_lines, self.y_lines)

    def solve_board(self):
        self.check_solution()

    def check_solution(self):
        marked_field_count = 0
        for column in self.board_field:
            for field in column:
                if field.marked:
                    marked_field_count += 1
        assert self.count >= marked_field_count
        return marked_field_count == self.count
