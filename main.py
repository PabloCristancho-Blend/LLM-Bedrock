import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import streamlit as st



def AgentAI_AWS_bedrock():
    '''
    This function establishes a connection with a AWS bedrock service and a certain model.
    
    '''
    # Carga las credenciales AWS (.env):
    load_dotenv()

    # Reading the environment variables.
    # → Set the model ID, e.g., Claude 3.
    model_id = os.getenv("MODEL_ID")

    # Create a Bedrock Runtime client in the selected AWS Region.
    client = boto3.client("bedrock-runtime", region_name="us-east-1") # Each region has different models available.

    # System message: Defines the model's rol as an expert.
    system_prompt = (
        "Eres un experto certificado en AWS Cloud Practitioner. (Mencionalo y Saluda) "
        "Responde siempre con claridad, precisión y usando terminología oficial de AWS. "
        "Explica los conceptos de forma profesional pero accesible, y enfócate en las buenas prácticas "
        "de la nube de AWS, incluyendo servicios como EC2, S3, IAM, RDS, CloudFormation y otros. "
        "Si el usuario pide ejemplos o guías, proporciona pasos detallados y recomendaciones actualizadas."
        "No olvides despedirse y desear buena suerte en el aprendizaje de quien pregunta."
    )

    # User message: <Anything related to AWS Cloud practitioner>.
    user_message = "¿Qué es Amazon EC2 y para qué se utiliza?"


    # Building the conversation with the system and user messages.
    conversation = [
        {
            "role": "assistant",
            "content": [{"text": system_prompt}],
        },
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
            inferenceConfig={
                "maxTokens": 512,
                "temperature": 0.5,
                "topP": 0.9},
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        print("=== Respuesta del experto AWS ===")
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
    # Establish a connection with the AWS Bedrock model:
    AgentAI_AWS_bedrock()

    # Probar StreamLit.
    # test_streamlit()

if __name__ == "__main__":
    run()