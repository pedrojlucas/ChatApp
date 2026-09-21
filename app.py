import os
import streamlit as st
from ollama import Client

st.set_page_config(page_title="Private chat with Ollama Cloud", page_icon="☁️")

st.title("☁️ Chat with Ollama Cloud")
st.write("Your chats are not stored beyond this screen and the model used is open source."

# Configuración de la API Key de Ollama de forma segura
api_key = os.getenv("OLLAMA_API_KEY")

if not api_key:
    with st.sidebar:
        st.subheader("Configuración")
        api_key = st.text_input("Introduce tu Ollama API Key:", type="password")
        st.markdown("[Obtener clave en Ollama Cloud](https://ollama.com)")

if not api_key:
    st.warning("Por favor, introduce tu API Key de Ollama en la barra lateral para continuar.")
    st.stop()

# Inicializar el cliente apuntando a la nube de Ollama con la clave de autorización
client = Client(
    host='https://ollama.com',
    headers={'Authorization': f'Bearer {api_key}'}
)

# Gestión del historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿Qué quieres consultar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Llamada al modelo en la nube de Ollama (ej. un modelo disponible en su catálogo cloud)
            response_stream = client.chat(
                model='gemma4:31b', # O el modelo cloud que prefieras utilizar
                messages=st.session_state.messages,
                stream=True
            )
            
            # Recoger y mostrar la respuesta en streaming
            def generate():
                for chunk in response_stream:
                    if chunk['message']['content']:
                        yield chunk['message']['content']

            response = st.write_stream(generate())
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error connecting to the cloud: {e}")