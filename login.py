import csv
import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


PATIENT_FILE = Path(__file__).with_name("patients.csv")
FIELDS = {
    "patient_id": "Patient ID",
    "name": "Full name",
    "date_of_birth": "Date of birth (YYYY-MM-DD)",
    "phone": "Phone",
    "address": "Address",
    "reason_for_visit": "Reason for visit",
}


class HospitalManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management - Login")
        self.root.resizable(False, False)
        self.show_login()

    def new_form(self, title):
        frame = tk.Frame(self.root, padx=24, pady=20)
        frame.pack()
        tk.Label(frame, text=title, font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 12)
        )
        return frame

    def show_login(self):
        frame = self.new_form("Staff Login")
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
        self.root.title("Hospital Management - Patient Registration")
        self.show_registration()

    def show_registration(self):
        frame = self.new_form("Patient Registration")
        self.entries = {}

        for row, (key, label) in enumerate(FIELDS.items(), start=1):
            tk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=4)
            self.entries[key] = tk.Entry(frame, width=36)
            self.entries[key].grid(row=row, column=1, padx=(10, 0), pady=4)

        row = len(FIELDS) + 1
        tk.Button(frame, text="Save patient", command=self.save_patient).grid(
            row=row, column=0, pady=(12, 0), sticky="w"
        )
        tk.Button(frame, text="Clear", command=self.clear_form).grid(
            row=row, column=1, pady=(12, 0), sticky="e"
        )

    def save_patient(self):
        patient = {key: entry.get().strip() for key, entry in self.entries.items()}
        if not all(patient.values()):
            messagebox.showwarning("Missing information", "Please complete every field.")
            return

        try:
            has_records = PATIENT_FILE.exists() and PATIENT_FILE.stat().st_size > 0
            if has_records:
                with PATIENT_FILE.open("r", newline="", encoding="utf-8") as file:
                    if any(row["patient_id"] == patient["patient_id"] for row in csv.DictReader(file)):
                        messagebox.showerror("Duplicate ID", "This patient ID is already registered.")
                        return

            with PATIENT_FILE.open("a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=tuple(FIELDS))
                if not has_records:
                    writer.writeheader()
                writer.writerow(patient)
        except OSError as error:
            messagebox.showerror("Save failed", f"Could not save patient record: {error}")
            return

        messagebox.showinfo("Saved", "Patient registered successfully.")
        self.clear_form()

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    HospitalManagementApp(root)
    root.mainloop()
