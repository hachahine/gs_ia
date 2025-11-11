# GS AI - API Extratora de Skills

Microsserviço de IA Generativa (Google Gemini) criado como parte da Global Solution da FIAP.

A função desta API é atuar como um "especialista" em Processamento de Linguagem Natural (PLN). Ela recebe um bloco de texto (como um currículo ou uma descrição de vaga) e, usando IA Generativa, extrai uma lista estruturada de habilidades (skills) técnicas e interpessoais.

## Arquitetura

Esta API foi desenhada para atuar como um **microsserviço** focado. Ela não possui banco de dados e não armazena estado.

O fluxo de arquitetura da solução completa é:

`[Frontend (Web/Mobile)]` → `[Backend Principal (Java)]` → `[Esta API (Python/FastAPI)]`

1. O **Backend Java** (a aplicação principal) recebe uma requisição do frontend.

2. Quando precisa analisar um texto, o Java faz uma chamada HTTP POST para esta API Python.

3. Esta API (Python) processa o texto usando o Google Gemini, extrai as skills e retorna um JSON limpo para o Java.

4. O Java, então, continua sua lógica de negócio (comparar com o banco, etc.).

## Tecnologias Utilizadas

* **Python 3.12**
* **FastAPI:** Para a criação do servidor web e do endpoint REST.
* **Google Generative AI (Gemini):** Modelo `gemini-1.5-flash` para a extração de habilidades.
* **Pydantic:** Para validação dos dados de entrada e saída.
* **Uvicorn:** Como servidor ASGI para rodar o FastAPI.

## Configuração do Ambiente Local

### 1. Pré-requisitos

* [Python 3.12](https://www.python.org/downloads/)
* `pip` (gerenciador de pacotes)

### 2. Instalação

1. Clone este repositório:

```bash
git clone <url-do-seu-repositorio>
cd gs_ia
```

2. Crie e ative um ambiente virtual (Recomendado):

```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

3. Gere um arquivo `requirements.txt` a partir do `pyproject.toml` (se estiver usando `uv`):

```bash
uv pip freeze > requirements.txt
```

*(Ou gere o `requirements.txt` da forma que preferir)*

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

**Nota:** Este projeto não requer um arquivo `.env`, pois a chave da API do Google Gemini é fornecida dinamicamente pelo backend Java a cada requisição.

## Execução Local

Para rodar o servidor FastAPI localmente:

```bash
uvicorn main:app --reload --port 8000
```

A API estará disponível em `http://127.0.0.1:8000`.

* Acesse `http://127.0.0.1:8000/` para ver o *health check* (`{"msg": "service is running"}`).  
* Acesse `http://127.0.0.1:8000/docs` para ver a documentação interativa (Swagger UI) do FastAPI.

## Uso da API (Contrato da API)

Este é o endpoint principal que o seu backend Java deve consumir.

### Extrair Habilidades

* **Endpoint:** `POST /api/v1/skills`
* **Descrição:** Recebe um texto e a chave da API do Google, e retorna a lista de habilidades extraídas.

#### Request Body (Corpo da Requisição)

```json
{
  "text": "Sou um desenvolvedor júnior com experiência em Python, Git e FastAPI. Tenho boa comunicação e aprendo rápido.",
  "api_key": "SUA_CHAVE_SECRETA_DO_GEMINI_AQUI"
}
```

#### Success Response (Resposta de Sucesso 200)

O `prompt_engineering` no `ai_service.py` força o Gemini a retornar um JSON neste formato:

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

#### Error Responses (Respostas de Erro)

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

O deploy desta API foi realizado no **Azure App Service** utilizando um contêiner Docker.

* **Plano de Serviço:** `gs-python-plan-free` (SKU: F1 Gratuito, Linux)
* **Grupo de Recursos:** `rg-gs`
* **Imagem Docker:** `hachahine/gs_ai_api:latest` (Exemplo)
* **Endpoint (Produção):** `https://pythonaigs.azurewebsites.net`
