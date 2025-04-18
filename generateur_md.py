import tkinter as tk
from tkinter import filedialog, messagebox

def detect_markdown_from_text(text, title, rules):
    lines = text.strip().split('\n')
    output = [f"# {title.strip()}"] if title.strip() else []

    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        matched = False
        for keyword, style_tag in rules:
            if clean.lower().startswith(keyword.lower()):
                output.append(f"{style_tag} {clean}")
                matched = True
                break
        if not matched:
            output.append(clean)
    return "\n\n".join(output)

def generate_md():
    title = entry_title.get().strip()
    raw_text = text_area.get("1.0", tk.END).strip()

    if not raw_text:
        messagebox.showwarning("Avertissement", "Le champ de texte est vide.")
        return

    rules = []
    for frame in keyword_frames:
        keyword = frame['keyword'].get().strip()
        style = frame['style'].get().strip()
        if keyword and style:
            rules.append((keyword, style))

    if not rules:
        messagebox.showwarning("Avertissement", "Tu dois ajouter au moins une règle.")
        return

    processed_text = detect_markdown_from_text(raw_text, title, rules)

    file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
    if not file_path:
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(processed_text)

    messagebox.showinfo("Succès", f"Fichier .md enregistré :\n{file_path}")

def add_rule_field():
    frame = tk.Frame(frame_rules_inner)
    frame.pack(pady=2)

    tk.Label(frame, text="Mot-clé").pack(side=tk.LEFT)
    keyword_entry = tk.Entry(frame, width=20)
    keyword_entry.pack(side=tk.LEFT, padx=(5, 15))

    tk.Label(frame, text="Style").pack(side=tk.LEFT)
    style_entry = tk.Entry(frame, width=10)
    style_entry.pack(side=tk.LEFT, padx=5)

    keyword_frames.append({'frame': frame, 'keyword': keyword_entry, 'style': style_entry})

root = tk.Tk()
#root.overrideredirect(True)
root.title("Générateur Markdown multi-règles")

window_width = 900
window_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_centre = int((screen_width - window_width) / 2)
y_centre = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x_centre}+{y_centre}")

# Faire apparaître devant au démarrage, mais pas bloqué devant
root.lift()
root.after(100, lambda: root.focus_force())
root.after(200, lambda: root.attributes("-topmost", False))

tk.Label(root, text="Titre du livre").pack(pady=(10, 0))
entry_title = tk.Entry(root, font=("Arial", 12), width=80)
entry_title.pack(pady=(0, 10))

# FRAME PRINCIPALE (scrollable + contenu)
canvas_frame = tk.Frame(root)
canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(canvas_frame, bd=0, highlightthickness=0)
scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scrollable_frame = tk.Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# CONTENU DANS LE SCROLLABLE FRAME
frame_rules_inner = tk.Frame(scrollable_frame)
frame_rules_inner.pack()

keyword_frames = []
add_rule_field()  # champ par défaut

tk.Button(scrollable_frame, text="➕ Ajouter une règle", command=add_rule_field).pack(pady=5)
tk.Label(scrollable_frame, text="Colle ici ton texte brut :").pack(pady=5)

# ZONE DE TEXTE AVEC SCROLL
frame_text_area = tk.Frame(scrollable_frame)
frame_text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

text_scroll_y = tk.Scrollbar(frame_text_area, orient=tk.VERTICAL)
text_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

text_area = tk.Text(
    frame_text_area,
    wrap=tk.WORD,
    font=("Arial", 12),
    bd=0,
    highlightthickness=0,
    yscrollcommand=text_scroll_y.set
)
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text_scroll_y.config(command=text_area.yview)

# FOOTER FIXÉ EN BAS
frame_footer = tk.Frame(root)
frame_footer.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

tk.Button(frame_footer, text="💾 Générer le fichier .md", command=generate_md).pack(pady=5)

root.mainloop()
