"""Chain module."""
import yaml
from fractions import Fraction


class Field:
    """Class reprent singe field on board.

    if marked and probability equal 1 means field is marked full
    if marked and probability equal 0 means field is marked empty
    """

    def __init__(self, col: int, row: int, marked=False,
                 probability=Fraction(0)) -> None:
        """Init method.

        Args:
            col (int): column position
            row (int): row position
            marked (boolean): is marked
            probability (float): change to marked
        """
        self._probability = probability
        self.col = col
        self.row = row
        self.marked = marked

    @property
    def probability(self):
        return self._probability

    @probability.setter
    def probability(self, value: Fraction):
        assert value <= Fraction(1, 1), "{} {}".format(self, value)
        self._probability = value

    def __repr__(self):
        return "Field({}, {}, {}, {})".format(self.col, self.row,
                                              self.probability, self.marked)

def percent(value: Fraction) -> str:
    if value < Fraction(1, 8):
        return " "
    if value < Fraction(2, 8):
        return "▁"
    if value < Fraction(3, 8):
        return "▂"
    if value < Fraction(4, 8):
        return "▃"
    if value < Fraction(5, 8):
        return "▄"
    if value < Fraction(6, 8):
        return "▅"
    if value < Fraction(7, 8):
        return "▆"
    if value < Fraction(8, 8):
        return "▇"
    return "█"


class Board:
    """Board class."""

    def __init__(self, filename: str) -> None:
        """Init method for board class.

        Args:
            filename (str): path for file
        """

        with open(filename) as stream:
            result = yaml.load(stream)
            self.x_lines = result['xaxis']['lines']
            self.y_lines = result['yaxis']['lines']
            sum_in_x = sum([sum(l) for l in self.x_lines])
            sum_in_y = sum([sum(l) for l in self.y_lines])
            assert sum_in_x == sum_in_y, """sum of marked field in x {} is not
                                            equal field y {}""".format(sum_in_x, sum_in_y)
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

    def print_board(self):
        display_board = ""
        for col in self.board_field:
            for field in col:
                display_board += percent(field.probability)
            display_board += "\n"
        print(display_board)

    def solve_board(self):
        while not self.check_solution():
            for i, column in enumerate(self.x_lines):
                x_combinations = self.make_combinations(column)
                number_of_combination = len(x_combinations)
                if number_of_combination == 0:
                    self.mark_field(i)
                    continue
                x_combinations = self.get_not_collidate(x_combinations, column, i)
                probability = Fraction(1, len(x_combinations))

                for field in self.board_field[i]:
                    if not field.marked:
                        field.probability = Fraction(0)
                for combination in x_combinations:
                    match = zip(combination, column)
                    self.add_probability_to_field(match, i, probability)
                self.mark_field(i)
            for i, row in enumerate(self.y_lines):
                y_combinations = self.make_combinations(row, True)
                number_of_combination = len(y_combinations)
                if number_of_combination == 0:
                    self.mark_field(i, True)
                    continue
                y_combinations = self.get_not_collidate(y_combinations, row, i, True)
                probability = Fraction(1, len(y_combinations))

                for fields_row in self.board_field:
                    if not fields_row[i].marked:
                        fields_row[i].probability = Fraction(0)
                for combination in y_combinations:
                    match = zip(combination, row)
                    self.add_probability_to_field(match, i, probability, True)
                self.mark_field(i, True)
            #return None

    def get_not_collidate(self, combinations, row, i: int, is_row=False):
        new_list = []
        for combination in combinations:
            start = 0
            fail = False
            for (space, axe) in zip(combination, row):
                for x in range(space):
                    axe_marked = Fraction(1)
                    fail = self.is_collidate(is_row, start, x, i, axe_marked)
                start += space
                for x in range(axe):
                    axe_unmarked = Fraction(0)
                    fail = self.is_collidate(is_row, start, x, i, axe_unmarked)
            if not fail:
                new_list.append(combination)
        return new_list

    def is_collidate(self, is_row, start, x: int, i: int, axe_marked) -> bool:
        if is_row:
            field = self.board_field[start+x][i]
        else:
            field = self.board_field[i][start+x]
        return field.marked and field.probability == axe_marked

    def add_probability_to_field(self, match, i: int, probability: Fraction,
                                 is_row=False) -> None:
        start = 0
        for (space, axe) in match:
            start += space
            for x in range(axe):
                if is_row:
                    field = self.board_field[start+x][i]
                else:
                    field = self.board_field[i][start+x]
                if not field.marked:
                    field.probability += probability
            start += axe

    def mark_field(self, i, is_row=False):
        if is_row:
            fields = self.board_field[:][i]
        else:
            fields = self.board_field[i]
        for field in fields:
            if field.probability in [Fraction(0), Fraction(1)]:
                field.marked = True

    def make_combinations(self, column, is_row=False) -> []:
        lenght = self.x_lenght if is_row else self.y_lenght

        number_of_space = len(column) + 1
        """
            OXOXOXO    OXXXOO
            4 space    2 space
            3 Axe :)   1 Axe :)
            Number of space = Number of axe + 1
        """
        combination_list = Board.generate(column, lenght, number_of_space)
        return [combination for combination in combination_list]

    @staticmethod
    def generate(column: [int], lenght: int, number_of_space: int):
        if number_of_space < 2 or lenght < 1 or number_of_space < 2:
            return
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
            sum_of_column = sum(column)
            exclusive_length = sum(combination) + sum_of_column
            if exclusive_length == lenght and exclusive_zero:
                yield combination[:]

    optimize_counter = 0
    optimize_max = 100

    def check_solution(self) -> bool:
        if self.optimize_counter > self.optimize_max:
            return True
        self.optimize_counter += 1
        marked_field_count = 0
        for column in self.board_field:
            for field in column:
                if field.marked and field.probability == Fraction(1):
                    marked_field_count += 1
        assert self.count >= marked_field_count
        return marked_field_count == self.count
