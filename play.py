import copy
import math
from Game import Game

class Play:
    def __init__(self, game):
        self.game = game

    def renderGameState(self):
        print(self.game.state.board)
    
    # def renderGameState(self):
    #     board = self.game.state.board
    #     # Print header with pit names (you can adjust this for your format)
    #     print("---------------------<<<<<<<<<<PLAYER 2--------------------------------------")
    #     player_2_pits = self.game.state.player_pits[2]
    #     # Extract each pit one by one
    #     pit_G = player_2_pits[0]  
    #     pit_H = player_2_pits[1]  
    #     pit_I = player_2_pits[2]  
    #     pit_J = player_2_pits[3]  
    #     pit_K = player_2_pits[4]  
    #     pit_L = player_2_pits[5]  
    #     print(f"2      |{pit_G}      |{pit_H}      |{pit_I}       |{pit_J}      |{pit_K}      |{pit_L}       |      1")
    #     print("       |       |       |        |       |       |        |       ")
    #     self.game.state.player_pits[2]#PLAYER 2
    #     # Extract pits G to L
    #     pit_G = board["G"]  
    #     pit_H = board["H"]  
    #     pit_I = board["I"]  
    #     pit_J = board["J"]  
    #     pit_K = board["K"]  
    #     pit_L = board["L"]  

    #     # Extract the stores (1 and 2)
    #     store_1 = board[1]  # 0
    #     store_2 = board[2]  # 0
        
          
          
    #     print(f"       |  {pit_G}    |  {pit_H}    |  {pit_I}     |  {pit_J}    |  {pit_K}    |  {pit_L}     |       ")
    #     print("       |       |       |        |       |       |        |       ")

        
    #     print(f"    {store_2}  |-----------------PLAYER 1>>>>>>>>>---------------|   {store_1}    ")
    #     player_1_pits = self.game.state.player_pits[1]
    #     pit_A = player_1_pits[0]  
    #     pit_B = player_1_pits[1]  
    #     pit_C = player_1_pits[2]  
    #     pit_D = player_1_pits[3]  
    #     pit_E = player_1_pits[4]  
    #     pit_F = player_1_pits[5] 
         

          
    #     print(f"       |{pit_A}      |{pit_B}      |{pit_C}       |{pit_D}      |{pit_E}      |{pit_F}       |       ")
    #     print("       |       |       |        |       |       |        |       ")
        
    #     pit_A = board["A"]  
    #     pit_B = board["B"]  
    #     pit_C = board["C"]  
    #     pit_D = board["D"]  
    #     pit_E = board["E"]  
    #     pit_F = board["F"] 
    #     print(f"       |  {pit_A}    |  {pit_B}    |  {pit_C}     |  {pit_D}    |  {pit_E}    |  {pit_F}     |       ")
    #     print("       |       |       |        |       |       |        |       ")
    #     print("----------------------------------------------------------------------------------")



    def humanTurn(self):
        """
        Allows the human player to make a move.
        """
        print("Human's turn")
        possible_moves = self.game.state.possible_moves(self.game.player_side["HUMAN"])
        print("Possible moves:", possible_moves)

        while True:
            pit = input("Choose a pit to play from: ")
            if pit in possible_moves:
                self.game.state.doMove(self.game.player_side["HUMAN"], pit)
                break
            else:
                print("Invalid move. Please choose a valid pit.")

        # Visualize the updated game state
        self.renderGameState()

    def computerTurn(self, depth=3):
        """
        Determines the computer's move using Minimax with Alpha-Beta Pruning.
        """
        print("Computer's turn")
        _, best_pit = self.MinimaxAlphaBetaPruning(self.game, 1, depth, -math.inf, math.inf)
        print(f"Computer chooses pit {best_pit}")
        pit=self.game.state.doMove(self.game.player_side["COMPUTER"], best_pit)

        # Visualize the updated game state
        self.renderGameState()

    def MinimaxAlphaBetaPruning(self, game, player, depth, alpha, beta):
        if game.gameOver() or depth == 1:
            bestValue = game.evaluate()
            return bestValue, None

        if player == 1:  
            best_value = -math.inf
            best_pit = None

            for pit in game.state.possible_moves(game.player_side["COMPUTER"]):
                child_game = copy.deepcopy(game)
                child_game.state.doMove(game.player_side["COMPUTER"], pit)
                value, _ = self.MinimaxAlphaBetaPruning(child_game, -1, depth - 1, alpha, beta)

                if value > best_value:
                    best_value = value
                    best_pit = pit

                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break  # Beta cutoff

            return best_value, best_pit

        else:  # MIN/Human's turn
            best_value = math.inf
            best_pit = None

            for pit in game.state.possible_moves(game.player_side["HUMAN"]):
                child_game = copy.deepcopy(game)
                child_game.state.doMove(game.player_side["HUMAN"], pit)
                value, _ = self.MinimaxAlphaBetaPruning(child_game, 1, depth - 1, alpha, beta)

                if value < best_value:
                    best_value = value
                    best_pit = pit

                beta = min(beta, best_value)
                if beta <= alpha:
                    break  # Alpha cutoff

            return best_value, best_pit

# Example usage
if __name__ == "__main__":
    chosenPlayer=input("please chose which player are you:(1 or 2 )")
    # Convert the input to an integer
    chosenPlayer = int(chosenPlayer)
    if chosenPlayer==1:
        computerPlayer=2
    else:
        computerPlayer=1
    game = Game(human_side=chosenPlayer,computer_side=computerPlayer)
    play = Play(game)

    play.renderGameState()  # Initial game state visualization

    while not game.gameOver():
        play.humanTurn()
        if game.gameOver():
            break
        play.computerTurn()

    winner, score = game.findWinner()
    print(f"Game Over! The winner is {winner} with a score of {score}.")
