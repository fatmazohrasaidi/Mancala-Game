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
        """Draw the board, pits, and stores with their seed counts and labels."""
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
        
        # Draw pits and display number of seeds and labels
        positions = self.get_pit_positions()
        for pit, pos in positions.items():
            # Draw the pit
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

    def handle_click(self, pos):
        """Determine which pit (if any) the user clicked on."""
        pits_positions = self.get_pit_positions()
        for pit, center in pits_positions.items():
            if (isinstance(pit, str)  # Exclude stores
                and ((pos[0] - center[0]) ** 2 + (pos[1] - center[1]) ** 2) ** 0.5 <= PIT_RADIUS):
                return pit
        return None

    def humanTurn(self):
        """Handle the human player's turn via mouse click."""
        print("Human's turn")
        possible_moves = self.game.state.possible_moves(self.game.player_side["HUMAN"])
        print("Possible moves:", possible_moves)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    selected_pit = self.handle_click(pos)
                    if selected_pit in possible_moves:
                        self.game.state.doMove(self.game.player_side["HUMAN"], selected_pit)
                        return  # Exit after a valid move
                    else:
                        print("Invalid move. Please choose a valid pit.")
                        
            # Render game state after each attempt
            self.renderGameState()
            pygame.display.flip()
            pygame.time.wait(500)

    def computerTurn(self, depth=3):
        """Handle the computer player's turn."""
        print("Computer's turn")
        _, best_pit = self.MinimaxAlphaBetaPruning(self.game, 1, depth, -math.inf, math.inf)
        print(f"Computer chooses pit {best_pit}")
        self.game.state.doMove(self.game.player_side["COMPUTER"], best_pit)

        # Render the game state after the computer's move
        self.renderGameState()
        pygame.display.flip()  # Ensure the display is updated

        # Optionally, add a delay to show the computer's move clearly
        #pygame.time.wait(500)  # Wait 500 milliseconds (adjust as needed)

    def MinimaxAlphaBetaPruning(self, game, player, depth, alpha, beta):
        """Minimax with Alpha-Beta Pruning to find the best move."""
        if game.gameOver() or depth == 0:
            bestValue = game.evaluate()
            return bestValue, None

        if player == 1:  # Computer's turn
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
                    break

            return best_value, best_pit

        else:  # Human's turn
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
                    break

            return best_value, best_pit

    def draw_start_screen(self):
        """Draw the start screen with options to choose Player 1 or Player 2."""
        screen.fill(BOARD_COLOR)
        
        # Draw buttons
        button_1 = pygame.Rect(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2 - 30, 150, 60)
        button_2 = pygame.Rect(WINDOW_WIDTH // 4+200, WINDOW_HEIGHT // 2 - 30, 150, 60)
        
        pygame.draw.rect(screen, PIT_COLOR, button_1)  # Button for Player 1
        pygame.draw.rect(screen, PIT_COLOR, button_2)  # Button for Player 2
        
        # Render button text
        player_1_text = font.render("Player 1", True, TEXT_COLOR)
        player_2_text = font.render("Player 2", True, TEXT_COLOR)
        screen.blit(player_1_text, (button_1.centerx - player_1_text.get_width() // 2, button_1.centery - player_1_text.get_height() // 2))
        screen.blit(player_2_text, (button_2.centerx - player_2_text.get_width() // 2, button_2.centery - player_2_text.get_height() // 2))
        
        pygame.display.flip()

        # Wait for the player to choose
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_1.collidepoint(pos):
                        return 1  # Player 1 chosen
                    elif button_2.collidepoint(pos):
                        return 2  # Player 2 chosen


# Example usage
if __name__ == "__main__":
    play = Play(None)  # Initialize Play without a game object initially
    chosenPlayer = play.draw_start_screen()
    computerPlayer = 2 if chosenPlayer == 1 else 1
    game = Game(human_side=chosenPlayer, computer_side=computerPlayer)
    play.game = game

    while not game.gameOver():
        play.humanTurn()
        if game.gameOver():
            break
        play.computerTurn()

    play.render_game_over()
    pygame.quit()
    sys.exit()
