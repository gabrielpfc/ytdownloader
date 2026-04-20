import os
import re
from yt_dlp import YoutubeDL

# --- CONFIGURAÇÕES ---
YOUTUBE_URL = 'https://www.youtube.com/watch?v=aTUcg2q-dDA&list=PLppJTs1HbHYzuLE6n7iHoygFDfnTzPo66'

def normalizar_nome(texto):
    """Limpa caracteres especiais para garantir que a comparação entre o nome do vídeo e o arquivo funcione."""
    # Remove barras, aspas, interrogações e transforma tudo em minúsculo
    return re.sub(r'[\\/*?:"<>|？]', '', texto).strip().casefold()

def olhar_pasta_antes_de_baixar(info, *, incomplete):
    """Função que LITERALMENTE olha os arquivos na pasta antes de deixar o yt-dlp baixar."""
    titulo_video = info.get('title', '')
    nome_pasta = info.get('playlist_title') or 'IGNITE'
    
    # Se a pasta ainda não existe, pode baixar livremente
    if not os.path.exists(nome_pasta):
        return None
        
    titulo_limpo = normalizar_nome(titulo_video)
    
    # Vasculha todos os arquivos físicos que já estão na pasta
    for arquivo in os.listdir(nome_pasta):
        # Pega o nome do arquivo sem a extensão (.mp3, .mp4, etc)
        arquivo_sem_extensao = os.path.splitext(arquivo)[0]
        arquivo_limpo = normalizar_nome(arquivo_sem_extensao)
        
        # Se o nome do vídeo do YouTube já existir na pasta, aborta o download!
        if titulo_limpo == arquivo_limpo or titulo_limpo in arquivo_limpo:
            print(f"  -> Pulando: '{titulo_video}' já está na pasta fisicamente.")
            return "Já existe na pasta." # Retornar um texto aqui faz o yt-dlp pular o vídeo
            
    return None # Se não achou na pasta, permite o download

def run_youtube():
    print("\n--- Verificando a pasta fisicamente para pular o que já tem ---")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(playlist_title)s/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'nocheckcertificate': True, 
        'ignoreerrors': True, 
        'yesplaylist': True,
        
        # Chama a nossa função que olha a pasta antes de cada vídeo
        'match_filter': olhar_pasta_antes_de_baixar,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([YOUTUBE_URL])

def main():
    print("================================================")
    print("   ATUALIZADOR DE PLAYLIST (SÓ O QUE FALTA)     ")
    print("================================================")
    run_youtube()

if __name__ == "__main__":
    main()