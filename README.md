# Global Solution AI

Microsserviço de IA Generativa (Google Gemini) criado como parte da Global Solution da FIAP.

A função desta API é atuar como um "especialista" em Processamento de Linguagem Natural (PLN). Ela recebe um bloco de texto (como um currículo ou uma descrição de vaga) e, usando IA Generativa, extrai uma lista estruturada de skills técnicas e pessoais.

## Arquitetura

Esta API é responsável por enviar os dados estruturados para o BackEnd Java.

O fluxo da solução é:

`[Frontend (Web/Mobile)]` → `[Backend Principal (Java)]` → `[API (Python/FastAPI)]`

1. O **Backend Java** (a aplicação principal) recebe uma requisição do frontend.

2. Java faz uma chamada HTTP POST para esta API Python.

3. API Python processa o texto usando o Google Gemini, extrai as skills e retorna um JSON limpo para o Java.

4. O Java, então, continua sua lógica de negócio.

## Tecnologias Utilizadas

* **Python 3.12**
* **FastAPI:** Para a criação do servidor web e do endpoint REST.
* **Google Generative AI (Gemini):** Modelo `gemini-2.5-flash` para a extração de skills.
* **Pydantic:** Para validação dos dados de entrada e saída.
* **Uvicorn:** Como servidor para rodar o FastAPI.

## Configuração do Ambiente Local

### 1. Pré-requisitos

* [Python 3.12](https://www.python.org/downloads/)
* `pip` (gerenciador de pacotes)

### 2. Instalação

1. Clone este repositório:

```bash
git clone https://github.com/hachahine/gs_ia.git
cd gs_ia
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
# No Windows:
.venv\Scripts\activate

# No Linux/Mac
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução Local

Para rodar o servidor FastAPI localmente:

```bash
uvicorn main:app --reload --port 8000
```

A API estará disponível em `http://127.0.0.1:8000`.

* Acesse `http://127.0.0.1:8000/` para ver o *health check* (`{"msg": "service is running"}`).  
* Acesse `http://127.0.0.1:8000/docs` para ver a documentação interativa (Swagger UI) do FastAPI.

### Extrair skills

* **Endpoint:** `POST /api/v1/skills`
* **Descrição:** Recebe um texto e a api-key do Gemini, retorna a lista de habilidades extraídas.

#### Request Body 

```json
{
  "text": "Sou um desenvolvedor júnior com experiência em Python, Git e FastAPI. Tenho boa comunicação e aprendo rápido.",
  "api_key": "api-key"
}
```

#### Exemplo de sucesso

json retornado:

```json
{
  "habilidades": [
    "Python",
    "Git",
    "FastAPI",
    "comunicação"
  ]
}
```

#### Error Responses

* `400 Bad Request`: Retornado se os campos `text` ou `api_key` estiverem vazios.

```json
{
  "detail": "O campo 'text' é obrigatório e não pode estar vazio."
}
```

* `401 Unauthorized`: Retornado se a `api_key` do Google for inválida ou expirar.

```json
{
  "detail": "A GOOGLE_API_KEY fornecida é inválida ou não autorizada."
}
```

* `500 Internal Server Error`: Retornado se a API do Google estiver fora do ar ou outro erro inesperado ocorrer.

```json
{
  "detail": "Erro interno do servidor: <descrição do erro>"
}
```

## Deploy

O deploy desta API foi realizado no **Azure Web App* utilizando um contêiner Docker.

* **Plano de Serviço:** `gs-python-plan-free`
* **Grupo de Recursos:** `rg-gs`
* **Imagem Docker:** `hachahine/gs_ai_api:latest`
* **Endpoint (Prod):** `https://pythonaigs.azurewebsites.net`

