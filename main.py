import boto3, json
from botocore.exceptions import ClientError



import streamlit as st
import os
from dotenv import load_dotenv


def test_AWS_bedrock():
    # Carga las credenciales AWS (.env):
    load_dotenv()

    # Use the Conversation API to send a text message to Anthropic Claude.

    # Create a Bedrock Runtime client in the AWS Region you want to use.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID, e.g., Claude 3 Haiku.
    model_id = "meta.llama3-70b-instruct-v1:0"

    # Start a conversation with the user message.
    user_message = "Who are Linkin Park?."
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        print(response_text)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)


def test_streamlit():

    # Prueba sencilla de StreamLit.
    st.title("Demo IA")
    nombre = st.text_input("Tu nombre:")
    if st.button("Saludar"):
        st.write(f"Hola, {nombre} 👋")
    

def run():
    # Probar conexión con AWS Bedrock:
    test_AWS_bedrock()

    # Probar StremLit.
    # test_streamlit()

if __name__ == "__main__":
    run()