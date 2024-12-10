import tkinter as tk
import random
from tkinter import messagebox

class Minesweeper:
    def __init__(self, root, rows=10, cols=10, mines=15):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flags = 0

        self.init_game()
        self.place_mines()
        self.calculate_numbers()

    def init_game(self):
        self.root.title("Minesweeper")
        for row in range(self.rows):
            for col in range(self.cols):
                btn = tk.Button(self.root, text="", width=3, height=1, font=("Arial", 14),
                                command=lambda r=row, c=col: self.reveal_cell(r, c))
                btn.bind("<Button-3>", lambda event, r=row, c=col: self.toggle_flag(r, c))
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn

    def place_mines(self):
        placed_mines = 0
        while placed_mines < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.board[r][c] != -1:
                self.board[r][c] = -1
                placed_mines += 1

    def calculate_numbers(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    continue
                count = 0
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc] == -1:
                        count += 1
                self.board[row][col] = count

    def reveal_cell(self, row, col):
        if self.revealed[row][col]:
            return
        self.revealed[row][col] = True

        if self.board[row][col] == -1:
            self.buttons[row][col].config(text="*", bg="red")
            self.game_over(False)
            return
        elif self.board[row][col] == 0:
            self.buttons[row][col].config(text="", bg="light grey")
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    self.reveal_cell(nr, nc)
        else:
            self.buttons[row][col].config(text=str(self.board[row][col]), bg="light grey")
        
        self.check_win()

    def toggle_flag(self, row, col):
        if self.revealed[row][col]:
            return
        btn = self.buttons[row][col]
        if btn.cget("text") == "F":
            btn.config(text="")
            self.flags -= 1
        else:
            btn.config(text="F", fg="blue")
            self.flags += 1

    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != -1 and not self.revealed[row][col]:
                    return
        self.game_over(True)

    def game_over(self, win):
        if win:
            messagebox.showinfo("Minesweeper", "Congratulations! You win!")
        else:
            messagebox.showinfo("Minesweeper", "Game Over! You hit a mine!")
        self.reset_game()

    def reset_game(self):
        self.root.destroy()
        root = tk.Tk()
        Minesweeper(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()
