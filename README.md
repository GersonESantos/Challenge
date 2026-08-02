# Challenge

# Alura Agent — Desafio Final

Agente de IA para responder perguntas sobre documentos internos de uma empresa.

## Estrutura do projeto

```
Challenge/
├── pdf/
│   └── documento.pdf        <- coloque aqui o PDF escolhido
├── src/
│   ├── document_loader.py   <- lê e processa o PDF (etapa 1 do desafio)
│   └── main.py               <- ponto de entrada do programa
├── requirements.txt
└── README.md
```

## Como rodar (Windows, PowerShell ou CMD)

1. Abra o terminal na pasta do projeto:
   ```
   cd C:\Repo2026\Challenge
   ```

2. (Recomendado) Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Certifique-se de que o PDF está em `pdf\documento.pdf` (ou ajuste o nome
   do arquivo em `src/main.py`, na variável `PDF_PATH`).

5. Rode o programa:
   ```
   cd src
   python main.py
   ```

   Você deve ver quantos chunks foram gerados e uma prévia do conteúdo
   extraído do PDF.

## Próximas etapas do desafio

- Gerar embeddings dos chunks
- Indexar os chunks para busca (ex: FAISS, Chroma)
- Criar a interface de perguntas e respostas usando um modelo de IA