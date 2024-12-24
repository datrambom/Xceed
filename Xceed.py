import json
import os

import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


# noinspection PyTypeChecker
class Xceed(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.output_label = None
        self.calculate_button = None
        self.remaining_days_entry = None
        self.total_work_entry = None
        self.work_done_entry = None
        self.title("Xceed")
        self.geometry("250x400")
        self.resizable(False, False)

        self.total_work_var = ctk.DoubleVar(value=0)
        self.work_done_var = ctk.DoubleVar(value=0)
        self.remaining_days_var = ctk.IntVar(value=0)

        self.create_widgets()
        self.load_session()

    def create_widgets(self):
        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        widget_width = 200

        ctk.CTkLabel(frame, text="Total Weekly Work:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.total_work_entry = ctk.CTkEntry(frame, textvariable=self.total_work_var, width=widget_width)
        self.total_work_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Work Done So Far:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.work_done_entry = ctk.CTkEntry(frame, textvariable=self.work_done_var, width=widget_width)
        self.work_done_entry.grid(row=3, column=0, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(frame, text="Remaining Days:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.remaining_days_entry = ctk.CTkEntry(frame, textvariable=self.remaining_days_var, width=widget_width)
        self.remaining_days_entry.grid(row=5, column=0, padx=5, pady=10, sticky="w")

        self.calculate_button = ctk.CTkButton(frame, text="Calculate", command=self.calculate, width=widget_width)
        self.calculate_button.grid(row=6, column=0, pady=6, padx=5, sticky="w")

        self.output_label = ctk.CTkLabel(frame, text="", wraplength=300, justify="left")
        self.output_label.grid(row=7, column=0, padx=5, pady=10, sticky="w")

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("300x150")

        error_frame = ctk.CTkFrame(error_window, border_width=2, corner_radius=5, fg_color="red")
        error_frame.pack(padx=10, pady=10, fill="both", expand=True)

        error_label = ctk.CTkLabel(error_frame, text=message, text_color="white", wraplength=270, justify="left")
        error_label.pack(padx=10, pady=10)

        close_button = ctk.CTkButton(error_frame, text="Close", command=error_window.destroy)
        close_button.pack(pady=5)

    def calculate(self):
        try:
            total_work = self.total_work_var.get()
            work_done = self.work_done_var.get()
            remaining_days = self.remaining_days_var.get()

            # Validate inputs
            if total_work <= 0 or remaining_days <= 0:
                raise ValueError("Total work and remaining days must be positive numbers.")

            work_left = max(0, (total_work - work_done))
            percentage_done = min(100, (work_done / total_work) * 100)
            daily_work = work_left / remaining_days if remaining_days > 0 else 0

            # Update output
            self.output_label.configure(text=(
                f"Completed: {work_done:.1f} units ({percentage_done:.1f}%)\n"
                f"Remaining: {work_left:.1f} units\n"
                f"Suggested: {daily_work:.1f} units/day"
            ))
            self.save_session()
        except Exception as e:
            self.show_error(str(e))

    def save_session(self):
        # Save the current session data to a file (JSON format)
        session_data = {
            "total_work": self.total_work_var.get(),
            "work_done": self.work_done_var.get(),
            "remaining_days": self.remaining_days_var.get()
        }

        try:
            with open("session_data.json", "w") as file:
                json.dump(session_data, file)
        except Exception as e:
            self.show_error(f"Error saving session: {str(e)}")

    def load_session(self):
        # Load session data from a file (if exists)
        if os.path.exists("session_data.json"):
            try:
                with open("session_data.json", "r") as file:
                    session_data = json.load(file)

                self.total_work_var.set(session_data.get("total_work", 0))
                self.work_done_var.set(session_data.get("work_done", 0))
                self.remaining_days_var.set(session_data.get("remaining_days", 0))

            except Exception as e:
                self.show_error(f"Error loading session: {str(e)}")


if __name__ == "__main__":
    app = Xceed()
    app.mainloop()
