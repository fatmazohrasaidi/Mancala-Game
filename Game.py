from mancala import MancalaBoard

class Game:
    def __init__(self, human_side=1, computer_side=2):
        """Initialize the game with a starting board and player sides."""
        # Initialize the state as an instance of MancalaBoard
        self.state = MancalaBoard()

        # Player sides
        self.player_side = {
            "HUMAN": human_side,# from A to F (its an argument and its initially 1)
            "COMPUTER": computer_side # from G to L
        }

    def gameOver(self):
        """Check if the game has ended. Returns:True if the game has ended, False otherwise. """
        human_side = self.player_side["HUMAN"]
        computer_side = self.player_side["COMPUTER"]
        
        # Check if all pits on either player's side are empty
        human_empty = all(self.state.board[pit] == 0 for pit in self.state.player_pits[human_side])
        computer_empty = all(self.state.board[pit] == 0 for pit in self.state.player_pits[computer_side])

        if human_empty or computer_empty:
            # Collect remaining seeds and place them in the respective store
            for pit in self.state.player_pits[human_side]:
                self.state.board[human_side] += self.state.board[pit]
                self.state.board[pit] = 0

            for pit in self.state.player_pits[computer_side]:
                self.state.board[computer_side] += self.state.board[pit]
                self.state.board[pit] = 0

            return True

        return False

    def findWinner(self):
        """ Determine the winner of the game. """
        human_store = self.state.board[self.player_side["HUMAN"]]
        computer_store = self.state.board[self.player_side["COMPUTER"]]

        if human_store > computer_store:
            return "HUMAN", human_store
        elif computer_store > human_store:
            return "COMPUTER", computer_store
        else:
            return "TIE", human_store  # Both scores are equal

    def evaluate(self):
        computer_store = self.state.board[self.player_side["COMPUTER"]]
        human_store = self.state.board[self.player_side["HUMAN"]]

        # Equation 1: Difference between seeds in the computer's store and the human's store
        return computer_store - human_store



# # Initialize the game

# game = Game()
# print(game.player_side)
# # Check possible moves for Player 1 (human)
# print("Possible moves for HUMAN:", game.state.possible_moves(1))

# # Perform a move
# game.state.doMove(1, "A")
# game.state.doMove(1, "B")
# game.state.doMove(1, "C")
# game.state.doMove(1, "D")
# game.state.doMove(1, "E")
# game.state.doMove(1, "F")
# print("Board after HUMAN's move:", game.state.board)

# # Check if the game is over
# if game.gameOver():
#     print("Game Over!")
#     winner, score = game.findWinner()
#     print(f"The winner is {winner} with a score of {score}.")
# else:
#     print("The game is still ongoing.")

# # Evaluate the current state
# print("Evaluation of the current state:", game.evaluate())

