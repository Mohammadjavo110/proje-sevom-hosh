import copy
import random
import tkinter as tk
from tkinter import messagebox
import json
import os

# --- Game Constants ---
SIZE = 6
BLACK = 1       # AI (Red)
WHITE = -1      # Human (White)
BLACK_KING = 2
WHITE_KING = -2
EMPTY = 0

# --- Colors & Styles ---
BOARD_COLOR_1 = "#E8CCAA"
BOARD_COLOR_2 = "#8B5A2B"
HIGHLIGHT_COLOR = "#00FF7F"
SELECTED_COLOR = "#1E90FF"
HINT_COLOR = "#FFD700"
BG_COLOR = "#2C3E50"
PIECE_RED = "#D32F2F"
PIECE_RED_LIGHT = "#EF5350"
PIECE_WHITE = "#F5F5F5"
PIECE_WHITE_SHADOW = "#BDBDBD"

# --- Logic Class ---
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

# --- AI Class with Learning Mechanism (Stage 6) ---
class AI_Agent:
    def __init__(self, depth=4):
        self.depth = depth
        self.memory_file = "ai_memory.json"
        # Default Weights (Gen 0)
        self.weights = {
            "w_piece": 10.0,
            "w_king": 16.0,
            "w_center": 2.0,
            "w_edge": 1.0,
            "w_advance": 1.0,
            "games_played": 0,
            "wins": 0
        }
        self.load_memory()

    def load_memory(self):
        """Stage 6: Load experience from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.weights.update(data)
                print(f"Memory Loaded! AI has played {self.weights['games_played']} games.")
            except:
                print("Memory file corrupted, starting fresh.")

    def save_memory(self):
        """Stage 6: Save experience to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.weights, f, indent=4)
        print("Memory Saved.")

    def learn_from_game(self, result):
        """
        Stage 6: Modify weights based on game result.
        result: 1 (AI Won), -1 (AI Lost), 0 (Draw)
        """
        self.weights['games_played'] += 1
        learning_rate = 0.5 

        if result == 1:
            self.weights['wins'] += 1
            # Reinforcement: The current strategy worked, slightly amplify key features
            # to make the AI more confident in this playstyle.
            self.weights['w_king'] += learning_rate
            self.weights['w_center'] += (learning_rate / 2)
            print("AI Won! Strengthening weights (Positive Reinforcement).")
        
        elif result == -1:
            # Correction: The current strategy failed. Adjust weights slightly.
            # Maybe we undervalued Kings or overvalued Center?
            # Random perturbation to try to break out of local optima
            self.weights['w_king'] += random.uniform(-1.0, 1.0)
            self.weights['w_center'] += random.uniform(-0.5, 0.5)
            self.weights['w_piece'] += random.uniform(-0.5, 0.5)
            print("AI Lost! Adjusting weights (Correction).")
        
        # Keep weights within sane bounds
        self.weights['w_piece'] = max(5.0, self.weights['w_piece'])
        self.weights['w_king'] = max(10.0, self.weights['w_king'])
        
        self.save_memory()

    def get_move(self, game):
        _, move = self.alpha_beta(game, self.depth, float('-inf'), float('inf'), True)
        return move

    def evaluate(self, game):
        """
        Stage 4 & 6: Evaluation using Learned Weights
        """
        score = 0
        w_p = self.weights['w_piece']
        w_k = self.weights['w_king']
        w_c = self.weights['w_center']
        w_e = self.weights['w_edge']
        w_a = self.weights['w_advance']

        for r in range(SIZE):
            for c in range(SIZE):
                p = game.board[r][c]
                if p == 0: continue
                
                # Base Value
                val = w_p if abs(p) == 1 else w_k
                
                # Positional Features
                if 1 < r < 4 and 1 < c < 4: val += w_c # Center
                if c == 0 or c == 5: val += w_e        # Edge (Safety)
                
                # Advancement
                if p == BLACK: val += (r * w_a)
                else: val += ((5 - r) * w_a)
                
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
        self.root.title("6x6 Checkers AI - With Learning")
        self.root.configure(bg=BG_COLOR)
        
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        w, h = 600, 750
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.main_frame = tk.Frame(root, bg=BG_COLOR)
        self.main_frame.pack(pady=20)

        self.status_label = tk.Label(self.main_frame, text="AI Learning Mode Active", 
                                     font=("Helvetica", 16, "bold"), bg=BG_COLOR, fg="white")
        self.status_label.pack(pady=(0, 10))
        
        self.stats_label = tk.Label(self.main_frame, text="Stats: Loading...", 
                                    font=("Arial", 10), bg=BG_COLOR, fg="#BDC3C7")
        self.stats_label.pack(pady=(0, 10))

        self.cell_size = 80
        board_pixel_size = SIZE * self.cell_size
        self.canvas_frame = tk.Frame(self.main_frame, bg="#4E342E", bd=10, relief=tk.RIDGE)
        self.canvas_frame.pack()
        
        self.canvas = tk.Canvas(self.canvas_frame, width=board_pixel_size, height=board_pixel_size, 
                                highlightthickness=0, bg=BOARD_COLOR_1)
        self.canvas.pack()
        
        self.game = CheckersLogic()
        self.ai = AI_Agent(depth=5)
        
        # Update Stats Display
        self.update_stats_display()

        self.selected_piece = None
        self.valid_moves_cache = []
        self.is_human_turn = False
        self.game_mode = None
        self.animating = False

        self.canvas.bind("<Button-1>", self.click_handler)
        self.select_game_mode()

    def update_stats_display(self):
        w = self.ai.weights
        stats = f"Games: {w['games_played']} | Wins: {w['wins']} | King Weight: {w['w_king']:.2f} | Center Weight: {w['w_center']:.2f}"
        self.stats_label.config(text=stats)

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
        tk.Button(msg_box, text="AI vs AI (Train)", command=set_ai_vs_ai, **btn_style).pack(pady=5)

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
                if c == 0:
                    self.canvas.create_text(x1+10, y1+10, text=str(r), fill="#8D6E63", font=("Arial", 8), tags="square")

    def highlight_square(self, r, c, color, tag="highlight"):
        x1, y1 = c * self.cell_size, r * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        self.canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, outline=color, width=4, tags=tag)

    def draw_pieces(self):
        self.canvas.delete("piece")
        self.canvas.delete("hint")
        self.canvas.delete("highlight")
        
        if self.selected_piece:
            self.highlight_square(*self.selected_piece, SELECTED_COLOR)
        
        if self.selected_piece and self.valid_moves_cache:
             possible_dests = [m['end'] for m in self.valid_moves_cache if m['start'] == self.selected_piece]
             for (r, c) in possible_dests:
                 cx, cy = c*self.cell_size + self.cell_size/2, r*self.cell_size + self.cell_size/2
                 self.canvas.create_oval(cx-8, cy-8, cx+8, cy+8, fill=HINT_COLOR, outline=HIGHLIGHT_COLOR, width=2, tags="hint")

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
        
        self.canvas.create_oval(x+padding+2, y+padding+4, x+self.cell_size-padding+2, y+self.cell_size-padding+4, 
                                fill="black", outline="", stipple="gray50", tags=tag)
        self.canvas.create_oval(x+padding, y+padding, x+self.cell_size-padding, y+self.cell_size-padding, 
                                fill=base_color, outline=shadow_color, width=1, tags=tag)
        self.canvas.create_oval(x+padding+5, y+padding+5, x+self.cell_size-padding-5, y+self.cell_size-padding-5, 
                                fill="", outline=shadow_color, width=2, tags=tag)
        self.canvas.create_oval(x+padding+10, y+padding+10, x+padding+25, y+padding+20, 
                                fill=light_color, outline="", tags=tag)

        if abs(piece) == 2:
            cx, cy = x + self.cell_size/2, y + self.cell_size/2
            self.canvas.create_text(cx, cy, text="♕", font=("Arial", 30, "bold"), fill="gold", tags=tag)

    def process_next_turn(self):
        if self.game.game_over:
            self.handle_game_over()
            return

        turn_text = "AI (Red) is Thinking..." if self.game.turn == BLACK else "Your Turn (White)"
        color_text = PIECE_RED_LIGHT if self.game.turn == BLACK else "white"
        
        if self.game_mode == 'AI_VS_AI' and self.game.turn == WHITE:
            turn_text = "Opponent (White) is Thinking..."
            
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

    def handle_game_over(self):
        """Handle end of game and trigger learning"""
        winner = self.game.winner
        w_txt = "RED WINS!" if winner == BLACK else "WHITE WINS!"
        
        # --- TRIGGER LEARNING ---
        # 1 means AI Win, -1 means AI Loss
        result_for_ai = 1 if winner == BLACK else -1
        self.ai.learn_from_game(result_for_ai)
        self.update_stats_display()
        # ------------------------

        self.status_label.config(text=f"GAME OVER - {w_txt}", fg=HIGHLIGHT_COLOR)
        messagebox.showinfo("Game Over", f"{w_txt}\nAI weights have been updated based on this result.")

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
        current_val = self.game.board[r][c]
        if current_val < 0:
            self.selected_piece = (r, c)
            self.draw_pieces()
            return
        if self.selected_piece:
            chosen_move = None
            for move in self.valid_moves_cache:
                if move['start'] == self.selected_piece and move['end'] == (r, c):
                    chosen_move = move
                    break
            if chosen_move:
                self.selected_piece = None
                self.is_human_turn = False
                self.draw_pieces()
                self.smooth_move_animation(chosen_move)
            elif current_val == 0:
                 self.selected_piece = None
                 self.draw_pieces()

    def smooth_move_animation(self, move):
        self.animating = True
        sr, sc = move['start']
        er, ec = move['end']
        piece = self.game.board[sr][sc]
        self.canvas.delete("piece")
        for r in range(SIZE):
            for c in range(SIZE):
                if (r,c) != (sr, sc) and self.game.board[r][c] != 0:
                    self.draw_single_piece(r, c, self.game.board[r][c])
        self.highlight_square(sr, sc, "yellow", "anim_hl")
        self.highlight_square(er, ec, HIGHLIGHT_COLOR, "anim_hl")
        start_x = sc * self.cell_size
        start_y = sr * self.cell_size
        end_x = ec * self.cell_size
        end_y = er * self.cell_size
        steps = 20
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps
        self.anim_tag = "moving_piece"
        self.draw_single_piece(0, 0, piece, self.anim_tag)
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
