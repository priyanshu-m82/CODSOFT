import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe - With AI")
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.buttons = [tk.Button(master, text=" ", font='Arial 20 bold', width=5, height=2,
                                  command=lambda i=i: self.player_move(i)) for i in range(9)]
        self.score = {'X': 0, 'O': 0, 'tie': 0}
        self.first_player = tk.StringVar(value="X")
        self.create_widgets()
        self.start_game()

    def create_widgets(self):
        for i, button in enumerate(self.buttons):
            button.grid(row=i // 3 + 1, column=i % 3)

        # Score display
        self.score_label = tk.Label(self.master, text=self.get_score_text(), font='Arial 12 bold')
        self.score_label.grid(row=0, column=0, columnspan=3)

        # First move option
        tk.Label(self.master, text="First Move:", font='Arial 10').grid(row=4, column=0, pady=10)
        tk.Radiobutton(self.master, text="Player", variable=self.first_player, value="X").grid(row=4, column=1)
        tk.Radiobutton(self.master, text="AI", variable=self.first_player, value="O").grid(row=4, column=2)
        tk.Button(self.master, text="New Game", command=self.start_game).grid(row=5, column=0, columnspan=3, pady=10)

    def get_score_text(self):
        return f"Player (X): {self.score['X']}  |  AI (O): {self.score['O']}  |  Ties: {self.score['tie']}"

    def start_game(self):
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ", bg="SystemButtonFace", state="normal")
        self.current_player = self.first_player.get()
        self.score_label.config(text=self.get_score_text())

        if self.current_player == "O":
            self.master.after(500, self.ai_move)

    def player_move(self, index):
        if self.board[index] == " ":
            self.make_move(index, self.current_player)
            if not self.check_winner():
                self.current_player = "O"
                self.master.after(400, self.ai_move)

    def ai_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i
        self.make_move(best_move, "O")
        self.check_winner()
        self.current_player = "X"

    def make_move(self, index, player):
        self.board[index] = player
        color = "#D1E7DD" if player == "X" else "#F8D7DA"
        self.buttons[index].config(text=player, bg=color)
        self.buttons[index].update()

    def minimax(self, board, depth, is_maximizing):
        winner = self.get_winner(board)
        if winner:
            return {'X': -1, 'O': 1, 'tie': 0}[winner]

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self):
        winner = self.get_winner(self.board)
        if winner:
            self.score[winner] += 1
            self.show_result(f"{'Player' if winner == 'X' else 'AI'} wins!")
            return True
        elif " " not in self.board:
            self.score["tie"] += 1
            self.show_result("It's a tie!")
            return True
        return False

    def get_winner(self, board):
        win_combos = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
        for a, b, c in win_combos:
            if board[a] == board[b] == board[c] != " ":
                return board[a]
        if " " not in board:
            return "tie"
        return None

    def show_result(self, message):
        self.score_label.config(text=self.get_score_text())
        messagebox.showinfo("Game Over", message)
        self.start_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

