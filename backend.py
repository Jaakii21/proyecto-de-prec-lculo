import os
import re
from google import genai
from google.genai import types

def validar_y_limpiar(expr_str):
    """Valida caracteres prohibidos y normaliza la sintaxis algebraica."""
    if any(c in expr_str for c in ["$", "\\", "#", "_", "{", "}", "[", "]"]):
        raise ValueError("Se detectaron caracteres inválidos o de formato.")
    
    if "=" in expr_str and not ("," in expr_str):
        partes = expr_str.split("=")
        expr_str = partes[0]
        
    expr_str = expr_str.replace("^", "**")
    expr_str = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr_str)
    return expr_str

def resolver_ia(pregunta_ia):
    """Conecta con Gemini usando el SDK moderno."""
    # Carga segura del .env
    try:
        from dotenv import load_dotenv
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(dotenv_path)
    except Exception:
        pass

    api_key = None
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return "⚠️ No se encontró la `GEMINI_API_KEY`. Configúrala en tu archivo `.env` o en los Secrets de Streamlit."

    system_prompt = (
        "Eres una tutora experta y pedagógica en Precálculo y Cálculo para la Universidad Mariano Gálvez de Guatemala. "
        "Tu ÚNICA función es responder dudas teóricas, conceptuales, explicaciones de teoremas y métodos matemáticos de Precálculo y Cálculo "
        "(álgebra, funciones, límites, derivadas, integrales y sus aplicaciones). "
        "RESTRICCIÓN ESTRICTA: Si el usuario te hace preguntas fuera de este tema (como historia, deportes, programación general, recetas, noticias o conversación casual), "
        "debes declinar la respuesta educadamente diciendo: 'Lo siento, como tutora especializada de la Universidad Mariano Gálvez, únicamente puedo responder dudas relacionadas con Precálculo y Cálculo.' "
        "Responde siempre en español claro, usando notación matemática limpia."
    )

    try:
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=pregunta_ia,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.3
            )
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error al conectar con la tutora IA: {e}"