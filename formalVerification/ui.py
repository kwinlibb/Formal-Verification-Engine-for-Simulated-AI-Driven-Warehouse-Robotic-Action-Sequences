import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://127.0.0.1:5000/verify"

def send_sequence():
    sequence = text_input.get("1.0", tk.END).strip()

    if not sequence:
        messagebox.showwarning("Warning", "Please enter an action sequence.")
        return

    try:
        response = requests.post(API_URL, json={"actions": sequence})
        data = response.json()

        # Clear table first
        for row in table.get_children():
            table.delete(row)

        # Fill table with color coding
        for i, item in enumerate(data["validation"]):
            result = item["result"]
            color = "green" if result == "valid" else "red"
            table.insert("", "end", values=(i+1, item["action"], result), tags=(color,))

        table.tag_configure("green", foreground="green")
        table.tag_configure("red", foreground="red")

        # Update summary
        summary_label.config(text=data["summary"])

    except Exception as e:
        messagebox.showerror("Error", f"Could not connect to backend:\n{e}")


root = tk.Tk()
root.title("Formal Verification Engine")
root.geometry("700x550")

# Title
title = tk.Label(root, text="Formal Verification Engine", font=("Arial", 18))
title.pack(pady=10)

# Input
text_input = tk.Text(root, height=5, width=60)
text_input.pack()

btn = tk.Button(root, text="Verify Sequence", command=send_sequence)
btn.pack(pady=10)

# Table with scrollbar
columns = ("step", "action", "result")
frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=20, pady=20)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

table = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
table.heading("step", text="Step")
table.heading("action", text="Action")
table.heading("result", text="Result")
table.pack(fill="both", expand=True)

scrollbar.config(command=table.yview)

# Summary label
summary_label = tk.Label(root, text="No verification yet.", font=("Arial", 14))
summary_label.pack(pady=10)

root.mainloop()
