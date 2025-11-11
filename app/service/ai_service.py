import google.generativeai as genai
import json
from decouple import config

base_prompt = """
Você é um assistente de RH especialista em recrutamento técnico.
Sua única tarefa é extrair habilidades (skills) técnicas (hard skills) e 
interpessoais (soft skills) do texto fornecido.

Retorne um objeto JSON com uma única chave "habilidades", 
que contém um array de strings com as habilidades encontradas.

Não inclua nenhuma habilidade que não esteja explicitamente no texto.

"""

# pouca criatividade e retorno da resposta em JSON
generation_config = {
    "temperature": 0.2,
    "response_mime_type": "application/json",
}


def extract_skills(text: str, api_key: str) -> dict:
    try:

        # setando a api key
        genai.configure(api_key=api_key)

        # configs do modelo 
        model = genai.GenerativeModel(
            'models/gemini-2.5-flash-lite',
            generation_config=generation_config,
            system_instruction=base_prompt
        )


        response = model.generate_content(text)
        result = json.loads(response.text)

        return result 


    except json.JSONDecodeError:
        return {"habilidades": []}

    except Exception as e:
        print(f"Erro ao extrair skills: {e}")
        return {"habilidades": []}