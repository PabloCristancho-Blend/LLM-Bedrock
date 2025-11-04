# AWS Cloud Expert Chat

Una aplicación de chat interactiva construida con **Streamlit** que permite conversar con un asistente experto en **AWS Cloud Practitioner** usando **AWS Bedrock**.

---

## Descripción

Esta app permite a los usuarios hacer preguntas sobre AWS Cloud y recibir respuestas precisas de un modelo de lenguaje entrenado para actuar como un experto certificado en **AWS Cloud Practitioner**. El asistente se enfoca en buenas prácticas de la nube, servicios como EC2, S3, IAM, RDS, CloudFormation, y proporciona ejemplos detallados cuando se solicita.

---

## Características

- Chat en tiempo real con historial de conversación.
- Asistente especializado en AWS.
- Integración con **AWS Bedrock** para generación de respuestas.
- Manejo de errores al invocar el modelo.
- Interfaz amigable construida con **Streamlit**.

---

## Requisitos

- Python 3.9+
- AWS Account con acceso a Bedrock
- Docker (opcional para ejecutar en contenedor)
- Archivo `.env` con las siguientes variables:
  ```env
  AWS_ACCESS_KEY_ID=tu_access_key
  AWS_SECRET_ACCESS_KEY=tu_secret_key
  AWS_REGION=tu_region_aws  # Opcional, por defecto "us-east-1"
  MODEL_ID=tu_modelo_id
