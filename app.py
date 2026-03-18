import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="Transcritor Turbo", page_icon="🚀")

st.title("🚀 Transcritor Turbo v3")
st.write("Se o vídeo tiver qualquer tipo de legenda, eu vou encontrar!")

url = st.text_input("Cole o link do Vídeo ou Short:")

if url:
    try:
        # Extração inteligente do ID
        if "shorts/" in url:
            video_id = url.split("shorts/")[1].split("?")[0].split("&")[0]
        elif "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        else:
            video_id = url.split("/")[-1].split("?")[0]

        with st.spinner(f'Buscando em todos os bancos de dados do YouTube...'):
            # LISTA DE TENTATIVAS:
            # 1. Tenta Português (Manual ou Automático)
            # 2. Tenta Inglês (Manual ou Automático)
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            try:
                # Tenta capturar em Português primeiro
                transcript = transcript_list.find_transcript(['pt'])
            except:
                # Se não achar PT, tenta Inglês ou a primeira disponível
                transcript = transcript_list.find_generated_transcript(['pt', 'en'])

            data = transcript.fetch()
            texto_completo = " ".join([item['text'] for item in data])
            
            st.success(f"Encontrado! Idioma: {transcript.language}")
            st.text_area("Texto extraído:", texto_completo, height=400)
            st.download_button("Baixar TXT", texto_completo, file_name=f"transcricao_{video_id}.txt")

    except Exception as e:
        st.error("Infelizmente esse vídeo não tem NENHUMA legenda disponível no YouTube (nem automática).")
        st.info("Dica: Verifique se o vídeo abre no YouTube e se o botão 'CC' está disponível.")

st.markdown("---")
st.caption("Dica: Se o vídeo for muito novo, o YouTube pode levar uns minutos para gerar a legenda.")
