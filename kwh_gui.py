
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ---------- WINDOW ----------
window = tk.Tk()
window.title("KWH Calculator")
window.geometry("720x760")
window.minsize(560, 650)
window.configure(bg="#f3f6fb")

# ---------- COLORS ----------
BG = "#f3f6fb"
CARD = "#ffffff"
TEXT = "#172033"
MUTED = "#68758a"
BLUE = "#2563eb"
GREEN = "#087f5b"
BORDER = "#dce4ef"

# ---------- THEME ----------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Modern.TEntry",
    padding=10,
    font=("Segoe UI", 11),
    fieldbackground=CARD,
    foreground=TEXT,
    bordercolor=BORDER,
    lightcolor=BORDER,
    darkcolor=BORDER
)

style.configure(
    "Modern.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=(18, 12),
    background=BLUE,
    foreground="white",
    borderwidth=0
)

style.map(
    "Modern.TButton",
    background=[("active", "#1d4ed8"), ("pressed", "#1e40af")],
    foreground=[("active", "white")]
)

# ---------- RESPONSIVE LAYOUT ----------
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

main = tk.Frame(window, bg=BG, padx=24, pady=22)
main.grid(row=0, column=0, sticky="nsew")
main.grid_columnconfigure(0, weight=1)
main.grid_rowconfigure(2, weight=1)

# ---------- HEADER ----------
header = tk.Frame(main, bg=BG)
header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
header.grid_columnconfigure(0, weight=1)

tk.Label(
    header,
    text="KWH Calculator",
    font=("Segoe UI", 23, "bold"),
    bg=BG,
    fg=TEXT
).grid(row=0, column=0, sticky="w")

tk.Label(
    header,
    text="Electricity meter reading estimator",
    font=("Segoe UI", 11),
    bg=BG,
    fg=MUTED
).grid(row=1, column=0, sticky="w", pady=(4, 0))

# ---------- INPUT CARD ----------
input_card = tk.Frame(
    main,
    bg=CARD,
    padx=22,
    pady=20,
    highlightbackground=BORDER,
    highlightthickness=1
)
input_card.grid(row=1, column=0, sticky="ew", pady=(0, 16))
input_card.grid_columnconfigure(0, weight=1)

tk.Label(
    input_card,
    text="READING DETAILS",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=MUTED
).grid(row=0, column=0, sticky="w", pady=(0, 15))

form = tk.Frame(input_card, bg=CARD)
form.grid(row=1, column=0, sticky="ew")
form.grid_columnconfigure(0, weight=1)
form.grid_columnconfigure(1, weight=1)

def create_input(label_text, row, column, parent=form):
    field = tk.Frame(parent, bg=CARD)
    field.grid(
        row=row,
        column=column,
        sticky="ew",
        padx=(0, 10) if column == 0 else (10, 0),
        pady=(0, 15)
    )
    field.grid_columnconfigure(0, weight=1)

    tk.Label(
        field,
        text=label_text,
        font=("Segoe UI", 10),
        bg=CARD,
        fg=TEXT
    ).grid(row=0, column=0, sticky="w", pady=(0, 7))

    entry = ttk.Entry(field, style="Modern.TEntry")
    entry.grid(row=1, column=0, sticky="ew")
    return entry

previous_date_input = create_input(
    "Previous reading date (DD.MM.YYYY)", 0, 0
)
previous_kwh_input = create_input(
    "Previous meter reading (KWH)", 0, 1
)
current_date_input = create_input(
    "Latest reading date (DD.MM.YYYY)", 1, 0
)
current_kwh_input = create_input(
    "Latest meter reading (KWH)", 1, 1
)
target_date_input = create_input(
    "Date to estimate (DD.MM.YYYY)", 2, 0
)

# Example defaults to make testing easier
previous_date_input.insert(0, "20.05.2025")
previous_kwh_input.insert(0, "12000")
current_date_input.insert(0, "25.10.2026")
current_kwh_input.insert(0, "16342")
target_date_input.insert(0, "30.10.2026")

# ---------- RESULTS CARD ----------
result_card = tk.Frame(
    main,
    bg=CARD,
    padx=22,
    pady=20,
    highlightbackground=BORDER,
    highlightthickness=1
)
result_card.grid(row=2, column=0, sticky="nsew")
result_card.grid_columnconfigure(0, weight=1)
result_card.grid_rowconfigure(1, weight=1)

tk.Label(
    result_card,
    text="ESTIMATION RESULTS",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=MUTED
).grid(row=0, column=0, sticky="w", pady=(0, 12))

result_label = tk.Label(
    result_card,
    text="Enter your readings and select Calculate.",
    font=("Segoe UI", 11),
    bg=CARD,
    fg=MUTED,
    justify="left",
    anchor="nw",
    wraplength=650,
    padx=0,
    pady=5
)
result_label.grid(row=1, column=0, sticky="nsew")

# ---------- CALCULATION ----------
def calculate():
    try:
        previous_date = datetime.strptime(
            previous_date_input.get().strip(), "%d.%m.%Y"
        )
        current_date = datetime.strptime(
            current_date_input.get().strip(), "%d.%m.%Y"
        )
        target_date = datetime.strptime(
            target_date_input.get().strip(), "%d.%m.%Y"
        )

        previous_kwh = float(
            previous_kwh_input.get().replace(",", "").strip()
        )
        current_kwh = float(
            current_kwh_input.get().replace(",", "").strip()
        )

        if previous_kwh < 0 or current_kwh < 0:
            raise ValueError("Meter readings cannot be negative.")

        if current_kwh < previous_kwh:
            raise ValueError(
                "The latest reading cannot be lower than "
                "the previous reading."
            )

        days_between = (current_date - previous_date).days

        if days_between <= 0:
            raise ValueError(
                "The latest reading date must be after "
                "the previous reading date."
            )

        total_consumption = current_kwh - previous_kwh
        daily_consumption = total_consumption / days_between
        days_to_target = (target_date - current_date).days

        consumption_change = daily_consumption * days_to_target
        estimated_kwh = current_kwh + consumption_change

        if days_to_target < 0:
            direction = "before the latest reading"
        elif days_to_target > 0:
            direction = "after the latest reading"
        else:
            direction = "the latest reading date"

        result_label.config(
            text=(
                f"Historical consumption\n"
                f"{total_consumption:,.2f} KWH over "
                f"{days_between} days\n\n"
                f"Average daily consumption\n"
                f"{daily_consumption:,.2f} KWH per day\n\n"
                f"Target date: {target_date.strftime('%d.%m.%Y')}\n"
                f"{abs(days_to_target)} days {direction}\n"
                f"Estimated change: {consumption_change:+,.2f} KWH"
                f"\n\n"
                f"ESTIMATED METER READING\n"
                f"{estimated_kwh:,.2f} KWH"
            ),
            fg=GREEN
        )

    except ValueError as error:
        messagebox.showerror(
            "Check your inputs",
            str(error) if str(error) in [
                "Meter readings cannot be negative.",
                "The latest reading cannot be lower than "
                "the previous reading.",
                "The latest reading date must be after "
                "the previous reading date."
            ] else (
                "Please enter valid dates in DD.MM.YYYY format "
                "and valid numbers for the meter readings."
            )
        )

# ---------- CALCULATE BUTTON ----------
calculate_button = ttk.Button(
    main,
    text="Calculate estimated reading",
    style="Modern.TButton",
    command=calculate
)
calculate_button.grid(row=3, column=0, sticky="ew", pady=(16, 0))

# ---------- RESIZE RESULT TEXT ----------
def update_result_wrap(event):
    result_label.config(wraplength=max(250, event.width - 45))

result_card.bind("<Configure>", update_result_wrap)

# ---------- START ----------
window.mainloop()
