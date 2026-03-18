import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="Transcritor Turbo", page_icon="📝")

st.title("🚀 Meu Transcritor Automático")
st.write("Cole o link do YouTube e veja a mágica acontecer!")

url = st.text_input("Link do vídeo:")

if url:
    try:
        # Extrai o ID do vídeo
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        else:
            video_id = url.split("/")[-1]

        with st.spinner('Buscando a transcrição...'):
            # Busca o texto (tenta em português, depois em inglês)
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
            
            # Formata o texto
            texto_completo = ""
            for item in transcript:
                texto_completo += f"{item['text']} "
            
            st.success("Pronto!")
            st.text_area("Transcrição:", texto_completo, height=400)
            
            # Botão para baixar o texto
            st.download_button("Baixar Transcrição", texto_completo, file_name="transcricao.txt")

    except Exception as e:
        st.error("Não foi possível encontrar transcrição para este vídeo. Verifique se as legendas estão ativadas no YouTube.")

st.markdown("---")
st.caption("Criado com Streamlit e Python")
