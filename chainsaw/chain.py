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
        while not self.check_solution():
            for i, column in enumerate(self.x_lines):
                x_combinations = Board.make_combination_list(column,
                                                             self.x_lenght)
                number_of_combination = len(x_combinations)
                if number_of_combination == 0:
                    self.mark_field(i)
                    continue
                axe_probability = 1.0/number_of_combination

                for field in self.board_field[i]:
                    field.probability = 0.0
                for combination in x_combinations:
                    match = zip(combination, column)
                    self.add_probability_to_field(match, i, axe_probability)
                self.mark_field(i)
            for i, row in enumerate(self.x_lines):
                y_combinations = Board.make_combination_list(row,
                                                             self.y_lenght)
                number_of_combination = len(y_combinations)
                if number_of_combination == 0:
                    self.mark_field(i, True)
                    continue
                axe_probability = 1.0/number_of_combination

                for field in self.board_field[:][i]:
                    field.probability = 0.0
                for combination in y_combinations:
                    match = zip(combination, row)
                    self.add_probability_to_field(match, i, axe_probability, True)
                self.mark_field(i)
            return None

    def add_probability_to_field(self, match, i, axe_probability, row=False):
        start = 0
        for (space, axe) in match:
            start += space
            for x in range(axe):
                if row:
                    field = self.board_field[start+x][i]
                else:
                    field = self.board_field[i][start+x]
                if not field.marked:
                    field.probability += axe_probability
            start += axe

    def mark_field(self, i, row=False):
        fields = self.board_field[i]
        if row:
            fields = self.board_field[:][i]

        for field in fields:
            if field.probability == 0.0 or field.probability == 1.0:
                field.marked = True

    def make_combination_list(column, lenght):
        
        number_of_space = len(column) + 1
        """
            OXOXOXO    OXXXOO
            4 space    2 space
            3 Axe :)   1 Axe :)
            Number of space = Number of axe + 1
        """
        combination_list = Board.generate(column, lenght, number_of_space)
        return [combination for combination in combination_list]

    def generate(column, lenght, number_of_space):
        sum_of_column = sum(column)
        if number_of_space > 1:
            combination = [0 for i in range(number_of_space)]
            end = False
            while not end:
                for number in range(number_of_space):
                    if combination[number] + 1 == lenght:
                        combination[number] = 0
                        if number + 1 == number_of_space:
                            end = True
                        else:
                            combination[number+1] += 1
                    elif number == 0:
                        combination[number] += 1
                exclusive_zero = all([x > 0 for x in combination[1:-1]])
                exclusive_length = sum(combination) + sum_of_column
                if exclusive_length == lenght and exclusive_zero:
                    yield combination[:]

    def check_solution(self):
        marked_field_count = 0
        for column in self.board_field:
            for field in column:
                if field.marked:
                    marked_field_count += 1
        assert self.count >= marked_field_count
        return marked_field_count == self.count
