class TicTacToe:
    def __init__(self):
        self.reset_game()

    def validate_move(self, row, col):
        if self.check_winner() is not None or self.is_draw():
            raise ValueError("Игра уже завершена")
        
        if not (0 <= row < 3 and 0 <= col < 3):
            raise ValueError("Координаты вне диапазона")
        
        if self.board[row][col] is not None:
            raise ValueError("Клетка уже занята")

    def make_move(self, row, col):
        self.validate_move(row, col)
        
        self.board[row][col] = self.current_player
        self.current_player = "O" if self.current_player == "X" else "X"

    def _check_line(self, line):
        if line[0] is not None and all(cell == line[0] for cell in line):
            return line[0]
        return None

    def check_winner(self):
        # Проверка горизонтальных линий
        for row in self.board:
            winner = self._check_line(row)
            if winner:
                return winner

        # Проверка вертикальных линий
        for col in range(3):
            column = [self.board[row][col] for row in range(3)]

            winner = self._check_line(column)
            if winner:
                return winner

        # Проверка главной диагонали
        main_diagonal = [self.board[i][i] for i in range(3)]
        winner = self._check_line(main_diagonal)
        
        if winner:
            return winner

        # Проверка побочной диагонали
        secondary_diagonal = [self.board[i][2 - i] for i in range(3)]
        winner = self._check_line(secondary_diagonal)
        
        if winner:
            return winner

        return None


    def is_draw(self):
        return (self.check_winner() is None and all(
            cell is not None for row in self.board for cell in row
        ))


    def reset_game(self):
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = "X"


    def get_game_result(self):
        winner = self.check_winner()

        if winner is not None:
            return winner

        if self.is_draw():
            return "draw"

        return None


    def play_moves(self, moves):
        for row, col in moves:
            self.make_move(row, col)

        return self.get_game_result()