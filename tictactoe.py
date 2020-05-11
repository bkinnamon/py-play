"""This module provides a class that plays a tic-tac-toe game."""


class TicTacToe:
    """This class plays a tic-tac-toe game."""

    board = [None] * 9
    player = 'X'
    winner = None

    def new_game(self):
        """Creates a new game."""
        self.board = [None] * 9
        self.player = "X"
        self.winner = None

    def make_move(self, index):
        """Makes a move for the current player."""
        if self.board[index] is None and self.get_winner() is None:
            self.board[index] = self.player
            self.player = 'O' if self.player == 'X' else 'X'
            self.winner = self.get_winner()

    def get_winner(self):
        """Checks to see if a player has won yet."""
        combos = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        winner = None
        for combo in combos:
            a, b, c = combo
            if (
                    self.board[a] is not None
                    and self.board[a] == self.board[b]
                    and self.board[a] == self.board[c]
            ):
                winner = self.board[a]
                break
        return winner

    def get_state(self):
        """Returns the state of the game."""
        return {
            "board": self.board,
            "player": self.player,
            "winner": self.winner
        }
