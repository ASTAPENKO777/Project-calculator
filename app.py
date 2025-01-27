import tkinter as tk


def on_button_click(char):
    current_text = entry.get()

    if current_text == "Error":
        entry.delete(0, tk.END)
        
    entry.insert(tk.END, char)

def clear():
    entry.delete(0, tk.END)

def calculate():
    try:
        expression = entry.get()

        expression = expression.replace("÷", "/").replace("×", "*")

        result = eval(expression)

        entry.delete(0, tk.END)
        entry.insert(0, str(result))

        history.append(f"{expression} = {result}")
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    if dark_mode:
        root.config(bg="#1e1e1e")
        entry.config(bg="#222222", fg="#00FF00", insertbackground='white')
        control_panel.config(bg="#333333")  
        for button in root.winfo_children():
            if isinstance(button, tk.Button):
                button.config(bg="#333333", fg="#ffffff", activebackground="#555555", activeforeground="#00FF00")
        theme_button.config(bg="#333333", fg="#ffffff", activebackground="#555555")
        history_button.config(bg="#333333", fg="#ffffff", activebackground="#555555") 
    else:
        root.config(bg="#ffffff")
        entry.config(bg="#ffffff", fg="#000000", insertbackground='black')
        control_panel.config(bg="#f1f1f1")  
        for button in root.winfo_children():
            if isinstance(button, tk.Button):
                button.config(bg="#f1f1f1", fg="#000000", activebackground="#cccccc", activeforeground="#000000")
        theme_button.config(bg="#f1f1f1", fg="#000000", activebackground="#dddddd")
        history_button.config(bg="#f1f1f1", fg="#000000", activebackground="#dddddd") 

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Історія обчислень")
    history_window.geometry("400x400")
    
    history_text = tk.Text(history_window, font=("Segoe UI", 14), height=15, width=40, wrap=tk.WORD, bg="#333333", fg="#ffffff", bd=0, insertbackground='white')
    history_text.pack(pady=10)
    
    for item in history:
        history_text.insert(tk.END, item + "\n")
    
    history_text.config(state=tk.DISABLED)  

    copy_button = tk.Button(history_window, text="Копіювати", font=("Segoe UI", 12, "bold"), bg="#333333", fg="#ffffff", activebackground="#555555", command=lambda: copy_history(history_text))
    copy_button.pack(pady=10)

def copy_history(history_text):
    history_text.config(state=tk.NORMAL)
    history_text.select_range(0, tk.END)
    history_text.copy()
    history_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Калькулятор")

root.geometry("400x600")
root.config(bg="#1e1e1e") 

dark_mode = True

entry = tk.Entry(root, font=("Segoe UI", 24), bd=5, relief="flat", justify="right", bg="#222222", fg="#00FF00", insertbackground='white')
entry.grid(row=0, column=0, columnspan=4, pady=20, padx=20, sticky="nsew")

buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("÷", 1, 3),  
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("×", 2, 3),  
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
    ("C", 5, 0, 4) 
]

button_style = {
    "font": ("Segoe UI", 20, "bold"),
    "width": 5,
    "height": 2,
    "bg": "#333333",
    "fg": "#ffffff",
    "activebackground": "#555555", 
    "activeforeground": "#00FF00",
    "relief": "flat",
    "bd": 0,
    "highlightthickness": 0
}

history = []

for (text, row, col, *span) in buttons:
    span = span[0] if span else 1
    if text == "C":
        button = tk.Button(root, text=text, **button_style, command=clear)
    else:
        button = tk.Button(root, text=text, **button_style, 
                           command=lambda t=text: on_button_click(t) if t != "=" else calculate() if t == "=" else None)
    button.grid(row=row, column=col, padx=10, pady=10, columnspan=span, sticky="nsew")

control_panel = tk.Frame(root, bg="#333333")
control_panel.grid(row=0, column=4, rowspan=6, sticky="ns")

theme_button = tk.Button(control_panel, text="🌙", font=("Segoe UI", 18, "bold"), width=3, height=1, bg="#333333", fg="#ffffff", activebackground="#555555", activeforeground="#00FF00", relief="flat", bd=0, highlightthickness=0, command=toggle_theme)
theme_button.grid(row=0, column=0, padx=10, pady=10)

history_button = tk.Button(control_panel, text="📜", font=("Segoe UI", 18, "bold"), width=3, height=1, bg="#333333", fg="#ffffff", activebackground="#555555", activeforeground="#00FF00", relief="flat", bd=0, highlightthickness=0, command=show_history)
history_button.grid(row=1, column=0, padx=10, pady=10)

for i in range(6):
    root.grid_rowconfigure(i, weight=1, uniform="equal")
for i in range(4):
    root.grid_columnconfigure(i, weight=1, uniform="equal")

def on_enter(event):
    if dark_mode: 
        event.widget.config(bg="#555555")
    else:  
        event.widget.config(bg="#cccccc")

def on_leave(event):
    event.widget.config(bg="#333333" if dark_mode else "#f1f1f1")

for button in root.winfo_children():
    if isinstance(button, tk.Button):
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

root.mainloop()
