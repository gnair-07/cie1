import os
import tkinter as tk
from tkinter import messagebox

from registration import RegistrationPage


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management - Login")
        self.root.resizable(False, False)
        self.show()

    def show(self):
        frame = tk.Frame(self.root, padx=24, pady=20)
        frame.pack()
        tk.Label(frame, text="Staff Login", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 12)
        )

        self.username = tk.Entry(frame, width=28)
        self.password = tk.Entry(frame, width=28, show="*")
        for row, (label, entry) in enumerate(
            (("Username", self.username), ("Password", self.password)), start=1
        ):
            tk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=5)
            entry.grid(row=row, column=1, padx=(10, 0), pady=5)

        self.password.bind("<Return>", lambda _event: self.login())
        tk.Button(frame, text="Sign in", command=self.login, width=14).grid(
            row=3, column=0, columnspan=2, pady=(12, 0)
        )

    def login(self):
        username = os.environ.get("HOSPITAL_USER", "admin")
        password = os.environ.get("HOSPITAL_PASSWORD", "admin123")
        if self.username.get() != username or self.password.get() != password:
            messagebox.showerror("Login failed", "Invalid username or password.")
            return

        for widget in self.root.winfo_children():
            widget.destroy()
        RegistrationPage(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()
