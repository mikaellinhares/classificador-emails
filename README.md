# AutoU – Classificação e Resposta Automática de E-mails com IA

Este projeto é uma aplicação web que utiliza inteligência artificial para classificar e sugerir respostas automáticas para e-mails recebidos por uma empresa. O sistema aceita textos ou arquivos (.pdf ou .txt) e retorna a classificação do e-mail (produtivo ou improdutivo), uma sugestão de resposta e uma prévia do texto extraído.

## Funcionalidades

- Upload de texto ou arquivo (.pdf/.txt) de e-mail
- Classificação automática do e-mail (produtivo/improdutivo)
- Sugestão de resposta polida e adequada
- Prévia do texto extraído do e-mail

## Tecnologias Utilizadas

- Python 3.11+
- Flask
- SpaCy (para processamento de texto)
- PyPDF2 (leitura de PDFs)
- DeepSeek API (IA para classificação e sugestão de resposta)
- TailwindCSS (interface web)

## Configuração

1. **Clone o repositório:**
   ```sh
   git clone git@github.com:mikaellinhares/classificador-emails.git
   cd AutoU
   ```

2. **Crie e ative um ambiente virtual:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Baixe o modelo SpaCy para português:**
   ```sh
   python -m spacy download pt_core_news_sm
   ```

5. **Configure o arquivo `.env`:**
   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
   ```
   FLASK_SECRET_KEY=sua-chave-secreta
   AI_PROVIDER=deepseek
   DEEPSEEK_API_KEY=sua-chave-de-api
   DEEPSEEK_MODEL=deepseek-chat
   FLASK_DEBUG=1
   PORT=5000
   ```
   Substitua `sua-chave-secreta` e `sua-chave-de-api` pelos valores adequados.

## Como Rodar

1. **Inicie o servidor Flask:**
   ```sh
   python app.py
   ```

2. **Acesse a aplicação:**  
   Abra o navegador e acesse [http://localhost:5000](http://localhost:5000)

## Estrutura de Pastas

- `app.py` – Arquivo principal da aplicação Flask
- `ai_providers/` – Implementações dos provedores de IA
- `utils/` – Utilitários para leitura e processamento de arquivos/textos
- `templates/` – Templates HTML para interface web
- `uploads/` – Pasta temporária

## Observações

É necessário possuir uma chave de API válida do DeepSeek para funcionamento da IA.
O projeto pode ser adaptado para outros provedores de IA implementando novas classes em ai_providers/.
