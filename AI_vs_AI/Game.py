from mancala import MancalaBoard

class Game:
    def __init__(self, computer1_side=1, computer2_side=2):
        """Initialize the game with a starting board and player sides."""
        self.state = MancalaBoard()  # Initialize the board
        self.player_side = {
            "COMPUTER1": computer1_side,  # Assign Player 1
            "COMPUTER2": computer2_side  # Assign Player 2
        }

    def gameOver(self):
        """Check if the game has ended. Returns True if the game has ended, False otherwise."""
        # Check if all pits on either player's side are empty
        player1_empty = all(self.state.board[pit] == 0 for pit in self.state.player_pits[1])
        player2_empty = all(self.state.board[pit] == 0 for pit in self.state.player_pits[2])

        if player1_empty or player2_empty:
            # Collect remaining seeds and place them in the respective stores
            for pit in self.state.player_pits[1]:
                self.state.board[1] += self.state.board[pit]
                self.state.board[pit] = 0

            for pit in self.state.player_pits[2]:
                self.state.board[2] += self.state.board[pit]
                self.state.board[pit] = 0

            return True
        return False

    def findWinner(self):
        """Determine the winner of the game."""
        player1_store = self.state.board[1]
        player2_store = self.state.board[2]

        if player1_store > player2_store:
            return "COMPUTER1", player1_store
        elif player2_store > player1_store:
            return "COMPUTER2", player2_store
        else:
            return "TIE", player1_store  # Both scores are equal

    def evaluate_player1(self):
        """Evaluate the board based on Player 1's potential capture advantage."""
        capture_advantage = 0

        for pit in self.state.player_pits[1]:  # Iterate over Player 1's pits
            if self.state.board[pit] == 0:  # Check if the pit is empty
                opposite_pit = self.state.opposite_pit[pit]
                capture_advantage += self.state.board[opposite_pit]  # Seeds in the opponent's pit

        return capture_advantage

    def evaluate_player2(self):
        """Evaluate the board based on Player 2's score advantage."""
        player2_store = self.state.board[2]
        player1_store = self.state.board[1]

        # Difference between Player 2's store and Player 1's store
        return player2_store - player1_store

    def evaluate(self, player):
        """Evaluate the board from the perspective of the given player."""
        if player == 1:
            return self.evaluate_player1()
        else:
            return self.evaluate_player2()


# Test the Game Class
game = Game()

# Display player sides
print("Player sides:", game.player_side)

# Check possible moves for Player 1
print("Possible moves for COMPUTER1:", game.state.possible_moves(1))

# Perform moves for Player 1
for pit in game.state.player_pits[1]:
    if game.state.board[pit] > 0:  # Check if pit is non-empty
        print(f"Performing move on pit {pit}")
        game.state.doMove(1, pit)
        break

# Display the board after the move
print("Board after COMPUTER1's move:", game.state.board)

# Check if the game is over
if game.gameOver():
    print("Game Over!")
    winner, score = game.findWinner()
    print(f"The winner is {winner} with a score of {score}.")
else:
    print("The game is still ongoing.")

# Evaluate the board for Player 1
print("Evaluation for COMPUTER1:", game.evaluate(1))
# Evaluate the board for Player 2
print("Evaluation for COMPUTER2:", game.evaluate(2))
