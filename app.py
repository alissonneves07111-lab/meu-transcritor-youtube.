import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="Transcritor Turbo", page_icon="📝")

st.title("🚀 Transcritor de Vídeos e Shorts")
st.write("Funciona com links normais e links de Shorts!")

url = st.text_input("Cole o link aqui (Vídeo ou Short):")

if url:
    try:
        # --- MÁGICA PARA SHORTS ---
        # Se o link for de short, a gente transforma no ID do vídeo
        if "shorts/" in url:
            video_id = url.split("shorts/")[1].split("?")[0]
        elif "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        else:
            # Pega o final do link caso seja o formato youtu.be/ID
            video_id = url.split("/")[-1].split("?")[0]

        with st.spinner(f'Processando ID: {video_id}...'):
            # Busca a transcrição (tenta PT, se não tiver tenta EN)
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
            
            # Junta as frases e remove quebras de linha desnecessárias
            texto_completo = " ".join([item['text'] for item in transcript])
            
            st.success("Transcrição capturada com sucesso!")
            
            # Mostra o texto em uma caixa grande
            st.text_area("Texto extraído:", texto_completo, height=400)
            
            # Botão para o usuário baixar o arquivo
            st.download_button("Baixar em .txt", texto_completo, file_name=f"transcricao_{video_id}.txt")

    except Exception as e:
        st.error("Erro: O YouTube não liberou a transcrição para este link. Verifique se o vídeo/short realmente tem legendas disponíveis.")
