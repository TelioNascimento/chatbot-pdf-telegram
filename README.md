# 🤖 Chatbot PDF com Telegram & Interface Web

Assistente virtual automático capaz de responder a dúvidas de usuários com base em um arquivo PDF hospedado publicamente no GitHub. A aplicação oferece atendimento simultâneo via **Telegram** e por uma **Interface Web interativa**, utilizando a API do **Google Gemini** para geração de respostas baseadas em contexto (RAG) e **FastAPI** para o backend.

---

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn
* **Integração Telegram:** [python-telegram-bot](https://python-telegram-bot.org/) (execução assíncrona via Polling)
* **Inteligência Artificial:** [Google Gemini API](https://aistudio.google.com/) (`gemini-2.5-flash` via SDK `google-genai`)
* **Processamento de PDF:** [PyPDF](https://pypdf.readthedocs.io/) & [HTTPX](https://www.python-httpx.org/)
* **Deploy / Hospedagem:** [Render](https://render.com/) (Web Service Gratuito)

---

## 📋 Pré-requisitos e Credenciais

Antes de iniciar, obtenha as seguintes chaves de acesso:

1. **Token do Telegram:** Crie um bot através do [@BotFather](https://t.me/BotFather) no Telegram e guarde o token de API (`TELEGRAM_BOT_TOKEN`).
2. **Chave Google Gemini:** Obtenha uma chave gratuita no [Google AI Studio](https://aistudio.google.com/) (`GEMINI_API_KEY`).
3. **Link RAW do PDF:** Hospede seu arquivo `.pdf` em um repositório público do GitHub e copie o link direto para o arquivo bruto (`https://raw.githubusercontent.com/...`).

---

## 📁 Estrutura de Arquivos

```text
├── main.py              # Aplicação FastAPI, bot Telegram e lógica RAG
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação e instruções de deploy
```

---

## 🛠️ Instalação e Execução Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # Linux/Mac:
   source venv/bin/activate
   # Windows (PowerShell):
   venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Defina as variáveis de ambiente:**
   * **Linux/Mac:**
     ```bash
     export TELEGRAM_BOT_TOKEN="seu_token_aqui"
     export GEMINI_API_KEY="sua_chave_gemini_aqui"
     export PDF_URL="https://raw.githubusercontent.com/usuario/repo/main/documento.pdf"
     ```
   * **Windows (PowerShell):**
     ```powershell
     $env:TELEGRAM_BOT_TOKEN="seu_token_aqui"
     $env:GEMINI_API_KEY="sua_chave_gemini_aqui"
     $env:PDF_URL="https://raw.githubusercontent.com/usuario/repo/main/documento.pdf"
     ```

5. **Inicie o servidor local:**
   ```bash
   uvicorn main:app --reload
   ```
   Acesse a interface web em: `http://127.0.0.1:8000`

---

## ☁️ Deploy no Render (Gratuito)

1. Crie uma conta no [Render](https://render.com/).
2. Clique em **New +** e selecione **Web Service**.
3. Conecte sua conta do GitHub e selecione este repositório.
4. Configure os parâmetros da aplicação:
   * **Name:** `chatbot-pdf-telegram`
   * **Environment:** `Python 3`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   * **Plan Type:** `Free`
5. Na seção **Environment Variables**, adicione as seguintes chaves:
   * `TELEGRAM_BOT_TOKEN`
   * `GEMINI_API_KEY`
   * `PDF_URL`
6. Clique em **Deploy Web Service**.

---

## ⚙️ Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
| :--- | :--- | :---: |
| `TELEGRAM_BOT_TOKEN` | Token de autenticação gerado pelo @BotFather | Sim |
| `GEMINI_API_KEY` | Chave de API gerada no Google AI Studio | Sim |
| `PDF_URL` | URL pública direta (Raw) do PDF no GitHub | Sim |

---

## 📌 Observações Importantes

* **Modo de Espera (Cold Start):** No plano gratuito do Render, a aplicação entra em suspensão após 15 minutos sem tráfego. O primeiro acesso após esse período pode levar cerca de 50 segundos para responder enquanto a instância inicializa.
* **Leitura do PDF:** O arquivo PDF precisa conter texto digital selecionável. PDFs escaneados apenas como imagem requerem OCR prévio para correta extração de conteúdo.

---

## 📌 Exemplos de perguntas

* **Qual nome da equipe?
* **Onde nasceu o taekwondo?

---

## 📌 Exemplos de respostas

* **Com base no documento, o nome da equipe/academia é **Soares Team** (ou **Soares Team – Taekwondo & Hapkido**).
* **Com base no documento fornecido, o Taekwondo surgiu (nasceu) na **antiga Coréia, na cidade/província de Surabul, no Reino de Silla** (localizado na região sul da península coreana).

---

## ☁️ Link Publico da Aplicação
https://chatbot-pdf-telegram.onrender.com/

---

## ☁️ Evidencia do funcionamento da aplicação encontra-se no arquivo evidencia.png
