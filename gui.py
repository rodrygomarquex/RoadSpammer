import tkinter as tk
from tkinter import ttk, messagebox
from config import skill_keys, delay, toggle_key
from PIL import Image, ImageTk
import threading
import keyboard
import time
import sys  # Import sys to get the Python version

# Ensure mouse library is imported correctly
try:
    import mouse
except ImportError:
    messagebox.showerror("Erro", "O módulo 'mouse' não está instalado. Por favor, instale-o e tente novamente.")
    sys.exit(1)

active_keys = set()
spamming = False

def spam_key_with_mouse(key):
    while key in active_keys:
        keyboard.press_and_release(key.strip())
        mouse.click("left")
        time.sleep(delay)

def on_key_press(event):
    key = event.name
    if key in skill_keys and key not in active_keys:
        active_keys.add(key)
        threading.Thread(target=spam_key_with_mouse, args=(key,), daemon=True).start()

def on_key_release(event):
    key = event.name
    if key in active_keys:
        active_keys.remove(key)

def start_spammer():
    keyboard.on_press(on_key_press)
    keyboard.on_release(on_key_release)
    messagebox.showinfo("Spammer", "Spammer iniciado! Pressione as teclas configuradas para usar.")

def stop_spammer():
    keyboard.unhook_all()
    active_keys.clear()
    messagebox.showinfo("Spammer", "Spammer parado!")

def toggle_spammer():
    global spamming
    spamming = not spamming
    if spamming:
        start_spammer()
        toggle_button.config(text="Desligar Spammer", style="Red.TButton")
    else:
        stop_spammer()
        toggle_button.config(text="Ligar Spammer", style="Green.TButton")

def update_keys():
    global skill_keys, toggle_key
    new_keys = skill_keys_entry.get().strip()
    new_toggle_key = toggle_key_entry.get().strip()
    if new_keys:
        skill_keys = [key.strip() for key in new_keys.split(',') if key.strip()]
    if new_toggle_key:
        toggle_key = new_toggle_key.strip()
    if not skill_keys:
        messagebox.showerror("Erro", "As teclas configuradas não podem estar vazias!")
        return
    if not toggle_key:
        messagebox.showerror("Erro", "A tecla de ativação/desativação não pode estar vazia!")
        return
    messagebox.showinfo("Configuração", "Teclas atualizadas com sucesso!")

def update_keys_from_checkboxes():
    global skill_keys
    selected_keys = [key for key, var in checkboxes.items() if var.get()]
    if not selected_keys:
        messagebox.showerror("Erro", "Você deve selecionar pelo menos uma tecla para spammar!")
        return
    skill_keys = selected_keys
    toggle_key_input = toggle_key_entry.get().strip()
    if not toggle_key_input:
        messagebox.showerror("Erro", "A tecla de ativação/desativação não pode estar vazia!")
        return
    global toggle_key
    toggle_key = toggle_key_input
    messagebox.showinfo("Configuração", "Teclas atualizadas com sucesso!")

def on_toggle_key_entry_focus(event):
    """Captura a tecla pressionada enquanto o campo de entrada está em foco."""
    def on_key_press(event):
        toggle_key_entry.delete(0, tk.END)  # Limpa o campo de entrada
        toggle_key_entry.insert(0, event.name)  # Insere o nome da tecla pressionada
        global toggle_key
        toggle_key = event.name  # Atualiza a tecla de ativação/desativação
        keyboard.unhook_all()  # Remove o hook após capturar a tecla

    keyboard.on_press(on_key_press)  # Adiciona o hook para capturar a tecla

def monitor_toggle_key():
    """Monitora a tecla de ativação/desativação para alternar o spammer."""
    def on_key_event(event):
        if event.name == toggle_key:  # Verifica se a tecla pressionada é a tecla de ativação/desativação
            toggle_spammer()

    keyboard.on_press(on_key_event)  # Adiciona o hook para monitorar a tecla de ativação/desativação

# Function to change the language
def change_language(event=None):
    selected_language = language_var.get()
    if selected_language == "English":
        messagebox.showinfo("Language", "Language changed to English!")
        # Update text for English (example)
        toggle_button.config(text="Start Spammer")
        stop_button.config(text="Stop Spammer")
        update_button.config(text="Update Keys")
    elif selected_language == "Português (Brasil)":
        messagebox.showinfo("Idioma", "Idioma alterado para Português (Brasil)!")
        # Update text for Portuguese (example)
        toggle_button.config(text="Ligar Spammer")
        stop_button.config(text="Parar Spammer")
        update_button.config(text="Atualizar Teclas")

# Interface gráfica
root = tk.Tk()
root.title("Road Spammer Beta")  # Nome do aplicativo
root.geometry("900x600")  # Ajuste para acomodar o layout moderno
root.resizable(False, False)
root.configure(bg="#2C3E50")  # Restore the dark background color

# Estilo moderno
style = ttk.Style()
style.theme_use("clam")  # Tema moderno
style.configure("TButton", padding=10, relief="flat", background="#1ABC9C", foreground="white", font=("Arial", 10, "bold"))
style.map("TButton", background=[("active", "#16A085")])
style.configure("Green.TButton", background="#1ABC9C", foreground="white")
style.configure("Red.TButton", background="#E74C3C", foreground="white")
style.configure("TLabel", padding=6, font=("Arial", 10), background="#2C3E50", foreground="white")
style.configure("TEntry", padding=5, font=("Arial", 10), fieldbackground="#34495E", foreground="white")
style.configure("TCheckbutton", background="#2C3E50", foreground="white")
style.configure("TFrame", background="#2C3E50")  # Restore the background for TFrame

frame = ttk.Frame(root, padding="20", style="TFrame")  # Aplica o estilo com fundo definido
frame.pack(fill="both", expand=True)

# Adiciona a logo usando Pillow com tamanho ajustado para 50x50
image = Image.open("assets/logo.jpg").resize((50, 50), Image.Resampling.LANCZOS)
logo = ImageTk.PhotoImage(image)
logo_label = ttk.Label(frame, image=logo, anchor="center", background="#2C3E50")  # Restore logo label background
logo_label.grid(row=0, column=0, columnspan=15, pady=10, sticky="nsew")

# Ensure all functional elements are added after the character image to appear in front
logo_label.lift()  # Ensure the logo is in front

# Ensure the title is added with a background
ttk.Label(frame, text="Road Spammer", font=("Arial", 24, "bold"), anchor="center", background="#2C3E50", foreground="#1ABC9C").grid(
    row=1, column=0, columnspan=15, pady=10, sticky="nsew"
)

# Subtítulo with background
ttk.Label(frame, text="Selecione as teclas para spammar:", font=("Arial", 14), background="#2C3E50", foreground="white").grid(
    row=2, column=0, columnspan=15, sticky="w", pady=10
)

# Criação de checkboxes para simular o layout de um teclado (centralizados)
checkboxes = {}
keyboard_layout = [
    ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M"]
]

row_index = 3
for row in keyboard_layout:
    col_index = 0
    for key in row:
        var = tk.BooleanVar(value=key in skill_keys)
        check = ttk.Checkbutton(frame, text=key, variable=var, style="TCheckbutton")
        check.grid(row=row_index, column=col_index, sticky="nsew", pady=2, padx=2)
        checkboxes[key] = var
        col_index += 1
    row_index += 1

# Configura o layout para centralizar as colunas das teclas
for col in range(len(keyboard_layout[0])):
    frame.columnconfigure(col, weight=1)

# Centraliza os controles adicionais
ttk.Label(frame, text="Teclas para spammar:", font=("Arial", 12), background="", foreground="white").grid(
    row=row_index, column=0, columnspan=2, sticky="w", pady=10
)
skill_keys_entry = ttk.Entry(frame, width=30, font=("Arial", 12))
skill_keys_entry.grid(row=row_index, column=2, columnspan=3, pady=10, sticky="w")

ttk.Label(frame, text="Tecla para ativar/desativar:", font=("Arial", 12), background="", foreground="white").grid(
    row=row_index + 1, column=0, columnspan=2, sticky="w", pady=10
)
toggle_key_entry = ttk.Entry(frame, width=15, font=("Arial", 12))
toggle_key_entry.insert(0, toggle_key)
toggle_key_entry.grid(row=row_index, column=2, columnspan=3, pady=10, sticky="w")
toggle_key_entry.bind("<FocusIn>", on_toggle_key_entry_focus)  # Adiciona o evento para capturar a tecla

# Organiza os botões centralizados sem o estilo de fundo
button_frame = ttk.Frame(frame, padding="10")  # Remove o estilo "TFrame"
button_frame.grid(row=row_index + 1, column=0, columnspan=15, pady=20, sticky="nsew")

update_button = ttk.Button(button_frame, text="Atualizar Teclas", command=update_keys_from_checkboxes, style="Green.TButton")
update_button.grid(row=0, column=0, padx=10)

toggle_button = ttk.Button(button_frame, text="Ligar Spammer", command=toggle_spammer, style="Green.TButton")
toggle_button.grid(row=0, column=1, padx=10)

stop_button = ttk.Button(button_frame, text="Parar Spammer", command=stop_spammer, style="Red.TButton")
stop_button.grid(row=0, column=2, padx=10)

# Configura o layout para centralizar os elementos principais
frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)

# Add a language selection dropdown in the top-right corner
language_var = tk.StringVar(value="Português (Brasil)")
language_dropdown = ttk.OptionMenu(
    root, language_var, "Português (Brasil)", "English", "Português (Brasil)", command=change_language
)
language_dropdown.place(x=750, y=10)  # Position in the top-right corner

# Add the app version in the bottom-right corner
app_version_label = ttk.Label(root, text="Version 1.0.0", font=("Arial", 10), background="#2C3E50", foreground="white")
app_version_label.place(relx=1.0, rely=1.0, anchor="se")  # Corrected placement

# Load images for Discord and GitHub buttons
discord_icon = Image.open("assets/discord_icon.png").resize((30, 30), Image.Resampling.LANCZOS)
discord_photo = ImageTk.PhotoImage(discord_icon)

github_icon = Image.open("assets/github_icon.png").resize((30, 30), Image.Resampling.LANCZOS)
github_photo = ImageTk.PhotoImage(github_icon)

# Functions to open URLs
def open_discord():
    import webbrowser
    webbrowser.open("https://discord.gg/bmZP4Dvt")

def open_github():
    import webbrowser
    webbrowser.open("https://github.com/rodrygomarquex/RoadSpammer")

# Add buttons for Discord and GitHub at the bottom center
social_button_frame = ttk.Frame(frame, padding="10", style="TFrame")
social_button_frame.grid(row=row_index + 2, column=0, columnspan=15, pady=20, sticky="nsew")

# Style for rounded buttons
style.configure("Rounded.TButton", padding=10, relief="flat", background="#1ABC9C", foreground="white", font=("Arial", 10, "bold"))
style.map("Rounded.TButton", background=[("active", "#16A085")])

discord_button = ttk.Button(
    social_button_frame, image=discord_photo, command=open_discord, style="Rounded.TButton"
)
discord_button.grid(row=0, column=0, padx=20)  # Reduced padding for closer spacing

github_button = ttk.Button(
    social_button_frame, image=github_photo, command=open_github, style="Rounded.TButton"
)
github_button.grid(row=0, column=1, padx=5)  # Reduced padding for closer spacing

# Configure layout for social buttons
social_button_frame.columnconfigure(0, weight=1)
social_button_frame.columnconfigure(1, weight=1)

# Inicia o monitoramento da tecla de ativação/desativação
monitor_toggle_key()

root.mainloop()
