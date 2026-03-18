import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
import whisper
import os

st.set_page_config(page_title="Transcritor Turbo V4", page_icon="🎙️")

st.title("🎙️ Transcritor Turbo Ultra")
st.write("Tenta pegar a legenda original. Se não houver, ele 'ouve' o áudio e escreve!")

url = st.text_input("Cole o link aqui:")

if url:
    video_id = ""
    if "shorts/" in url: video_id = url.split("shorts/")[1].split("?")[0].split("&")[0]
    elif "v=" in url: video_id = url.split("v=")[1].split("&")[0]
    else: video_id = url.split("/")[-1].split("?")[0]

    try:
        with st.spinner('Tentando capturar legendas prontas...'):
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript(['pt', 'en'])
            data = transcript.fetch()
            texto_final = " ".join([item['text'] for item in data])
            st.success("Legenda oficial encontrada!")
            st.text_area("Resultado:", texto_final, height=300)

    except:
        st.warning("Legendas não encontradas. Iniciando modo 'Ouvir Áudio' (IA Whisper)...")
        
        try:
            with st.spinner('Baixando áudio e processando com IA... Isso pode levar 1-2 minutos.'):
                # Baixa o áudio do vídeo
                ydl_opts = {'format': 'm4a/bestaudio/best', 'outtmpl': 'audio.m4a'}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Carrega o modelo de IA que ouve o áudio
                model = whisper.load_model("tiny") # Modelo leve para o Streamlit aguentar
                result = model.transcribe("audio.m4a")
                texto_final = result["text"]
                
                st.success("Transcrição por IA concluída!")
                st.text_area("Resultado (IA):", texto_final, height=300)
                
                # Limpa o arquivo de áudio depois de usar
                os.remove("audio.m4a")
        except Exception as e:
            st.error(f"Erro crítico: O vídeo é muito longo ou o YouTube bloqueou o download. Erro: {e}")

st.markdown("---")
st.caption("Nota: O processamento por áudio é mais lento, mas funciona em quase qualquer vídeo.")
