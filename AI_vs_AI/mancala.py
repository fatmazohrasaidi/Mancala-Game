
class MancalaBoard:
    def __init__(self):
        self.board={"A":4,"B":4,"C":4,"D":4,"E":4,"F":4,"G":4,"H":4,"I":4,"J":4,"K":4,"L":4,1:0,2:0}
        self.player_pits={1:("A","B","C","D","E","F"),
                          2:("G","H","I","J","K","L")}
        self.opposite_pit={"A":"G","B":"H","C":"I","D":"J","E":"K","L":"F",
                           "G":"A","H":"B","I":"C","J":"D","K":"E","F":"L"}
        self.next_pit = {
            "A": "B", "B": "C", "C": "D", "D": "E", "E": "F", "F": 1,   # Player 1's store after "F"
            1: "L",  # Player 1's store connects to Player 2's last pit
            "L": "K", "K": "J", "J": "I", "I": "H", "H": "G", "G": 2,   # Counterclockwise order for Player 2
            2: "A"    # Player 2's store connects back to Player 1’s first pit
        }
    
    def possible_moves(self, player):
        """Return the pits that the player can play from (non-empty pits)."""
        return [pit for pit in self.player_pits[player] if self.board[pit] > 0]


    def doMove(self,player,pit):
        """Execute a move for the given player starting at the specified pit."""
        seeds = self.board[pit]#how many seeds are in this pit
        if seeds == 0:
            raise ValueError(f"Pit {pit} is empty, choose a different pit.")

        self.board[pit] = 0  # Remove all seeds from the starting pit
        current_pit = pit

        # Distribute seeds counterclockwise
        while seeds > 0:
            current_pit = self.next_pit[current_pit]
            # Skip opponent's store
            if (current_pit == 1 and player == 2) or (current_pit == 2 and player == 1):
                continue

            self.board[current_pit] += 1
            seeds -= 1

        # Check capture condition
        if current_pit in self.player_pits[player] and self.board[current_pit] == 1:
            opposite_pit = self.opposite_pit[current_pit]  # Get the opposite pit
            captured_seeds = self.board[opposite_pit]
            if captured_seeds > 0:  # Only capture if there are seeds in the opposite pit
                self.board[current_pit] = 0
                self.board[opposite_pit] = 0
                self.board[player] += 1 + captured_seeds  # Add the last seed + captured seeds to the store


        # Return the final pit for any additional game logic (optional)
        return current_pit
    
# board=MancalaBoard()
# print(board.possible_moves(1))
# print(board.possible_moves(2))
# print(board.doMove(1,"A"))
# print(board.board)
