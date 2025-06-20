import os
import tkinter as tk
from tkinter import messagebox
import subprocess
from dotenv import load_dotenv

ENV_PATH = ".env"

# Carregar variáveis de ambiente
load_dotenv()

# Função para salvar uma variável no .env
def set_env_variable(key, value):
    lines = []
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

    # Atualizar ou adicionar a variável
    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break

    if not found:
        lines.append(f"{key}={value}\n")

    # Reescrever o .env com a variável atualizada
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Atualiza a variável no ambiente atual
    os.environ[key] = value

def download_playlist():
    url = entry_url.get().strip()
    path = entry_path.get().strip()

    if not url:
        messagebox.showerror("Erro", "Por favor, insira o link da playlist.")
        return
    if not path:
        messagebox.showerror("Erro", "Por favor, insira o caminho da pasta de destino.")
        return

    # Salva o novo caminho no .env
    set_env_variable("DOWNLOAD_PATH", path)
    os.makedirs(path, exist_ok=True)

    try:
        command = [
            "yt-dlp.exe",
            "-x",
            "--audio-format", "mp3",
            "-o", os.path.join(path, "%(title)s.%(ext)s"),
            url
        ]

        subprocess.run(command, check=True)
        messagebox.showinfo("Concluído", "Download da playlist concluído!")

    except subprocess.CalledProcessError as e:
        # Salvar o erro no arquivo
        error_file = os.path.join(path, "erros.txt")
        with open(error_file, "a", encoding="utf-8") as f:
            f.write(url + "\n")
        messagebox.showerror("Erro", f"Erro ao baixar a playlist:\n{e}")

# GUI
root = tk.Tk()
root.title("Download de Playlist do YouTube")
root.geometry("600x200")

label_url = tk.Label(root, text="Link da playlist do YouTube:")
label_url.pack(pady=(10, 0))

entry_url = tk.Entry(root, width=80)
entry_url.pack()

label_path = tk.Label(root, text="Caminho da pasta de destino:")
label_path.pack(pady=(10, 0))

# Preenche com valor atual do .env, se existir
default_path = os.getenv("DOWNLOAD_PATH", "")
entry_path = tk.Entry(root, width=80)
entry_path.insert(0, default_path)
entry_path.pack()

download_button = tk.Button(root, text="Baixar Playlist", command=download_playlist)
download_button.pack(pady=15)

root.mainloop()
