from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Lista de teclas de skill a serem spammadas
skill_keys = os.getenv("SKILL_KEYS", "").split(',')

# Verifica se as teclas de skill foram configuradas
if not skill_keys or skill_keys == [""]:
    skill_keys = ["F1", "F2", "F3"]  # Valores padrão

# Remove espaços em branco das teclas
skill_keys = [key.strip() for key in skill_keys if key.strip()]

# Tecla para ativar/desativar o spammer
toggle_key = os.getenv("TOGGLE_KEY", "end").strip()

# Intervalo entre os comandos (em segundos)
try:
    delay = float(os.getenv("DELAY", 0.1))
    if delay <= 0:
        raise ValueError
except ValueError:
    delay = 0.1
