import pygame
import sys
import copy
import math
from Game import Game
# Constants for the Pygame window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
PIT_RADIUS = 30
STORE_WIDTH = 80
STORE_HEIGHT = 200
BOARD_COLOR = (34, 139, 34)  # Green
PIT_COLOR = (210, 180, 140)  # Tan
TEXT_COLOR = (0, 0, 0)  # Black
SEED_COLOR = (255, 223, 0)  # Yellow
FONT_SIZE = 20

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mancala Game")
font = pygame.font.Font(None, FONT_SIZE)

class Play:
    def __init__(self, game):
        self.game = game
    
    def render_game_over(self):
        """Render the Game Over screen with the winner and the score."""
        screen.fill(BOARD_COLOR)

        # Get winner and score
        winner,score = self.game.findWinner()
        

        # Render Game Over text
        game_over_text = font.render("Game Over!", True, TEXT_COLOR)
        game_over_text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        screen.blit(game_over_text, game_over_text_rect)

        # Render Winner text
        winner_text = font.render(f"Winner: {winner}", True, TEXT_COLOR)
        winner_text_rect = winner_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        screen.blit(winner_text, winner_text_rect)

        # Render Scores
        score_text = font.render(f"Score: {score} - {48-score}", True, TEXT_COLOR)
        
        screen.blit(score_text, (WINDOW_WIDTH // 2 - 40, WINDOW_HEIGHT // 2 + 40))
        

        pygame.display.flip()

        # Wait for the player to close the window or press a key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

    def renderGameState(self):
        screen.fill(BOARD_COLOR)
        # Draw stores and display seed count
        player_2_store = self.game.state.board.get(2, 0)  # Player 2 store
        player_1_store = self.game.state.board.get(1, 0)  # Player 1 store
        pygame.draw.rect(screen, PIT_COLOR, (50, 100, STORE_WIDTH, STORE_HEIGHT))  # Player 2 store
        pygame.draw.rect(screen, PIT_COLOR, (WINDOW_WIDTH - 130, 100, STORE_WIDTH, STORE_HEIGHT))  # Player 1 store
        
        # Display seed count in the stores
        player_2_text = font.render(str(player_2_store), True, TEXT_COLOR)
        player_2_text_rect = player_2_text.get_rect(center=(50 + STORE_WIDTH // 2, 100 + STORE_HEIGHT // 2))
        screen.blit(player_2_text, player_2_text_rect)
        
        player_1_text = font.render(str(player_1_store), True, TEXT_COLOR)
        player_1_text_rect = player_1_text.get_rect(center=(WINDOW_WIDTH - 130 + STORE_WIDTH // 2, 100 + STORE_HEIGHT // 2))
        screen.blit(player_1_text, player_1_text_rect)
        
        # Draw pits and display number of seeds in each pit
        positions = self.get_pit_positions()
        for pit, pos in positions.items():
            pygame.draw.circle(screen, PIT_COLOR, pos, PIT_RADIUS)
            
            # Display number of seeds in each pit
            seeds = self.game.state.board.get(pit, 0)
            seed_text = font.render(str(seeds), True, TEXT_COLOR)
            seed_text_rect = seed_text.get_rect(center=(pos[0], pos[1] - 15))  # Slightly above the pit
            screen.blit(seed_text, seed_text_rect)
            
            # Display pit label
            label_text = font.render(pit, True, TEXT_COLOR)
            label_text_rect = label_text.get_rect(center=(pos[0], pos[1] + 20))  # Below the pit
            screen.blit(label_text, label_text_rect)
        
        # Display player labels
        player_1_label = font.render("Player 1", True, TEXT_COLOR)
        player_2_label = font.render("Player 2", True, TEXT_COLOR)
        screen.blit(player_1_label, (WINDOW_WIDTH - 100, 350))
        screen.blit(player_2_label, (50, 50))

    def get_pit_positions(self):
        """Calculate positions for all pits on the board."""
        positions = {}
        x_gap = (WINDOW_WIDTH - 200) // 6
        y_top = 100
        y_bottom = 300

        # Player 2 pits (G to L)
        for i, pit in enumerate(["G", "H", "I", "J", "K", "L"]):
            positions[pit] = (150 + i * x_gap, y_top)

        # Player 1 pits (A to F)
        for i, pit in enumerate(["A", "B", "C", "D", "E", "F"]):
            positions[pit] = (150 + i * x_gap, y_bottom)

        return positions
    
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



    def computerTurn(self,player, depth=3):
        """
        Determines the computer's move using Minimax with Alpha-Beta Pruning.
        """
        print(f"Computer {player} turn")
        _, best_pit = self.MinimaxAlphaBetaPruning(self.game, player, depth, -math.inf, math.inf)
        print(f"Computer {player} chooses pit {best_pit}")
        pit=self.game.state.doMove(player, best_pit)

        # Visualize the updated game state
        self.renderGameState()
        pygame.display.flip()
        pygame.time.delay(500) 

    def MinimaxAlphaBetaPruning(self, game, player, depth, alpha, beta):
        if game.gameOver() or depth == 1:
            bestValue = game.evaluate(player)
            return bestValue, None

        if player == 1:  
            best_value = -math.inf
            best_pit = None

            for pit in game.state.possible_moves(game.player_side["COMPUTER1"]):
                child_game = copy.deepcopy(game)
                child_game.state.doMove(game.player_side["COMPUTER1"], pit)
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

            for pit in game.state.possible_moves(game.player_side["COMPUTER2"]):
                child_game = copy.deepcopy(game)
                child_game.state.doMove(game.player_side["COMPUTER2"], pit)
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
   
    # Convert the input to an integer

    game = Game()
    play = Play(game)

    play.renderGameState()  # Initial game state visualization

    while not game.gameOver():
        play.computerTurn(1)
        if game.gameOver():
            break
        play.computerTurn(2)

    play.render_game_over()
    pygame.quit()
    sys.exit()
