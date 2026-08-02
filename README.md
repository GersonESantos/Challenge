# Challenge

# Alura Agent — Desafio Final

Agente de IA para responder perguntas sobre documentos internos de uma empresa.

Agora o projeto roda como uma aplicação web Flask, pronta para publicação em uma instância Oracle Compute.

## Estrutura do projeto

```
Challenge/
├── pdf/
│   └── documento.pdf        <- coloque aqui o PDF escolhido
├── templates/
│   └── index.html           <- interface web
├── src/
│   ├── document_loader.py   <- lê e processa o PDF (etapa 1 do desafio)
│   └── main.py              <- servidor Flask
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

   Abra `http://127.0.0.1:5000` no navegador. Você pode enviar um PDF, escolher um arquivo da pasta `pdf/` ou buscar por um trecho do conteúdo.

## Deploy na Oracle Cloud

1. Crie uma Compute Instance na região `sa-saopaulo-1`.
2. Libere as portas `22` (SSH), `80` (HTTP) e, se quiser testar direto, `5000`.
3. Copie o projeto para a máquina virtual.
4. Instale Python 3, crie um ambiente virtual e instale as dependências:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
5. Inicie o app com Gunicorn a partir da pasta `src`:
   ```
   cd src
   gunicorn -w 2 -b 127.0.0.1:8000 main:app
   ```
6. Configure o Nginx como proxy reverso para `127.0.0.1:8000` e use o Nginx para servir a interface web na porta 80.

Os arquivos prontos ficam em:
- [deploy/alura-agent.service](deploy/alura-agent.service)
- [deploy/nginx.conf](deploy/nginx.conf)

Fluxo típico na VM:
1. Copie o projeto para `/opt/alura-agent/Challenge`.
2. Crie o venv em `/opt/alura-agent/Challenge/.venv`.
3. Copie [deploy/alura-agent.service](deploy/alura-agent.service) para `/etc/systemd/system/alura-agent.service`.
4. Copie [deploy/nginx.conf](deploy/nginx.conf) para a configuração do site no Nginx.
5. Se existir um site padrão do Nginx na porta 80, desative-o para evitar conflito:
   ```
   sudo rm -f /etc/nginx/conf.d/default.conf
   ```
6. Rode `sudo systemctl daemon-reload && sudo systemctl enable --now alura-agent`.

Exemplo de bloco `server` do Nginx:
```nginx
server {
    listen 80;
   server_name 147.15.28.10;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Próximas etapas do desafio

- Gerar embeddings dos chunks
- Indexar os chunks para busca (ex: FAISS, Chroma)
- Criar a interface de perguntas e respostas usando um modelo de IA