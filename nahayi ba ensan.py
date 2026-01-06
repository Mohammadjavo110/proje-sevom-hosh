# import copy
# import random
# import tkinter as tk
# from tkinter import messagebox, simpledialog
# import time

# # --- Game Constants ---
# SIZE = 6
# BLACK = 1       # AI (Red in GUI)
# WHITE = -1      # Human/Random (White in GUI)
# BLACK_KING = 2
# WHITE_KING = -2
# EMPTY = 0

# # --- Logic Class ---
# class CheckersLogic:
#     def __init__(self):
#         self.board = [[0] * SIZE for _ in range(SIZE)]
#         self.turn = BLACK
#         self.setup_board()
#         self.game_over = False
#         self.winner = None

#     def setup_board(self):
#         for r in range(SIZE):
#             for c in range(SIZE):
#                 if (r + c) % 2 == 1:
#                     if r < 2:
#                         self.board[r][c] = BLACK
#                     elif r > 3:
#                         self.board[r][c] = WHITE

#     def get_valid_moves(self, player):
#         moves = []
#         jumps = []
#         for r in range(SIZE):
#             for c in range(SIZE):
#                 p = self.board[r][c]
#                 if p != 0 and (p > 0) == (player > 0):
#                     piece_jumps = self._get_jumps(r, c, p, set())
#                     jumps.extend(piece_jumps)
#                     if not jumps: 
#                         moves.extend(self._get_slides(r, c, p))
#         if jumps:
#             max_len = max(len(j['captured']) for j in jumps)
#             return [j for j in jumps if len(j['captured']) == max_len]
#         return moves

#     def _get_slides(self, r, c, piece):
#         slides = []
#         directions = self._get_directions(piece)
#         for dr, dc in directions:
#             nr, nc = r + dr, c + dc
#             if 0 <= nr < SIZE and 0 <= nc < SIZE:
#                 if self.board[nr][nc] == EMPTY:
#                     slides.append({'start': (r, c), 'end': (nr, nc), 'captured': [], 'path': [(r,c), (nr,nc)]})
#         return slides

#     def _get_jumps(self, r, c, piece, captured_positions):
#         jumps = []
#         directions = self._get_directions(piece)
#         for dr, dc in directions:
#             mr, mc = r + dr, c + dc
#             nr, nc = r + 2*dr, c + 2*dc
#             if 0 <= nr < SIZE and 0 <= nc < SIZE:
#                 mid_p = self.board[mr][mc]
#                 dest_p = self.board[nr][nc]
#                 if mid_p != 0 and (mid_p > 0) != (piece > 0) and \
#                    (dest_p == EMPTY or (nr, nc) == (r,c)) and \
#                    (mr, mc) not in captured_positions:
#                     new_captured = captured_positions | {(mr, mc)}
#                     sub_jumps = self._get_jumps(nr, nc, piece, new_captured)
#                     if sub_jumps:
#                         for sub in sub_jumps:
#                             sub['start'] = (r, c)
#                             sub['captured'] = [(mr, mc)] + sub['captured']
#                             sub['path'] = [(r, c)] + sub['path']
#                             jumps.append(sub)
#                     else:
#                         jumps.append({'start': (r, c), 'end': (nr, nc), 'captured': [(mr, mc)], 'path': [(r, c), (nr, nc)]})
#         return jumps

#     def _get_directions(self, piece):
#         dirs = []
#         is_king = abs(piece) == 2
#         if piece > 0 or is_king: dirs.extend([(1, -1), (1, 1)])
#         if piece < 0 or is_king: dirs.extend([(-1, -1), (-1, 1)])
#         return dirs

#     def make_move(self, move):
#         new_game = copy.deepcopy(self)
#         board = new_game.board
#         sr, sc = move['start']
#         er, ec = move['end']
#         piece = board[sr][sc]
#         board[sr][sc] = EMPTY
#         board[er][ec] = piece
#         for cr, cc in move['captured']:
#             board[cr][cc] = EMPTY
#         if piece == BLACK and er == SIZE - 1: board[er][ec] = BLACK_KING
#         elif piece == WHITE and er == 0: board[er][ec] = WHITE_KING
#         new_game.turn = -self.turn
#         new_game.check_game_over()
#         return new_game

#     def check_game_over(self):
#         moves = self.get_valid_moves(self.turn)
#         if not moves:
#             self.game_over = True
#             self.winner = -self.turn

# # --- AI Class ---
# class AI_Agent:
#     def __init__(self, depth=3):
#         self.depth = depth
    
#     def get_move(self, game):
#         _, move = self.alpha_beta(game, self.depth, float('-inf'), float('inf'), True)
#         return move

#     def evaluate(self, game):
#         score = 0
#         board = game.board
#         total_b, total_w = 0, 0
#         for r in range(SIZE):
#             for c in range(SIZE):
#                 p = board[r][c]
#                 if p == 0: continue
#                 val = 10 if abs(p) == 1 else 15
#                 if 1 < r < 4 and 1 < c < 4: val += 2
#                 if c == 0 or c == 5: val += 1
#                 if p == BLACK: val += r
#                 if p == WHITE: val += (5 - r)
#                 if p > 0: score += val; total_b += 1
#                 else: score -= val; total_w += 1
#         if total_w == 0: return 10000
#         if total_b == 0: return -10000
#         return score

#     def alpha_beta(self, game, depth, alpha, beta, is_maximizing):
#         if depth == 0 or game.game_over:
#             return self.evaluate(game), None
        
#         current_player = BLACK if is_maximizing else WHITE
#         possible_moves = game.get_valid_moves(current_player)
#         if not possible_moves: return self.evaluate(game), None
        
#         possible_moves.sort(key=lambda m: len(m['captured']), reverse=True)
#         best_move = possible_moves[0]

#         if is_maximizing:
#             max_eval = float('-inf')
#             for move in possible_moves:
#                 new_game = game.make_move(move)
#                 eval_val, _ = self.alpha_beta(new_game, depth-1, alpha, beta, False)
#                 if eval_val > max_eval: max_eval = eval_val; best_move = move
#                 alpha = max(alpha, eval_val)
#                 if beta <= alpha: break
#             return max_eval, best_move
#         else:
#             min_eval = float('inf')
#             for move in possible_moves:
#                 new_game = game.make_move(move)
#                 eval_val, _ = self.alpha_beta(new_game, depth-1, alpha, beta, True)
#                 if eval_val < min_eval: min_eval = eval_val; best_move = move
#                 beta = min(beta, eval_val)
#                 if beta <= alpha: break
#             return min_eval, best_move

# # --- GUI Class ---
# class CheckersGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("6x6 Checkers")
#         self.cell_size = 80
#         self.canvas = tk.Canvas(root, width=SIZE*self.cell_size, height=SIZE*self.cell_size)
#         self.canvas.pack()
        
#         # --- Interactive Mode Variables ---
#         self.selected_piece = None # (r, c)
#         self.valid_moves_cache = [] # List of valid moves for current turn
#         self.highlighted_moves = [] # Visual cues for destinations
#         self.is_human_turn = False
#         self.game_mode = None # 'AI_VS_AI' or 'HUMAN_VS_AI'
        
#         self.game = CheckersLogic()
#         self.ai = AI_Agent(depth=4)
        
#         self.canvas.bind("<Button-1>", self.click_handler)
#         self.select_game_mode()

#     def select_game_mode(self):
#         # Create a simple dialog to choose mode
#         msg_box = tk.Toplevel(self.root)
#         msg_box.title("Select Mode")
#         msg_box.geometry("300x150")
        
#         tk.Label(msg_box, text="Choose Game Mode:", font=("Arial", 12)).pack(pady=20)
        
#         def set_mode_human():
#             self.game_mode = 'HUMAN_VS_AI'
#             msg_box.destroy()
#             self.start_game()

#         def set_mode_ai():
#             self.game_mode = 'AI_VS_AI'
#             msg_box.destroy()
#             self.start_game()

#         tk.Button(msg_box, text="Human vs AI (You are White)", command=set_mode_human).pack(side=tk.LEFT, padx=20, pady=20)
#         tk.Button(msg_box, text="AI vs AI (Watch)", command=set_mode_ai).pack(side=tk.RIGHT, padx=20, pady=20)

#     def start_game(self):
#         self.draw_board()
#         self.process_next_turn()

#     def draw_board(self, highlight_squares=None, move_hints=None):
#         self.canvas.delete("all")
#         colors = ["#F0D9B5", "#B58863"] 
        
#         for r in range(SIZE):
#             for c in range(SIZE):
#                 x1, y1 = c * self.cell_size, r * self.cell_size
#                 x2, y2 = x1 + self.cell_size, y1 + self.cell_size
#                 color = colors[(r + c) % 2]
                
#                 # Highlight last move (Yellow/Green)
#                 if highlight_squares and (r, c) in highlight_squares:
#                     color = "#FFFF00" if (r, c) == highlight_squares[0] else "#7BFF7B"
                
#                 # Highlight Selected Piece (Blue)
#                 if self.selected_piece and (r,c) == self.selected_piece:
#                     color = "#6495ED"

#                 self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
#                 # Draw Move Hints (Small dots)
#                 if move_hints and (r,c) in move_hints:
#                      self.canvas.create_oval(x1+30, y1+30, x1+50, y1+50, fill="#00FF00", outline="")

#                 piece = self.game.board[r][c]
#                 if piece != 0:
#                     self.draw_piece(x1, y1, piece)

#     def draw_piece(self, x, y, piece):
#         padding = 10
#         color = "#D32F2F" if piece > 0 else "#EEEEEE" # Red(AI), White(Human)
#         outline = "black"
        
#         self.canvas.create_oval(x+padding, y+padding, x+self.cell_size-padding, y+self.cell_size-padding, 
#                                 fill=color, outline=outline, width=2)
        
#         if abs(piece) == 2:
#             self.canvas.create_oval(x+padding+10, y+padding+10, x+self.cell_size-padding-10, 
#                                     y+self.cell_size-padding-10, outline="#FFD700", width=3)

#     def process_next_turn(self):
#         if self.game.game_over:
#             winner_text = "Red (AI) Wins!" if self.game.winner == BLACK else "White Wins!"
#             messagebox.showinfo("Game Over", winner_text)
#             return

#         if self.game.turn == BLACK:
#             # --- AI TURN ---
#             self.is_human_turn = False
#             self.root.title("Red (AI) Thinking...")
#             self.root.update()
#             # Delay slightly for visual pacing
#             self.root.after(500, self.ai_move_logic)

#         else:
#             # --- WHITE TURN (Human or AI) ---
#             if self.game_mode == 'AI_VS_AI':
#                 self.is_human_turn = False
#                 self.root.title("White (Random) Thinking...")
#                 self.root.update()
#                 self.root.after(500, self.random_move_logic)
#             else:
#                 # Human Turn
#                 self.is_human_turn = True
#                 self.root.title("Your Turn (White) - Click to move")
#                 self.valid_moves_cache = self.game.get_valid_moves(WHITE)
                
#                 # Check for loss condition
#                 if not self.valid_moves_cache:
#                     self.game.game_over = True
#                     self.game.winner = BLACK
#                     self.process_next_turn()

#     def ai_move_logic(self):
#         move = self.ai.get_move(self.game)
#         if move:
#             self.animate_move_step_1(move)
#         else:
#             # AI has no moves, Human wins
#             self.game.game_over = True
#             self.game.winner = WHITE
#             self.process_next_turn()

#     def random_move_logic(self):
#         moves = self.game.get_valid_moves(WHITE)
#         if not moves:
#             self.game.game_over = True
#             self.game.winner = BLACK
#             self.process_next_turn()
#             return
#         move = random.choice(moves)
#         self.animate_move_step_1(move)

#     def click_handler(self, event):
#         if not self.is_human_turn:
#             return

#         col = event.x // self.cell_size
#         row = event.y // self.cell_size
        
#         # 1. Select a piece
#         if (row, col) != self.selected_piece:
#             # Check if this square has a piece belonging to Human (WHITE < 0)
#             piece = self.game.board[row][col]
#             if piece < 0: 
#                 self.selected_piece = (row, col)
#                 # Filter valid moves that start from this piece
#                 possible_destinations = [m['end'] for m in self.valid_moves_cache if m['start'] == (row, col)]
#                 self.draw_board(highlight_squares=None, move_hints=possible_destinations)
#                 return

#         # 2. Move to a destination
#         if self.selected_piece:
#             # Check if clicked square is a valid destination for selected piece
#             chosen_move = None
#             for move in self.valid_moves_cache:
#                 if move['start'] == self.selected_piece and move['end'] == (row, col):
#                     chosen_move = move
#                     break
            
#             if chosen_move:
#                 self.selected_piece = None
#                 self.is_human_turn = False # Disable input during animation
#                 self.animate_move_step_1(chosen_move)
#             else:
#                 # If clicked on empty space or invalid move, deselect if it's not another piece
#                 if self.game.board[row][col] == 0:
#                      self.selected_piece = None
#                      self.draw_board()

#     def animate_move_step_1(self, move):
#         self.draw_board(highlight_squares=[move['start'], move['end']])
#         self.root.update()
#         self.root.after(600, lambda: self.animate_move_step_2(move))

#     def animate_move_step_2(self, move):
#         self.game = self.game.make_move(move)
#         self.draw_board(highlight_squares=[move['start'], move['end']])
#         self.root.update()
#         self.root.after(300, self.process_next_turn)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CheckersGUI(root)
#     root.mainloop()
import copy
import random
import tkinter as tk
from tkinter import messagebox
import math

# --- Game Constants ---
SIZE = 6
BLACK = 1       # AI (Red/Black Style)
WHITE = -1      # Human (White/Cream Style)
BLACK_KING = 2
WHITE_KING = -2
EMPTY = 0

# --- Colors & Styles ---
BOARD_COLOR_1 = "#E8CCAA"  # Light Wood
BOARD_COLOR_2 = "#8B5A2B"  # Dark Wood
HIGHLIGHT_COLOR = "#00FF7F" # Spring Green (Neon glow)
SELECTED_COLOR = "#1E90FF"  # Dodger Blue
HINT_COLOR = "#FFD700"      # Gold
BG_COLOR = "#2C3E50"        # Dark Blue/Grey Background
PIECE_RED = "#D32F2F"       # Deep Red
PIECE_RED_LIGHT = "#EF5350" # Lighter Red for 3D effect
PIECE_WHITE = "#F5F5F5"     # White Smoke
PIECE_WHITE_SHADOW = "#BDBDBD" # Grey for shadow

# --- Logic Class (Core Logic Remains Same) ---
class CheckersLogic:
    def __init__(self):
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.turn = BLACK
        self.setup_board()
        self.game_over = False
        self.winner = None

    def setup_board(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if (r + c) % 2 == 1:
                    if r < 2: self.board[r][c] = BLACK
                    elif r > 3: self.board[r][c] = WHITE

    def get_valid_moves(self, player):
        moves = []
        jumps = []
        for r in range(SIZE):
            for c in range(SIZE):
                p = self.board[r][c]
                if p != 0 and (p > 0) == (player > 0):
                    jumps.extend(self._get_jumps(r, c, p, set()))
                    if not jumps: moves.extend(self._get_slides(r, c, p))
        if jumps:
            max_len = max(len(j['captured']) for j in jumps)
            return [j for j in jumps if len(j['captured']) == max_len]
        return moves

    def _get_slides(self, r, c, piece):
        slides = []
        dirs = self._get_directions(piece)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < SIZE and 0 <= nc < SIZE and self.board[nr][nc] == EMPTY:
                slides.append({'start': (r, c), 'end': (nr, nc), 'captured': [], 'path': [(r,c), (nr,nc)]})
        return slides

    def _get_jumps(self, r, c, piece, captured):
        jumps = []
        dirs = self._get_directions(piece)
        for dr, dc in dirs:
            mr, mc = r + dr, c + dc
            nr, nc = r + 2*dr, c + 2*dc
            if 0 <= nr < SIZE and 0 <= nc < SIZE:
                mid_p = self.board[mr][mc]
                if mid_p != 0 and (mid_p > 0) != (piece > 0) and \
                   (self.board[nr][nc] == EMPTY or (nr, nc) == (r,c)) and \
                   (mr, mc) not in captured:
                    sub_jumps = self._get_jumps(nr, nc, piece, captured | {(mr, mc)})
                    if sub_jumps:
                        for sub in sub_jumps:
                            sub['start'] = (r, c)
                            sub['captured'] = [(mr, mc)] + sub['captured']
                            sub['path'] = [(r, c)] + sub['path']
                            jumps.append(sub)
                    else:
                        jumps.append({'start': (r, c), 'end': (nr, nc), 'captured': [(mr, mc)], 'path': [(r, c), (nr, nc)]})
        return jumps

    def _get_directions(self, piece):
        dirs = []
        is_king = abs(piece) == 2
        if piece > 0 or is_king: dirs.extend([(1, -1), (1, 1)])
        if piece < 0 or is_king: dirs.extend([(-1, -1), (-1, 1)])
        return dirs

    def make_move(self, move):
        new_game = copy.deepcopy(self)
        board = new_game.board
        sr, sc = move['start']
        er, ec = move['end']
        piece = board[sr][sc]
        board[sr][sc] = EMPTY
        board[er][ec] = piece
        for cr, cc in move['captured']: board[cr][cc] = EMPTY
        if piece == BLACK and er == SIZE - 1: board[er][ec] = BLACK_KING
        elif piece == WHITE and er == 0: board[er][ec] = WHITE_KING
        new_game.turn = -self.turn
        new_game.check_game_over()
        return new_game

    def check_game_over(self):
        if not self.get_valid_moves(self.turn):
            self.game_over = True
            self.winner = -self.turn

# --- AI Class ---
class AI_Agent:
    def __init__(self, depth=4): self.depth = depth
    def get_move(self, game):
        _, move = self.alpha_beta(game, self.depth, float('-inf'), float('inf'), True)
        return move
    def evaluate(self, game):
        score = 0
        for r in range(SIZE):
            for c in range(SIZE):
                p = game.board[r][c]
                if p == 0: continue
                val = 10 if abs(p) == 1 else 16
                if 1 < r < 4 and 1 < c < 4: val += 2
                if p == BLACK: val += r
                else: val += (5 - r)
                score += val if p > 0 else -val
        return score
    def alpha_beta(self, game, depth, alpha, beta, is_max):
        if depth == 0 or game.game_over: return self.evaluate(game), None
        moves = game.get_valid_moves(BLACK if is_max else WHITE)
        if not moves: return self.evaluate(game), None
        moves.sort(key=lambda m: len(m['captured']), reverse=True)
        best_move = moves[0]
        if is_max:
            max_eval = float('-inf')
            for m in moves:
                val, _ = self.alpha_beta(game.make_move(m), depth-1, alpha, beta, False)
                if val > max_eval: max_eval, best_move = val, m
                alpha = max(alpha, max_eval)
                if beta <= alpha: break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for m in moves:
                val, _ = self.alpha_beta(game.make_move(m), depth-1, alpha, beta, True)
                if val < min_eval: min_eval, best_move = val, m
                beta = min(beta, min_eval)
                if beta <= alpha: break
            return min_eval, best_move

# --- Advanced GUI Class ---
class CheckersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("6x6 Checkers Pro")
        self.root.configure(bg=BG_COLOR)
        
        # Center Window
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        w, h = 600, 700
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Main Layout
        self.main_frame = tk.Frame(root, bg=BG_COLOR)
        self.main_frame.pack(pady=20)

        # Header / Status Bar
        self.status_label = tk.Label(self.main_frame, text="Welcome to Checkers", 
                                     font=("Helvetica", 16, "bold"), bg=BG_COLOR, fg="white")
        self.status_label.pack(pady=(0, 10))

        # Canvas Setup with Border effect
        self.cell_size = 80
        board_pixel_size = SIZE * self.cell_size
        self.canvas_frame = tk.Frame(self.main_frame, bg="#4E342E", bd=10, relief=tk.RIDGE) # Wooden Frame
        self.canvas_frame.pack()
        
        self.canvas = tk.Canvas(self.canvas_frame, width=board_pixel_size, height=board_pixel_size, 
                                highlightthickness=0, bg=BOARD_COLOR_1)
        self.canvas.pack()
        
        # Game State
        self.game = CheckersLogic()
        self.ai = AI_Agent(depth=5)
        self.selected_piece = None
        self.valid_moves_cache = []
        self.is_human_turn = False
        self.game_mode = None
        
        # Images/Assets placeholders (using pure Tkinter drawing for portability)
        self.animating = False

        self.canvas.bind("<Button-1>", self.click_handler)
        self.select_game_mode()

    def select_game_mode(self):
        msg_box = tk.Toplevel(self.root)
        msg_box.title("Game Mode")
        msg_box.geometry("350x180")
        msg_box.configure(bg=BG_COLOR)
        
        l = tk.Label(msg_box, text="Choose Your Destiny", font=("Verdana", 14, "bold"), bg=BG_COLOR, fg="white")
        l.pack(pady=20)
        
        btn_style = {"font": ("Arial", 11), "width": 15, "bg": "#34495E", "fg": "white", "activebackground": "#1ABC9C"}

        def set_h_vs_ai():
            self.game_mode = 'HUMAN_VS_AI'
            msg_box.destroy()
            self.start_game()

        def set_ai_vs_ai():
            self.game_mode = 'AI_VS_AI'
            msg_box.destroy()
            self.start_game()

        tk.Button(msg_box, text="Human vs AI", command=set_h_vs_ai, **btn_style).pack(pady=5)
        tk.Button(msg_box, text="AI vs AI (Spectate)", command=set_ai_vs_ai, **btn_style).pack(pady=5)

    def start_game(self):
        self.draw_board_background()
        self.draw_pieces()
        self.process_next_turn()

    def draw_board_background(self):
        self.canvas.delete("square")
        for r in range(SIZE):
            for c in range(SIZE):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = BOARD_COLOR_2 if (r + c) % 2 == 1 else BOARD_COLOR_1
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags="square")
                
                # Add coordinate text lightly
                if c == 0:
                    self.canvas.create_text(x1+10, y1+10, text=str(r), fill="#8D6E63", font=("Arial", 8), tags="square")

    def highlight_square(self, r, c, color, tag="highlight"):
        x1, y1 = c * self.cell_size, r * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        # Create a semi-transparent looking rectangle using stipple (optional) or just an outline
        self.canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, outline=color, width=4, tags=tag)

    def draw_pieces(self):
        self.canvas.delete("piece")
        self.canvas.delete("hint")
        self.canvas.delete("highlight")
        
        # 1. Highlights
        if self.selected_piece:
            self.highlight_square(*self.selected_piece, SELECTED_COLOR)
        
        # 2. Hints
        if self.selected_piece and self.valid_moves_cache:
             possible_dests = [m['end'] for m in self.valid_moves_cache if m['start'] == self.selected_piece]
             for (r, c) in possible_dests:
                 cx, cy = c*self.cell_size + self.cell_size/2, r*self.cell_size + self.cell_size/2
                 # Draw a glowing dot
                 self.canvas.create_oval(cx-8, cy-8, cx+8, cy+8, fill=HINT_COLOR, outline=HIGHLIGHT_COLOR, width=2, tags="hint")

        # 3. Pieces
        for r in range(SIZE):
            for c in range(SIZE):
                p = self.game.board[r][c]
                if p != 0:
                    self.draw_single_piece(r, c, p)

    def draw_single_piece(self, r, c, piece, tag="piece"):
        x = c * self.cell_size
        y = r * self.cell_size
        padding = 12
        
        base_color = PIECE_RED if piece > 0 else PIECE_WHITE
        light_color = PIECE_RED_LIGHT if piece > 0 else "#FFFFFF"
        shadow_color = "#8B0000" if piece > 0 else PIECE_WHITE_SHADOW
        
        # Shadow (3D effect bottom right)
        self.canvas.create_oval(x+padding+2, y+padding+4, x+self.cell_size-padding+2, y+self.cell_size-padding+4, 
                                fill="black", outline="", stipple="gray50", tags=tag)
        
        # Main Body
        self.canvas.create_oval(x+padding, y+padding, x+self.cell_size-padding, y+self.cell_size-padding, 
                                fill=base_color, outline=shadow_color, width=1, tags=tag)
        
        # Inner Reflection/Gradient simulated
        self.canvas.create_oval(x+padding+5, y+padding+5, x+self.cell_size-padding-5, y+self.cell_size-padding-5, 
                                fill="", outline=shadow_color, width=2, tags=tag)
        
        # Highlight gloss (Top left)
        self.canvas.create_oval(x+padding+10, y+padding+10, x+padding+25, y+padding+20, 
                                fill=light_color, outline="", tags=tag)

        # King Crown
        if abs(piece) == 2:
            cx, cy = x + self.cell_size/2, y + self.cell_size/2
            self.canvas.create_text(cx, cy, text="♕", font=("Arial", 30, "bold"), fill="gold", tags=tag)

    def process_next_turn(self):
        if self.game.game_over:
            w_txt = "RED WINS!" if self.game.winner == BLACK else "WHITE WINS!"
            self.status_label.config(text=f"GAME OVER - {w_txt}", fg=HIGHLIGHT_COLOR)
            messagebox.showinfo("Game Over", w_txt)
            return

        turn_text = "AI (Red) is Thinking..." if self.game.turn == BLACK else "Your Turn (White)"
        color_text = PIECE_RED_LIGHT if self.game.turn == BLACK else "white"
        
        if self.game_mode == 'AI_VS_AI' and self.game.turn == WHITE:
            turn_text = "AI (White) is Thinking..."
            
        self.status_label.config(text=turn_text, fg=color_text)

        if self.game.turn == BLACK:
            self.is_human_turn = False
            self.root.after(500, self.ai_move_logic)
        else:
            if self.game_mode == 'AI_VS_AI':
                self.is_human_turn = False
                self.root.after(500, self.random_move_logic)
            else:
                self.is_human_turn = True
                self.valid_moves_cache = self.game.get_valid_moves(WHITE)
                if not self.valid_moves_cache:
                    self.game.game_over = True
                    self.game.winner = BLACK
                    self.process_next_turn()

    def ai_move_logic(self):
        move = self.ai.get_move(self.game)
        if move: self.smooth_move_animation(move)
        else:
            self.game.game_over = True
            self.game.winner = WHITE
            self.process_next_turn()

    def random_move_logic(self):
        moves = self.game.get_valid_moves(WHITE)
        if not moves:
            self.game.game_over = True
            self.game.winner = BLACK
            self.process_next_turn()
            return
        move = random.choice(moves)
        self.smooth_move_animation(move)

    def click_handler(self, event):
        if not self.is_human_turn or self.animating: return
        
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        
        # 1. Select
        current_val = self.game.board[r][c]
        if current_val < 0: # Human Piece
            self.selected_piece = (r, c)
            self.draw_pieces()
            return

        # 2. Move
        if self.selected_piece:
            chosen_move = None
            for move in self.valid_moves_cache:
                if move['start'] == self.selected_piece and move['end'] == (r, c):
                    chosen_move = move
                    break
            
            if chosen_move:
                self.selected_piece = None
                self.is_human_turn = False
                self.draw_pieces() # clear highlights
                self.smooth_move_animation(chosen_move)
            elif current_val == 0:
                 self.selected_piece = None
                 self.draw_pieces()

    def smooth_move_animation(self, move):
        """ Animates the piece sliding from start to end """
        self.animating = True
        sr, sc = move['start']
        er, ec = move['end']
        piece = self.game.board[sr][sc]
        
        # Remove piece from logical board temporarily to prevent drawing it static
        # We will draw a temporary "animating piece"
        self.canvas.delete("piece") # Clear all static pieces
        # Draw all pieces EXCEPT the moving one
        for r in range(SIZE):
            for c in range(SIZE):
                if (r,c) != (sr, sc) and self.game.board[r][c] != 0:
                    self.draw_single_piece(r, c, self.game.board[r][c])
        
        # Highlight start/end
        self.highlight_square(sr, sc, "yellow", "anim_hl")
        self.highlight_square(er, ec, HIGHLIGHT_COLOR, "anim_hl")

        # Animation Setup
        start_x = sc * self.cell_size
        start_y = sr * self.cell_size
        end_x = ec * self.cell_size
        end_y = er * self.cell_size
        
        steps = 20 # Number of frames
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps
        
        self.anim_tag = "moving_piece"
        
        # Create the moving piece object
        self.draw_single_piece(0, 0, piece, self.anim_tag) # Drawn at 0,0 initially
        # Move to start position
        self.canvas.move(self.anim_tag, start_x, start_y)

        def step_anim(count):
            if count < steps:
                self.canvas.move(self.anim_tag, dx, dy)
                self.root.after(15, lambda: step_anim(count + 1))
            else:
                self.finish_move(move)

        step_anim(0)

    def finish_move(self, move):
        self.canvas.delete("anim_hl")
        self.canvas.delete(self.anim_tag)
        self.game = self.game.make_move(move)
        self.animating = False
        self.draw_pieces()
        self.root.after(200, self.process_next_turn)

if __name__ == "__main__":
    root = tk.Tk()
    app = CheckersGUI(root)
    root.mainloop()
