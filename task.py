import tkinter as tk
from tkinter import messagebox
import random


class NumberGuessingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.best_score = None

        self.title_label = tk.Label(root, text="Number Guessing Game",
                                    font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        self.diff_label = tk.Label(root, text="Choose Difficulty:",
                                   font=("Arial", 14))
        self.diff_label.pack()

        self.diff_var = tk.StringVar(value="Easy (1-10)")
        difficulties = ["Easy (1-10)", "Medium (1-50)",
                        "Hard (1-100)", "Custom"]

        for d in difficulties:
            tk.Radiobutton(root, text=d, variable=self.diff_var, value=d,
                           font=("Arial", 12),
                           command=self.set_range).pack(anchor="w")

        self.custom_entry = tk.Entry(root, font=("Arial", 12))

        self.start_button = tk.Button(root, text="Start Game",
                                      font=("Arial", 12),
                                      command=self.start_game)
        self.start_button.pack(pady=10)

        self.info_label = tk.Label(root, text="", font=("Arial", 12))
        self.info_label.pack()

        self.guess_entry = tk.Entry(root, font=("Arial", 14))
        self.submit_button = tk.Button(root, text="Submit Guess",
                                       font=("Arial", 12),
                                       command=self.check_guess)

        self.low, self.high = 1, 10

    def set_range(self):
        choice = self.diff_var.get()

        if choice == "Easy (1-10)":
            self.low, self.high = 1, 10
            self.custom_entry.pack_forget()

        elif choice == "Medium (1-50)":
            self.low, self.high = 1, 50
            self.custom_entry.pack_forget()

        elif choice == "Hard (1-100)":
            self.low, self.high = 1, 100
            self.custom_entry.pack_forget()

        else:
            self.custom_entry.pack(pady=5)

    def start_game(self):
        choice = self.diff_var.get()

        if choice == "Custom":
            value = self.custom_entry.get()

            if not value.isdigit() or int(value) <= 1:
                messagebox.showerror("Error",
                                     "Enter a valid custom maximum number!")
                return

            self.low, self.high = 1, int(value)

        self.secret = random.randint(self.low, self.high)
        self.attempts = 0

        self.info_label.config(
            text=f"Guess a number between {self.low} and {self.high}"
        )

        self.guess_entry.pack(pady=5)
        self.submit_button.pack()

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

    def check_guess(self):
        guess_text = self.guess_entry.get()

        if not guess_text.isdigit():
            messagebox.showerror("Error", "Enter a valid number!")
            return

        guess = int(guess_text)
        self.attempts += 1

        if guess < self.secret:
            messagebox.showinfo("Hint", "Too Low!")

        elif guess > self.secret:
            messagebox.showinfo("Hint", "Too High!")

        else:
            msg = f"Correct! Attempts: {self.attempts}"

            if self.best_score is None or self.attempts < self.best_score:
                self.best_score = self.attempts
                msg += f" | New Best Score: {self.best_score}"

            messagebox.showinfo("Result", msg)

            self.guess_entry.delete(0, tk.END)
            self.guess_entry.pack_forget()
            self.submit_button.pack_forget()

            self.info_label.config(
                text=f"Game over. Best Score: {self.best_score}. Start again!"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGUI(root)
root.mainloop()
