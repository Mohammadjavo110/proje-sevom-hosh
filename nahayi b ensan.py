# # # import copy
# # # import random

# # # # --- تنظیمات اولیه ---
# # # SIZE = 6
# # # BLACK = 1
# # # WHITE = -1
# # # BLACK_KING = 2
# # # WHITE_KING = -2
# # # EMPTY = 0

# # # class CheckersGame:
# # #     def __init__(self):
# # #         self.board = [[0] * SIZE for _ in range(SIZE)]
# # #         self.turn = BLACK  # سیاه شروع می‌کند
# # #         self.setup_board()
# # #         self.game_over = False
# # #         self.winner = None

# # #     def setup_board(self):
# # #         # چیدمان اولیه طبق صورت سوال
# # #         # سیاه در دو ردیف اول (بالا)، سفید در دو ردیف آخر (پایین)
# # #         for r in range(SIZE):
# # #             for c in range(SIZE):
# # #                 if (r + c) % 2 == 1:  # خانه‌های سیاه
# # #                     if r < 2:
# # #                         self.board[r][c] = BLACK
# # #                     elif r > 3:
# # #                         self.board[r][c] = WHITE

# # #     def print_board(self):
# # #         print("\n   0 1 2 3 4 5")
# # #         print("  " + "-" * 13)
# # #         for r in range(SIZE):
# # #             row_str = f"{r}| "
# # #             for c in range(SIZE):
# # #                 p = self.board[r][c]
# # #                 char = "."
# # #                 if p == BLACK: char = "b"
# # #                 elif p == WHITE: char = "w"
# # #                 elif p == BLACK_KING: char = "B"
# # #                 elif p == WHITE_KING: char = "W"
# # #                 row_str += char + " "
# # #             print(row_str + "|")
# # #         print("  " + "-" * 13)

# # #     def get_valid_moves(self, player):
# # #         """
# # #         تمام حرکات مجاز را برمی‌گرداند.
# # #         اولویت با خوردن است (قانون خوردن اجباری).
# # #         """
# # #         moves = []
# # #         jumps = []
        
# # #         for r in range(SIZE):
# # #             for c in range(SIZE):
# # #                 p = self.board[r][c]
# # #                 if p != 0 and (p > 0) == (player > 0):
# # #                     # بررسی پرش‌ها (خوردن)
# # #                     piece_jumps = self._get_jumps(r, c, p, set())
# # #                     jumps.extend(piece_jumps)
                    
# # #                     # اگر پرشی پیدا نشده بود، حرکات ساده بررسی شوند
# # #                     # (چون اگر پرشی وجود داشته باشد، حرکات ساده مهم نیستند)
# # #                     if not jumps: 
# # #                         moves.extend(self._get_slides(r, c, p))

# # #         # قانون: اگر پرش (خوردن) وجود دارد، فقط پرش‌ها مجاز هستند
# # #         if jumps:
# # #             # قانون تکمیلی: انتخاب طولانی‌ترین زنجیره خوردن (Max Capture)
# # #             max_len = max(len(j['captured']) for j in jumps)
# # #             return [j for j in jumps if len(j['captured']) == max_len]
        
# # #         return moves

# # #     def _get_slides(self, r, c, piece):
# # #         slides = []
# # #         directions = self._get_directions(piece)
        
# # #         for dr, dc in directions:
# # #             nr, nc = r + dr, c + dc
# # #             if 0 <= nr < SIZE and 0 <= nc < SIZE:
# # #                 if self.board[nr][nc] == EMPTY:
# # #                     # ساختار حرکت
# # #                     slides.append({
# # #                         'start': (r, c),
# # #                         'end': (nr, nc),
# # #                         'captured': [],     # در حرکت ساده مهره‌ای خورده نمی‌شود
# # #                         'path': [(r,c), (nr,nc)]
# # #                     })
# # #         return slides

# # #     def _get_jumps(self, r, c, piece, captured_positions):
# # #         """
# # #         تولید بازگشتی حرکات پرشی (خوردن زنجیره‌ای)
# # #         """
# # #         jumps = []
# # #         directions = self._get_directions(piece)
        
# # #         found_jump = False
# # #         for dr, dc in directions:
# # #             mr, mc = r + dr, c + dc      # خانه میانی (حریف)
# # #             nr, nc = r + 2*dr, c + 2*dc  # خانه مقصد (خالی)
            
# # #             if 0 <= nr < SIZE and 0 <= nc < SIZE:
# # #                 mid_p = self.board[mr][mc]
# # #                 dest_p = self.board[nr][nc]
                
# # #                 # شرط خوردن: وسط حریف باشد، مقصد خالی باشد، قبلا در این زنجیره خورده نشده باشد
# # #                 if mid_p != 0 and (mid_p > 0) != (piece > 0) and \
# # #                    (dest_p == EMPTY or (nr, nc) == (r,c)) and \
# # #                    (mr, mc) not in captured_positions:
                    
# # #                     # شبیه‌سازی موقت برای ادامه زنجیره
# # #                     new_captured = captured_positions | {(mr, mc)}
                    
# # #                     # فراخوانی بازگشتی برای ادامه زنجیره
# # #                     # نکته: مهره فرضی به خانه جدید (nr, nc) رفته است
# # #                     sub_jumps = self._get_jumps(nr, nc, piece, new_captured)
                    
# # #                     if sub_jumps:
# # #                         for sub in sub_jumps:
# # #                             sub['start'] = (r, c) # اصلاح نقطه شروع کل زنجیره
# # #                             sub['captured'] = [(mr, mc)] + sub['captured']
# # #                             sub['path'] = [(r, c)] + sub['path']
# # #                             jumps.append(sub)
# # #                     else:
# # #                         # پایان زنجیره
# # #                         jumps.append({
# # #                             'start': (r, c),
# # #                             'end': (nr, nc),
# # #                             'captured': [(mr, mc)],
# # #                             'path': [(r, c), (nr, nc)]
# # #                         })
# # #                     found_jump = True
        
# # #         return jumps

# # #     def _get_directions(self, piece):
# # #         dirs = []
# # #         is_king = abs(piece) == 2
# # #         # سیاه به سمت پایین (ایندکس زیاد)، سفید به سمت بالا (ایندکس کم)
# # #         if piece > 0 or is_king: # Black or King
# # #             dirs.extend([(1, -1), (1, 1)])
# # #         if piece < 0 or is_king: # White or King
# # #             dirs.extend([(-1, -1), (-1, 1)])
# # #         return dirs

# # #     def make_move(self, move):
# # #         """
# # #         اجرای حرکت روی یک کپی از بازی و برگرداندن شیء جدید بازی
# # #         """
# # #         new_game = copy.deepcopy(self)
# # #         board = new_game.board
        
# # #         sr, sc = move['start']
# # #         er, ec = move['end']
# # #         piece = board[sr][sc]
        
# # #         # حرکت مهره
# # #         board[sr][sc] = EMPTY
# # #         board[er][ec] = piece
        
# # #         # حذف مهره‌های خورده شده
# # #         for cr, cc in move['captured']:
# # #             board[cr][cc] = EMPTY
            
# # #         # ارتقا به شاه (King)
# # #         if piece == BLACK and er == SIZE - 1:
# # #             board[er][ec] = BLACK_KING
# # #         elif piece == WHITE and er == 0:
# # #             board[er][ec] = WHITE_KING
            
# # #         new_game.turn = -self.turn # تغییر نوبت
# # #         new_game.check_game_over()
# # #         return new_game

# # #     def check_game_over(self):
# # #         # اگر بازیکنی که نوبتش است حرکت نداشته باشد یا مهره نداشته باشد
# # #         moves = self.get_valid_moves(self.turn)
# # #         if not moves:
# # #             self.game_over = True
# # #             self.winner = -self.turn # برنده حریف است

# # # # --- کلاس هوش مصنوعی ---

# # # class AI_Agent:
# # #     def __init__(self, depth=3, use_pruning=True):
# # #         self.depth = depth
# # #         self.use_pruning = use_pruning
# # #         self.nodes_visited = 0

# # #     def get_move(self, game):
# # #         self.nodes_visited = 0
# # #         if self.use_pruning:
# # #             score, move = self.alpha_beta(game, self.depth, float('-inf'), float('inf'), True)
# # #             alg_name = "Alpha-Beta"
# # #         else:
# # #             score, move = self.minimax(game, self.depth, True)
# # #             alg_name = "Minimax"
            
# # #         print(f"AI ({alg_name}) Depth: {self.depth}, Nodes: {self.nodes_visited}, Score: {score:.2f}")
# # #         return move

# # #     def evaluate(self, game):
# # #         """
# # #         تابع ارزیابی (Heuristic)
# # #         امتیاز مثبت به نفع سیاه (AI)، منفی به نفع سفید
# # #         """
# # #         score = 0
# # #         board = game.board
# # #         total_black = 0
# # #         total_white = 0
        
# # #         for r in range(SIZE):
# # #             for c in range(SIZE):
# # #                 p = board[r][c]
# # #                 if p == 0: continue
                
# # #                 # 1. ارزش مهره (شاه ارزش بیشتر)
# # #                 val = 10 if abs(p) == 1 else 15
                
# # #                 # 2. موقعیت مکانی (کنترل مرکز)
# # #                 if 1 < r < 4 and 1 < c < 4:
# # #                     val += 2
                
# # #                 # 3. امنیت (دیوارها)
# # #                 if c == 0 or c == 5:
# # #                     val += 1
                
# # #                 # 4. پیشروی (برای مهره‌های عادی)
# # #                 if p == BLACK: val += r 
# # #                 if p == WHITE: val += (5 - r)

# # #                 if p > 0: score += val; total_black += 1
# # #                 else: score -= val; total_white += 1
        
# # #         # برد/باخت قطعی ارزش بی‌نهایت دارد
# # #         if total_white == 0: return 10000
# # #         if total_black == 0: return -10000
        
# # #         return score

# # #     def minimax(self, game, depth, is_maximizing):
# # #         self.nodes_visited += 1
# # #         if depth == 0 or game.game_over:
# # #             return self.evaluate(game), None

# # #         # تعیین بازیکن فعلی بر اساس سطح درخت (AI همیشه Maximizer فرض شده در اینجا)
# # #         current_player = BLACK if is_maximizing else WHITE
# # #         possible_moves = game.get_valid_moves(current_player)

# # #         if not possible_moves:
# # #             return self.evaluate(game), None

# # #         best_move = random.choice(possible_moves) # انتخاب تصادفی در شرایط مساوی

# # #         if is_maximizing:
# # #             max_eval = float('-inf')
# # #             for move in possible_moves:
# # #                 new_game = game.make_move(move)
# # #                 # در مرحله بعد نوبت حریف است (minimizing)
# # #                 eval_val, _ = self.minimax(new_game, depth-1, False)
# # #                 if eval_val > max_eval:
# # #                     max_eval = eval_val
# # #                     best_move = move
# # #             return max_eval, best_move
# # #         else:
# # #             min_eval = float('inf')
# # #             for move in possible_moves:
# # #                 new_game = game.make_move(move)
# # #                 eval_val, _ = self.minimax(new_game, depth-1, True)
# # #                 if eval_val < min_eval:
# # #                     min_eval = eval_val
# # #                     best_move = move
# # #             return min_eval, best_move

# # #     def alpha_beta(self, game, depth, alpha, beta, is_maximizing):
# # #         self.nodes_visited += 1
# # #         if depth == 0 or game.game_over:
# # #             return self.evaluate(game), None

# # #         current_player = BLACK if is_maximizing else WHITE
# # #         possible_moves = game.get_valid_moves(current_player)
        
# # #         if not possible_moves:
# # #              return self.evaluate(game), None

# # #         # مرتب‌سازی حرکات برای بهینه‌سازی هرس (Moves ordering)
# # #         # اینجا اولویت با حرکاتی است که مهره می‌خورند
# # #         possible_moves.sort(key=lambda m: len(m['captured']), reverse=True)
# # #         best_move = possible_moves[0]

# # #         if is_maximizing:
# # #             max_eval = float('-inf')
# # #             for move in possible_moves:
# # #                 new_game = game.make_move(move)
# # #                 eval_val, _ = self.alpha_beta(new_game, depth-1, alpha, beta, False)
# # #                 if eval_val > max_eval:
# # #                     max_eval = eval_val
# # #                     best_move = move
# # #                 alpha = max(alpha, eval_val)
# # #                 if beta <= alpha:
# # #                     break # هرس بتا
# # #             return max_eval, best_move
# # #         else:
# # #             min_eval = float('inf')
# # #             for move in possible_moves:
# # #                 new_game = game.make_move(move)
# # #                 eval_val, _ = self.alpha_beta(new_game, depth-1, alpha, beta, True)
# # #                 if eval_val < min_eval:
# # #                     min_eval = eval_val
# # #                     best_move = move
# # #                 beta = min(beta, eval_val)
# # #                 if beta <= alpha:
# # #                     break # هرس آلفا
# # #             return min_eval, best_move

# # # # --- بدنه اصلی برنامه ---

# # # def run_match():
# # #     game = CheckersGame()
    
# # #     # تعریف بازیکنان
# # #     # بازیکن سیاه: عامل هوشمند با Alpha-Beta
# # #     ai_bot = AI_Agent(depth=4, use_pruning=True)
    
# # #     # بازیکن سفید: حریف ساده (انتخاب تصادفی) یا عامل هوشمند دیگر
# # #     # برای تست، حریف را تصادفی می‌گذاریم
# # #     print("شروع بازی: سیاه (هوش مصنوعی) در برابر سفید (تصادفی)")
# # #     game.print_board()

# # #     while not game.game_over:
# # #         if game.turn == BLACK:
# # #             # نوبت هوش مصنوعی
# # #             print(">>> نوبت سیاه (AI)...")
# # #             move = ai_bot.get_move(game)
# # #         else:
# # #             # نوبت حریف (سفید)
# # #             print(">>> نوبت سفید (Random)...")
# # #             moves = game.get_valid_moves(WHITE)
# # #             if not moves:
# # #                 print("سفید حرکتی ندارد. باخت.")
# # #                 break
# # #             move = random.choice(moves)
# # #             # برای بازی دو هوش مصنوعی، خط بالا را کامنت کنید و از کلاس AI استفاده کنید
        
# # #         # انجام حرکت
# # #         print(f"حرکت انجام شد: از {move['start']} به {move['end']}")
# # #         if move['captured']:
# # #             print(f"مهره‌های خورده شده: {move['captured']}")
            
# # #         game = game.make_move(move)
# # #         game.print_board()
# # #         # input("Press Enter for next turn...") # برای مشاهده گام به گام فعال کنید

# # #     print("\n--- پایان بازی ---")
# # #     if game.winner == BLACK:
# # #         print("برنده: سیاه (AI)")
# # #     elif game.winner == WHITE:
# # #         print("برنده: سفید")
# # #     else:
# # #         print("تساوی")

# # # if __name__ == "__main__":
# # #     run_match()
# # import copy
# # import random

# # SIZE = 6
# # BLACK = 1
# # WHITE = -1
# # BLACK_KING = 2
# # WHITE_KING = -2
# # EMPTY = 0

# # class CheckersGame:
# #     def __init__(self):
# #         self.board = [[0] * SIZE for _ in range(SIZE)]
# #         self.turn = BLACK
# #         self.setup_board()
# #         self.game_over = False
# #         self.winner = None

# #     def setup_board(self):
# #         for r in range(SIZE):
# #             for c in range(SIZE):
# #                 if (r + c) % 2 == 1:
# #                     if r < 2:
# #                         self.board[r][c] = BLACK
# #                     elif r > 3:
# #                         self.board[r][c] = WHITE

# #     def print_board(self):
# #         print("\n   0 1 2 3 4 5")
# #         print("  " + "-" * 13)
# #         for r in range(SIZE):
# #             row_str = f"{r}| "
# #             for c in range(SIZE):
# #                 p = self.board[r][c]
# #                 char = "."
# #                 if p == BLACK: char = "b"
# #                 elif p == WHITE: char = "w"
# #                 elif p == BLACK_KING: char = "B"
# #                 elif p == WHITE_KING: char = "W"
# #                 row_str += char + " "
# #             print(row_str + "|")
# #         print("  " + "-" * 13)

# #     def get_valid_moves(self, player):
# #         moves = []
# #         jumps = []
        
# #         for r in range(SIZE):
# #             for c in range(SIZE):
# #                 p = self.board[r][c]
# #                 if p != 0 and (p > 0) == (player > 0):
# #                     piece_jumps = self._get_jumps(r, c, p, set())
# #                     jumps.extend(piece_jumps)
                    
# #                     if not jumps: 
# #                         moves.extend(self._get_slides(r, c, p))

# #         if jumps:
# #             max_len = max(len(j['captured']) for j in jumps)
# #             return [j for j in jumps if len(j['captured']) == max_len]
        
# #         return moves

# #     def _get_slides(self, r, c, piece):
# #         slides = []
# #         directions = self._get_directions(piece)
        
# #         for dr, dc in directions:
# #             nr, nc = r + dr, c + dc
# #             if 0 <= nr < SIZE and 0 <= nc < SIZE:
# #                 if self.board[nr][nc] == EMPTY:
# #                     slides.append({
# #                         'start': (r, c),
# #                         'end': (nr, nc),
# #                         'captured': [],
# #                         'path': [(r,c), (nr,nc)]
# #                     })
# #         return slides

# #     def _get_jumps(self, r, c, piece, captured_positions):
# #         jumps = []
# #         directions = self._get_directions(piece)
        
# #         found_jump = False
# #         for dr, dc in directions:
# #             mr, mc = r + dr, c + dc
# #             nr, nc = r + 2*dr, c + 2*dc
            
# #             if 0 <= nr < SIZE and 0 <= nc < SIZE:
# #                 mid_p = self.board[mr][mc]
# #                 dest_p = self.board[nr][nc]
                
# #                 if mid_p != 0 and (mid_p > 0) != (piece > 0) and \
# #                    (dest_p == EMPTY or (nr, nc) == (r,c)) and \
# #                    (mr, mc) not in captured_positions:
                    
# #                     new_captured = captured_positions | {(mr, mc)}
                    
# #                     sub_jumps = self._get_jumps(nr, nc, piece, new_captured)
                    
# #                     if sub_jumps:
# #                         for sub in sub_jumps:
# #                             sub['start'] = (r, c)
# #                             sub['captured'] = [(mr, mc)] + sub['captured']
# #                             sub['path'] = [(r, c)] + sub['path']
# #                             jumps.append(sub)
# #                     else:
# #                         jumps.append({
# #                             'start': (r, c),
# #                             'end': (nr, nc),
# #                             'captured': [(mr, mc)],
# #                             'path': [(r, c), (nr, nc)]
# #                         })
# #                     found_jump = True
        
# #         return jumps

# #     def _get_directions(self, piece):
# #         dirs = []
# #         is_king = abs(piece) == 2
# #         if piece > 0 or is_king:
# #             dirs.extend([(1, -1), (1, 1)])
# #         if piece < 0 or is_king:
# #             dirs.extend([(-1, -1), (-1, 1)])
# #         return dirs

# #     def make_move(self, move):
# #         new_game = copy.deepcopy(self)
# #         board = new_game.board
        
# #         sr, sc = move['start']
# #         er, ec = move['end']
# #         piece = board[sr][sc]
        
# #         board[sr][sc] = EMPTY
# #         board[er][ec] = piece
        
# #         for cr, cc in move['captured']:
# #             board[cr][cc] = EMPTY
            
# #         if piece == BLACK and er == SIZE - 1:
# #             board[er][ec] = BLACK_KING
# #         elif piece == WHITE and er == 0:
# #             board[er][ec] = WHITE_KING
            
# #         new_game.turn = -self.turn
# #         new_game.check_game_over()
# #         return new_game

# #     def check_game_over(self):
# #         moves = self.get_valid_moves(self.turn)
# #         if not moves:
# #             self.game_over = True
# #             self.winner = -self.turn

# # class AI_Agent:
# #     def __init__(self, depth=3, use_pruning=True):
# #         self.depth = depth
# #         self.use_pruning = use_pruning
# #         self.nodes_visited = 0

# #     def get_move(self, game):
# #         self.nodes_visited = 0
# #         if self.use_pruning:
# #             score, move = self.alpha_beta(game, self.depth, float('-inf'), float('inf'), True)
# #             alg_name = "Alpha-Beta"
# #         else:
# #             score, move = self.minimax(game, self.depth, True)
# #             alg_name = "Minimax"
            
# #         print(f"AI ({alg_name}) Depth: {self.depth}, Nodes: {self.nodes_visited}, Score: {score:.2f}")
# #         return move

# #     def evaluate(self, game):
# #         score = 0
# #         board = game.board
# #         total_black = 0
# #         total_white = 0
        
# #         for r in range(SIZE):
# #             for c in range(SIZE):
# #                 p = board[r][c]
# #                 if p == 0: continue
                
# #                 val = 10 if abs(p) == 1 else 15
                
# #                 if 1 < r < 4 and 1 < c < 4:
# #                     val += 2
                
# #                 if c == 0 or c == 5:
# #                     val += 1
                
# #                 if p == BLACK: val += r 
# #                 if p == WHITE: val += (5 - r)

# #                 if p > 0: score += val; total_black += 1
# #                 else: score -= val; total_white += 1
        
# #         if total_white == 0: return 10000
# #         if total_black == 0: return -10000
        
# #         return score

# #     def minimax(self, game, depth, is_maximizing):
# #         self.nodes_visited += 1
# #         if depth == 0 or game.game_over:
# #             return self.evaluate(game), None

# #         current_player = BLACK if is_maximizing else WHITE
# #         possible_moves = game.get_valid_moves(current_player)

# #         if not possible_moves:
# #             return self.evaluate(game), None

# #         best_move = random.choice(possible_moves)

# #         if is_maximizing:
# #             max_eval = float('-inf')
# #             for move in possible_moves:
# #                 new_game = game.make_move(move)
# #                 eval_val, _ = self.minimax(new_game, depth-1, False)
# #                 if eval_val > max_eval:
# #                     max_eval = eval_val
# #                     best_move = move
# #             return max_eval, best_move
# #         else:
# #             min_eval = float('inf')
# #             for move in possible_moves:
# #                 new_game = game.make_move(move)
# #                 eval_val, _ = self.minimax(new_game, depth-1, True)
# #                 if eval_val < min_eval:
# #                     min_eval = eval_val
# #                     best_move = move
# #             return min_eval, best_move

# #     def alpha_beta(self, game, depth, alpha, beta, is_maximizing):
# #         self.nodes_visited += 1
# #         if depth == 0 or game.game_over:
# #             return self.evaluate(game), None

# #         current_player = BLACK if is_maximizing else WHITE
# #         possible_moves = game.get_valid_moves(current_player)
        
# #         if not possible_moves:
# #              return self.evaluate(game), None

# #         possible_moves.sort(key=lambda m: len(m['captured']), reverse=True)
# #         best_move = possible_moves[0]

# #         if is_maximizing:
# #             max_eval = float('-inf')
# #             for move in possible_moves:
# #                 new_game = game.make_move(move)
# #                 eval_val, _ = self.alpha_beta(new_game, depth-1, alpha, beta, False)
# #                 if eval_val > max_eval:
# #                     max_eval = eval_val
# #                     best_move = move
# #                 alpha = max(alpha, eval_val)
# #                 if beta <= alpha:
# #                     break
# #             return max_eval, best_move
# #         else:
# #             min_eval = float('inf')
# #             for move in possible_moves:
# #                 new_game = game.make_move(move)
# #                 eval_val, _ = self.alpha_beta(new_game, depth-1, alpha, beta, True)
# #                 if eval_val < min_eval:
# #                     min_eval = eval_val
# #                     best_move = move
# #                 beta = min(beta, eval_val)
# #                 if beta <= alpha:
# #                     break
# #             return min_eval, best_move

# # def run_match():
# #     game = CheckersGame()
# #     ai_bot = AI_Agent(depth=4, use_pruning=True)
    
# #     print("Game Start: Black (AI) vs White (Random)")
# #     game.print_board()

# #     while not game.game_over:
# #         if game.turn == BLACK:
# #             print(">>> Black's Turn (AI)...")
# #             move = ai_bot.get_move(game)
# #         else:
# #             print(">>> White's Turn (Random)...")
# #             moves = game.get_valid_moves(WHITE)
# #             if not moves:
# #                 print("White has no moves. White loses.")
# #                 break
# #             move = random.choice(moves)
        
# #         print(f"Move: {move['start']} -> {move['end']}")
# #         if move['captured']:
# #             print(f"Captured: {move['captured']}")
            
# #         game = game.make_move(move)
# #         game.print_board()

# #     print("\n--- Game Over ---")
# #     if game.winner == BLACK:
# #         print("Winner: Black (AI)")
# #     elif game.winner == WHITE:
# #         print("Winner: White")
# #     else:
# #         print("Draw")

# # if __name__ == "__main__":
# #     run_match()
# import copy
# import random
# import tkinter as tk
# from tkinter import messagebox
# import time

# # --- Game Constants ---
# SIZE = 6
# BLACK = 1       # AI (Red in GUI)
# WHITE = -1      # Random (White in GUI)
# BLACK_KING = 2
# WHITE_KING = -2
# EMPTY = 0

# # --- Logic Class (Same as before) ---
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
#         self.root.title("6x6 Checkers AI")
#         self.cell_size = 80
#         self.canvas = tk.Canvas(root, width=SIZE*self.cell_size, height=SIZE*self.cell_size)
#         self.canvas.pack()
        
#         self.game = CheckersLogic()
#         self.ai = AI_Agent(depth=4)
        
#         self.draw_board()
#         self.root.after(1000, self.game_loop) # Start game loop after 1 second

#     def draw_board(self, last_move=None):
#         self.canvas.delete("all")
#         colors = ["#F0D9B5", "#B58863"] # Light wood, Dark wood colors
        
#         for r in range(SIZE):
#             for c in range(SIZE):
#                 x1, y1 = c * self.cell_size, r * self.cell_size
#                 x2, y2 = x1 + self.cell_size, y1 + self.cell_size
#                 color = colors[(r + c) % 2]
                
#                 # Highlight last move
#                 if last_move and ((r,c) == last_move['start'] or (r,c) == last_move['end']):
#                     color = "#7BFF7B" # Light Green highlight

#                 self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
#                 piece = self.game.board[r][c]
#                 if piece != 0:
#                     self.draw_piece(x1, y1, piece)

#     def draw_piece(self, x, y, piece):
#         padding = 10
#         color = "#D32F2F" if piece > 0 else "#EEEEEE" # Red for AI(Black), White for Random
#         outline = "black"
        
#         self.canvas.create_oval(x+padding, y+padding, x+self.cell_size-padding, y+self.cell_size-padding, 
#                                 fill=color, outline=outline, width=2)
        
#         # Draw King Indicator (Gold Ring)
#         if abs(piece) == 2:
#             self.canvas.create_oval(x+padding+10, y+padding+10, x+self.cell_size-padding-10, 
#                                     y+self.cell_size-padding-10, outline="#FFD700", width=3)

#     def game_loop(self):
#         if self.game.game_over:
#             winner_text = "Red (AI) Wins!" if self.game.winner == BLACK else "White Wins!"
#             messagebox.showinfo("Game Over", winner_text)
#             return

#         move = None
#         if self.game.turn == BLACK:
#             # AI Turn
#             self.root.title("Thinking (AI)...")
#             self.root.update()
#             move = self.ai.get_move(self.game)
#         else:
#             # Random Opponent Turn
#             self.root.title("Opponent Turn...")
#             self.root.update()
#             # Small delay to make it visible
#             time.sleep(1) 
#             moves = self.game.get_valid_moves(WHITE)
#             if not moves:
#                 self.game.game_over = True
#                 self.game.winner = BLACK
#                 self.game_loop()
#                 return
#             move = random.choice(moves)

#         self.game = self.game.make_move(move)
#         self.draw_board(last_move=move)
        
#         # Schedule next turn
#         self.root.after(100, self.game_loop)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CheckersGUI(root)
#     root.mainloop()
import copy
import random
import tkinter as tk
from tkinter import messagebox
import time

# --- Game Constants ---
SIZE = 6
BLACK = 1       # AI (Red in GUI)
WHITE = -1      # Random (White in GUI)
BLACK_KING = 2
WHITE_KING = -2
EMPTY = 0

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
                    if r < 2:
                        self.board[r][c] = BLACK
                    elif r > 3:
                        self.board[r][c] = WHITE

    def get_valid_moves(self, player):
        moves = []
        jumps = []
        for r in range(SIZE):
            for c in range(SIZE):
                p = self.board[r][c]
                if p != 0 and (p > 0) == (player > 0):
                    piece_jumps = self._get_jumps(r, c, p, set())
                    jumps.extend(piece_jumps)
                    if not jumps: 
                        moves.extend(self._get_slides(r, c, p))
        if jumps:
            max_len = max(len(j['captured']) for j in jumps)
            return [j for j in jumps if len(j['captured']) == max_len]
        return moves

    def _get_slides(self, r, c, piece):
        slides = []
        directions = self._get_directions(piece)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < SIZE and 0 <= nc < SIZE:
                if self.board[nr][nc] == EMPTY:
                    slides.append({'start': (r, c), 'end': (nr, nc), 'captured': [], 'path': [(r,c), (nr,nc)]})
        return slides

    def _get_jumps(self, r, c, piece, captured_positions):
        jumps = []
        directions = self._get_directions(piece)
        for dr, dc in directions:
            mr, mc = r + dr, c + dc
            nr, nc = r + 2*dr, c + 2*dc
            if 0 <= nr < SIZE and 0 <= nc < SIZE:
                mid_p = self.board[mr][mc]
                dest_p = self.board[nr][nc]
                if mid_p != 0 and (mid_p > 0) != (piece > 0) and \
                   (dest_p == EMPTY or (nr, nc) == (r,c)) and \
                   (mr, mc) not in captured_positions:
                    new_captured = captured_positions | {(mr, mc)}
                    sub_jumps = self._get_jumps(nr, nc, piece, new_captured)
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
        for cr, cc in move['captured']:
            board[cr][cc] = EMPTY
        if piece == BLACK and er == SIZE - 1: board[er][ec] = BLACK_KING
        elif piece == WHITE and er == 0: board[er][ec] = WHITE_KING
        new_game.turn = -self.turn
        new_game.check_game_over()
        return new_game

    def check_game_over(self):
        moves = self.get_valid_moves(self.turn)
        if not moves:
            self.game_over = True
            self.winner = -self.turn

# --- AI Class ---
class AI_Agent:
    def __init__(self, depth=3):
        self.depth = depth
    
    def get_move(self, game):
        _, move = self.alpha_beta(game, self.depth, float('-inf'), float('inf'), True)
        return move

    def evaluate(self, game):
        score = 0
        board = game.board
        total_b, total_w = 0, 0
        for r in range(SIZE):
            for c in range(SIZE):
                p = board[r][c]
                if p == 0: continue
                val = 10 if abs(p) == 1 else 15
                if 1 < r < 4 and 1 < c < 4: val += 2
                if c == 0 or c == 5: val += 1
                if p == BLACK: val += r
                if p == WHITE: val += (5 - r)
                if p > 0: score += val; total_b += 1
                else: score -= val; total_w += 1
        if total_w == 0: return 10000
        if total_b == 0: return -10000
        return score

    def alpha_beta(self, game, depth, alpha, beta, is_maximizing):
        if depth == 0 or game.game_over:
            return self.evaluate(game), None
        
        current_player = BLACK if is_maximizing else WHITE
        possible_moves = game.get_valid_moves(current_player)
        if not possible_moves: return self.evaluate(game), None
        
        possible_moves.sort(key=lambda m: len(m['captured']), reverse=True)
        best_move = possible_moves[0]

        if is_maximizing:
            max_eval = float('-inf')
            for move in possible_moves:
                new_game = game.make_move(move)
                eval_val, _ = self.alpha_beta(new_game, depth-1, alpha, beta, False)
                if eval_val > max_eval: max_eval = eval_val; best_move = move
                alpha = max(alpha, eval_val)
                if beta <= alpha: break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in possible_moves:
                new_game = game.make_move(move)
                eval_val, _ = self.alpha_beta(new_game, depth-1, alpha, beta, True)
                if eval_val < min_eval: min_eval = eval_val; best_move = move
                beta = min(beta, eval_val)
                if beta <= alpha: break
            return min_eval, best_move

# --- GUI Class ---
class CheckersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("6x6 Checkers AI")
        self.cell_size = 80
        self.canvas = tk.Canvas(root, width=SIZE*self.cell_size, height=SIZE*self.cell_size)
        self.canvas.pack()
        
        self.game = CheckersLogic()
        self.ai = AI_Agent(depth=4)
        
        self.draw_board()
        self.root.after(1000, self.process_next_turn) # Start game logic

    def draw_board(self, highlight_squares=None):
        """
        Redraws the board.
        highlight_squares: List of (r, c) tuples to highlight specifically (e.g. start/end move)
        """
        self.canvas.delete("all")
        colors = ["#F0D9B5", "#B58863"] # Light wood, Dark wood
        
        for r in range(SIZE):
            for c in range(SIZE):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = colors[(r + c) % 2]
                
                # Check for special highlights
                if highlight_squares and (r, c) in highlight_squares:
                    color = "#FFFF00" if (r, c) == highlight_squares[0] else "#7BFF7B" 
                    # Yellow for start, Green for end

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
                piece = self.game.board[r][c]
                if piece != 0:
                    self.draw_piece(x1, y1, piece)

    def draw_piece(self, x, y, piece):
        padding = 10
        color = "#D32F2F" if piece > 0 else "#EEEEEE" # Red for AI, White for Random
        outline = "black"
        
        self.canvas.create_oval(x+padding, y+padding, x+self.cell_size-padding, y+self.cell_size-padding, 
                                fill=color, outline=outline, width=2)
        
        if abs(piece) == 2:
            self.canvas.create_oval(x+padding+10, y+padding+10, x+self.cell_size-padding-10, 
                                    y+self.cell_size-padding-10, outline="#FFD700", width=3)

    def process_next_turn(self):
        """Calculates logic and triggers animation"""
        if self.game.game_over:
            winner_text = "Red (AI) Wins!" if self.game.winner == BLACK else "White Wins!"
            messagebox.showinfo("Game Over", winner_text)
            return

        move = None
        if self.game.turn == BLACK:
            self.root.title("Red (AI) Thinking...")
            self.root.update()
            move = self.ai.get_move(self.game)
        else:
            self.root.title("White Thinking...")
            self.root.update()
            # Simulate thinking time for opponent
            self.root.after(500) 
            moves = self.game.get_valid_moves(WHITE)
            if not moves:
                self.game.game_over = True
                self.game.winner = BLACK
                self.process_next_turn()
                return
            move = random.choice(moves)

        # Start animation sequence
        if move:
            self.animate_move_step_1(move)

    def animate_move_step_1(self, move):
        """Step 1: Highlight the move (Start -> End)"""
        # Show where piece is moving from and to BEFORE moving it
        self.draw_board(highlight_squares=[move['start'], move['end']])
        self.root.update()
        
        # Wait 0.8 seconds so user can see the intent
        self.root.after(800, lambda: self.animate_move_step_2(move))

    def animate_move_step_2(self, move):
        """Step 2: Update board (remove piece, place at new location)"""
        self.game = self.game.make_move(move)
        self.draw_board(highlight_squares=[move['start'], move['end']])
        self.root.update()
        
        # Wait another 0.5 seconds before starting next turn calculation
        self.root.after(500, self.process_next_turn)

if __name__ == "__main__":
    root = tk.Tk()
    app = CheckersGUI(root)
    root.mainloop()
