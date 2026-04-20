import os
import random
import re
import asyncio
import edge_tts
from datetime import timedelta
from pydub import AudioSegment
from pydub.utils import which
import fitz  # PyMuPDF
import time
from langdetect import detect, LangDetectException

# ==========================================
# 🔻 CONFIGURAÇÕES GERAIS 🔻
# ==========================================

# Diretórios e Caminhos Fixos
CAMINHO_PDF = r"C:\Users\User\Documents\QA\Taking_Flight_PT_FINAL.pdf"
musicas_dir = r"C:\Users\User\Documents\QA\Runners"
tts_dir = r"C:\Users\User\Documents\QA\TTS"
saida_pasta = r"C:\Users\User\Documents\QA" 

# Configuração da Voz IA e Tempos
VOZ = "pt-BR-FranciscaNeural"
INTERVALO_PADRAO_MS = 30 * 1000   # 30 segundos exatos de música entre cada bloco
INTERVALO_INTRO_MS = 7 * 1000     # 7 segundos após a introdução
REDUCAO_DB = -16                  # redução da música durante TTS (dB)
REDUCAO_GLOBAL = -7               # redução global da música (dB)
FADE_MS = 2200                    # fade in/out em ms

# Inicializa ffmpeg para pydub
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

# ----- FUNÇÕES AUXILIARES -----
def m_to_ms(minutes): 
    return int(minutes * 60 * 1000)

def fmt_ms(ms): 
    return str(timedelta(seconds=int(ms/1000)))

def eh_portugues(texto):
    """ Verifica se o texto é predominantemente português. """
    try:
        if len(texto.strip()) < 20: return True
        return detect(texto) == 'pt'
    except LangDetectException:
        return True

def limpar_erros_pdf(texto):
    """ Filtro implacável para destruir caracteres de má extração antes do TTS. """
    texto = texto.replace("*", "")
    texto = texto.replace("??", "?")  # Transforma interrogações duplas numa só
    texto = re.sub(r'\?([.,!;:”"’\'])', r'\1', texto) # Remove '?' se estiver colado a pontuação real
    texto = re.sub(r'(^|\s)\?([A-ZÀ-Úa-zà-ú])', r'\1\2', texto) # Remove '?' no início de frases/palavras
    return texto.strip()

# ----- GERAÇÃO DE TTS (ASSÍNCRONA) -----
async def gerar_tts_unico(texto, caminho_saida):
    texto_limpo = limpar_erros_pdf(texto)
    communicate = edge_tts.Communicate(texto_limpo, VOZ)
    await communicate.save(caminho_saida)

# ----- CARREGAR MÚSICAS -----
def load_music_mix(folder, duracao_ms):
    arquivos =[os.path.join(folder, f) for f in os.listdir(folder) 
                if f.lower().endswith((".mp3", ".wav", ".webm", ".m4a", ".ogg"))]
    if not arquivos:
        raise FileNotFoundError(f"Nenhuma música encontrada em: {folder}")
    mix = AudioSegment.silent(0)
    while len(mix) < duracao_ms:
        random.shuffle(arquivos)
        for p in arquivos:
            mix += AudioSegment.from_file(p)
            if len(mix) >= duracao_ms: break
    return mix[:duracao_ms]

# ----- EXTRAÇÃO DO PDF -----
def extrair_texto_pdf(caminho_pdf, pag_inicio, pag_fim):
    print(f"\n📄 Extraindo texto do PDF (Páginas {pag_inicio} a {pag_fim})...")
    
    if not os.path.exists(caminho_pdf):
        print(f"❌ ERRO CRÍTICO: Ficheiro '{caminho_pdf}' não encontrado!")
        return None

    doc = fitz.open(caminho_pdf)
    idx_inicio = pag_inicio - 1
    idx_fim = min(pag_fim, len(doc))
    
    chunks_extraidos =[]
    texto_acumulado = ""
    
    for num_pagina in range(idx_inicio, idx_fim):
        pagina = doc[num_pagina]
        altura_pagina = pagina.rect.height
        blocos = pagina.get_text("dict")["blocks"]

        for bloco in blocos:
            if bloco.get("type") == 0:
                bbox = fitz.Rect(bloco["bbox"])
                if bbox.y0 < (altura_pagina * 0.10) or bbox.y1 > (altura_pagina * 0.90):
                    continue

                texto_bloco = ""
                for linha in bloco["lines"]:
                    for span in linha["spans"]:
                        texto_bloco += span["text"] + " "
                
                texto_bloco = texto_bloco.strip()
                
                # Ignora blocos digitais, vazios ou em inglês
                if not texto_bloco or texto_bloco.isdigit() or not eh_portugues(texto_bloco):
                    continue
                
                texto_acumulado += texto_bloco + " "
                
                # Agrupa texto e garante que corta apenas em final de frase
                if len(texto_acumulado) > 1800:
                    texto_test = texto_acumulado.strip()
                    ultimo_caracter = texto_test[-1] if texto_test else ""
                    if ultimo_caracter in['.', '!', '?', '"', '”', ':', ';']:
                        chunks_extraidos.append({
                            "texto": texto_test,
                            "pagina": num_pagina + 1
                        })
                        texto_acumulado = ""

    if texto_acumulado.strip():
        chunks_extraidos.append({
            "texto": texto_acumulado.strip(),
            "pagina": idx_fim
        })

    if not chunks_extraidos:
        print("❌ Nenhum texto extraído. Verifica as páginas.")
        return None
        
    print(f"✅ Foram extraídos {len(chunks_extraidos)} blocos de texto português estruturados.")
    return chunks_extraidos

# ----- PROCESSAMENTO DO EPISÓDIO (MIXAGEM E EXPORTAÇÃO) -----
def construir_episodio(ep_num, ep_chunks):
    pag_inicio_ep = ep_chunks[0]["pagina"]
    pag_fim_ep = ep_chunks[-1]["pagina"]
    
    print(f"\n⚙️ A construir Episódio {ep_num} (Páginas {pag_inicio_ep} a {pag_fim_ep})...")
    
    texto_intro = f"Iniciando o episódio {ep_num} deste livro. Esta parte cobrirá o conteúdo desde a página {pag_inicio_ep} até à página {pag_fim_ep}. Foca-te no teu ritmo e absorve o conteúdo. Boa corrida."
    texto_outro = f"Parte {ep_num} concluída com sucesso. Cobrimos as páginas {pag_inicio_ep} até {pag_fim_ep}. Para o próximo episódio, continuaremos a partir da página {pag_fim_ep}. Mantém o foco e a disciplina."
    
    intro_file = os.path.join(tts_dir, f"intro_ep{ep_num}.mp3")
    outro_file = os.path.join(tts_dir, f"outro_ep{ep_num}.mp3")
    
    asyncio.run(gerar_tts_unico(texto_intro, intro_file))
    asyncio.run(gerar_tts_unico(texto_outro, outro_file))
    
    intro_len = len(AudioSegment.from_file(intro_file))
    outro_len = len(AudioSegment.from_file(outro_file))

    timeline =[]
    timeline.append((0, intro_file, intro_len))
    
    # Cursor ajustado para usar INTERVALO_INTRO_MS após a introdução
    cursor_ms = intro_len + INTERVALO_INTRO_MS
    
    for chunk in ep_chunks:
        timeline.append((cursor_ms, chunk["arquivo"], chunk["duracao_ms"]))
        cursor_ms += chunk["duracao_ms"] + INTERVALO_PADRAO_MS
        
    timeline.append((cursor_ms, outro_file, outro_len))
    duracao_final_ep = cursor_ms + outro_len
    
    print(f"🎵 A misturar música de fundo com o TTS ({fmt_ms(duracao_final_ep)})...")
    corrida = load_music_mix(musicas_dir, duracao_final_ep).apply_gain(REDUCAO_GLOBAL)
    
    for start_ms, fpath, seg_len in timeline:
        end_ms = start_ms + seg_len
        
        if end_ms > len(corrida):
            corrida += AudioSegment.silent(duration=(end_ms - len(corrida)) + 1000)
            
        fundo = corrida[start_ms:end_ms]
        fundo_reduzido = fundo.apply_gain(REDUCAO_DB).fade_in(FADE_MS//2).fade_out(FADE_MS//2)
        combinado = fundo_reduzido.overlay(AudioSegment.from_file(fpath))
        corrida = corrida[:start_ms] + combinado + corrida[end_ms:]

    nome_ficheiro = f"Episodio_{ep_num}_Pag_{pag_inicio_ep}_a_{pag_fim_ep}.mp3"
    caminho_saida_ep = os.path.join(saida_pasta, nome_ficheiro)
    
    print(f"💾 A exportar ficheiro MP3 (Aguarde...).")
    corrida.export(caminho_saida_ep, format="mp3", bitrate="192k")
    print(f"✅ EPISÓDIO {ep_num} GUARDADO: {nome_ficheiro}")
    print("-" * 50)

# ----- LÓGICA PRINCIPAL -----
def main():
    print(f"📚 A usar o PDF: {CAMINHO_PDF}")
    
    try:
        pag_inicio = int(input("Página inicial: ").strip())
        pag_fim = int(input("Página final: ").strip())
        duracao_ep_min = float(input("Duração limite de CADA EPISÓDIO (em minutos): ").strip())
        reuse_tts = input("Reutilizar áudios TTS existentes (y/n)? ").lower().strip() == 'y'
    except ValueError:
        print("Erro: Digite apenas números válidos.")
        return

    duracao_max_ep_ms = m_to_ms(duracao_ep_min)

    chunks = extrair_texto_pdf(CAMINHO_PDF, pag_inicio, pag_fim)
    if not chunks: return

    os.makedirs(tts_dir, exist_ok=True)
    
    print("\n🚀 INÍCIO DA GERAÇÃO ITERATIVA (A gerar episódio a episódio)")
    
    episodio_num = 1
    ep_chunks =[]
    tempo_acumulado_ms = 10000  # Margem inicial para a intro
    
    total_chunks = len(chunks)

    for i, chunk in enumerate(chunks):
        caminho_audio = os.path.join(tts_dir, f"chunk_{i}.mp3")
        
        if not (reuse_tts and os.path.exists(caminho_audio)):
            print(f"🎙️ A processar áudio {i+1}/{total_chunks}...", end="\r")
            try:
                asyncio.run(gerar_tts_unico(chunk["texto"], caminho_audio))
            except Exception as e:
                print(f"\nErro no áudio {i}: {e}")
                continue
        else:
            print(f"♻️ Reutilizando áudio {i+1}/{total_chunks}...", end="\r")
        
        duracao_ms = len(AudioSegment.from_file(caminho_audio))
        chunk["arquivo"] = caminho_audio
        chunk["duracao_ms"] = duracao_ms
        
        espaco_necessario = duracao_ms + INTERVALO_PADRAO_MS
        
        if tempo_acumulado_ms + espaco_necessario > duracao_max_ep_ms - 15000 and len(ep_chunks) > 0:
            print(f"\n\n📦 Limite do Episódio {episodio_num} atingido. A iniciar montagem...")
            construir_episodio(episodio_num, ep_chunks)
            
            episodio_num += 1
            ep_chunks = [chunk]
            tempo_acumulado_ms = 10000 + espaco_necessario
        else:
            ep_chunks.append(chunk)
            tempo_acumulado_ms += espaco_necessario

    if ep_chunks:
        print(f"\n\n📦 A montar os blocos finais no Episódio {episodio_num}...")
        construir_episodio(episodio_num, ep_chunks)

    print("\n🏁 MISSÃO CUMPRIDA! Todos os episódios foram gerados com sucesso.")

if __name__ == "__main__":
    main()