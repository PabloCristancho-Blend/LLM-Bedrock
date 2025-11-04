import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import streamlit as st

def get_bedrock_client():
    """Crea el cliente de AWS Bedrock"""
    # Load the environment variables in the actual process (like credentials of AWS etc.) (.env):
    load_dotenv()

    # Bring and Store some necesary variables.
    model_id = os.getenv("MODEL_ID")
    region = os.getenv("AWS_REGION", "us-east-1") # If it doesn't find the environment variable for the region, it takes by default "us-esast-1"

    # Create a Bedrock Runtime client in the selected AWS Region.
    client = boto3.client("bedrock-runtime", region_name=region) # Each region has different models available.
    
    # Return the client, and the model_id.
    return client, model_id

def get_bedrock_response(client, model_id, user_input):
    """
    Envía el historial de conversación al modelo de AWS Bedrock
    y devuelve la respuesta del asistente experto.
    """

    # Prompt base: comportamiento del asistente experto
    expert_prompt = (
        "Eres un experto certificado en AWS Cloud Practitioner. Mencionalo para dar esa atmosfera en la conversación."
        "Responde siempre con claridad, precisión y usando terminología oficial de AWS. "
        "Explica los conceptos de forma profesional pero accesible, y enfócate en las buenas prácticas "
        "de la nube de AWS, incluyendo servicios como EC2, S3, IAM, RDS, CloudFormation y otros. "
        "Si el usuario pide ejemplos o guías, proporciona pasos detallados y recomendaciones actualizadas. "
        "Despídete deseando buena suerte en el aprendizaje y que estas dispuesto para responder más preguntas relacionadas."
    )

    # Building the conversation with the system and user messages.
    conversation = [
        {
            "role": "user",
            "content": [
                {"text": f"{expert_prompt}\n\n{user_input}"}
            ],
        }
    ]

    try:
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={
                "maxTokens": 512,
                "temperature": 0.5,
                "topP": 0.9},
        )

        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text

    except (ClientError, Exception) as e:
        return f"⚠️ Error al invocar el modelo: {e}"
    

import streamlit as st
import time  # solo para simular la espera

def streamlit_chat_app():
    st.set_page_config(page_title="AWS Cloud Expert Chat", page_icon="☁️")
    st.title("☁️ Chat con Experto en AWS (Cloud practitioner)")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container()
    prompt = st.chat_input("Haz una pregunta sobre AWS Cloud...")

    if prompt:
        # Guardar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Mostrar todo el historial hasta ahora
        with chat_container: 
            for msg in st.session_state.messages: 
                with st.chat_message(msg["role"]): 
                    st.markdown(msg["content"])

        # Placeholder para la respuesta del asistente (spinner)
        assistant_placeholder = st.empty()
        with assistant_placeholder.chat_message("assistant"):
            with st.spinner("Pensando..."):
                client, model_id = get_bedrock_client()
                response = get_bedrock_response(client, model_id, prompt)

        # Reemplazar el placeholder con la respuesta final
        assistant_placeholder.empty()  # elimina la burbuja de spinner
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Mostrar solo la respuesta final
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(response)

def run():
    # Run StreamLit.
    streamlit_chat_app()

if __name__ == "__main__":
    run()