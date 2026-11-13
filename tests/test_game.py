import pytest
from game import TicTacToe


def test_board_creation():
    game = TicTacToe()

    assert len(game.board) == 3
    assert all(len(row) == 3 for row in game.board)


def test_board_is_empty():
    game = TicTacToe()

    for row in game.board:
        for cell in row:
            assert cell is None


def test_first_move_x():
    game = TicTacToe()

    game.make_move(0, 0)

    assert game.board[0][0] == "X"


def test_player_switch_after_move():
    game = TicTacToe()

    assert game.current_player == "X"

    game.make_move(0, 0)

    assert game.current_player == "O"


def test_second_move_o():
    game = TicTacToe()

    game.make_move(0, 0)
    game.make_move(0, 1)

    assert game.board[0][0] == "X"
    assert game.board[0][1] == "O"
    assert game.current_player == "X"


def test_move_on_occupied_cell():
    game = TicTacToe()

    game.make_move(0, 0)

    with pytest.raises(ValueError):
        game.make_move(0, 0)

    assert game.board[0][0] == "X"
    assert game.current_player == "O"


@pytest.mark.parametrize(
    "row, col",
    [
        (-1, 0),
        (0, -1),
        (3, 0),
        (0, 3),
        (5, 5)
    ]
)
def test_move_out_of_bounds(row, col):
    game = TicTacToe()

    with pytest.raises(ValueError):
        game.make_move(row, col)

    assert game.board == [[None] * 3 for _ in range(3)]
    assert game.current_player == "X"


def test_horizontal_win():
    game = TicTacToe()

    game.make_move(0, 0)  # X
    game.make_move(1, 0)  # O
    game.make_move(0, 1)  # X
    game.make_move(1, 1)  # O
    game.make_move(0, 2)  # X

    assert game.check_winner() == "X"


def test_vertical_win():
    game = TicTacToe()

    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(1, 0)  # X
    game.make_move(1, 1)  # O
    game.make_move(2, 0)  # X

    assert game.check_winner() == "X"


def test_diagonal_win():
    game = TicTacToe()

    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(1, 1)  # X
    game.make_move(1, 0)  # O
    game.make_move(2, 2)  # X

    assert game.check_winner() == "X"


def test_draw():
    game = TicTacToe()

    game.board = [
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", "X"]
    ]

    assert game.is_draw() is True


def test_no_draw_on_incomplete_board():
    game = TicTacToe()

    game.make_move(0, 0)
    game.make_move(1, 1)

    assert game.is_draw() is False


def test_no_draw_when_winner_exists():
    game = TicTacToe()

    game.board = [
        ["X", "X", "X"],
        ["O", "O", "X"],
        ["O", "X", "O"]
    ]

    assert game.check_winner() == "X"
    assert game.is_draw() is False


def test_move_after_win():
    game = TicTacToe()

    game.make_move(0, 0)  # X
    game.make_move(1, 0)  # O
    game.make_move(0, 1)  # X
    game.make_move(1, 1)  # O
    game.make_move(0, 2)  # X — победа

    assert game.check_winner() == "X"

    board_before = [row.copy() for row in game.board]
    player_before = game.current_player

    with pytest.raises(ValueError):
        game.make_move(2, 2)

    assert game.board == board_before
    assert game.current_player == player_before


def test_move_after_draw():
    game = TicTacToe()

    game.board = [
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", "X"]
    ]

    assert game.is_draw() is True

    board_before = [row.copy() for row in game.board]
    player_before = game.current_player

    with pytest.raises(ValueError, match="Игра уже завершена"):
        game.make_move(0, 0)

    assert game.board == board_before
    assert game.current_player == player_before


def test_reset_game():
    game = TicTacToe()

    game.make_move(0, 0)
    game.make_move(1, 1)
    game.make_move(0, 1)

    game.reset_game()

    assert game.board == [[None] * 3 for _ in range(3)]
    assert game.current_player == "X"
    assert game.check_winner() is None
    assert game.is_draw() is False


def test_full_game_scenario():
    game = TicTacToe()

    moves = [
        (0, 0),  # X
        (1, 0),  # O
        (0, 1),  # X
        (1, 1),  # O
        (0, 2)   # X — победа
    ]

    result = game.play_moves(moves)

    assert result == "X"
    assert game.check_winner() == "X"

    assert game.board == [
        ["X", "X", "X"],
        ["O", "O", None],
        [None, None, None]
    ]

    with pytest.raises(ValueError):
        game.make_move(2, 2)