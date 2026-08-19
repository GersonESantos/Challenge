# Alura Agent - Análise Inteligente de Notas Fiscais com Gemini 3.6 Flash

Interface web desenvolvida em **Flask** para ingestão, fragmentação (chunking), busca textual e **análise analítica contábil/fiscal de documentos PDF (DANFEs/NF-e)** utilizando o modelo de IA **Google Gemini 3.6 Flash**.

O aplicativo está hospedado e em execução em uma instância na **Oracle Cloud Infrastructure (OCI)**:
🌐 **Acesso online:** [http://147.15.87.131](http://147.15.87.131)

---

## 📸 Demonstração

| Interface Principal | Processamento e Visualização |
| :---: | :---: |
| ![Interface Principal](Image/IMGA.png) | ![Chunks Processados](Image/IMGb.png) |

---

## 🚀 Funcionalidades

- **Consultas Analíticas com Gemini AI:** Responda perguntas complexas sobre as notas fiscais (ex: *"qual o total de vendas por mês/ano?"*, *"quais os produtos faturados?"*, *"qual o total de impostos e fretes?"*, *"quem são os maiores clientes?"*) utilizando o modelo `gemini-3.6-flash`.
- **Upload de Documentos:** Envio de novos arquivos `.pdf` diretamente pela interface web para o servidor.
- **Seleção e Escopo Flexível:** Consulta analítica em todas as notas fiscais disponíveis ou em documentos específicos.
- **Busca por Conteúdo:** Filtragem automática de documentos baseada em termos específicos (ex: nome, CPF, etc.).
- **Processamento e Chunking:** Segmentação dos PDFs em chunks estruturados, extraindo metadados como identificador (`id`), página e resumo de texto.
- **Renderização Rica em Markdown:** Apresentação de tabelas comparativas, métricas contábeis e destaque de valores com opção de cópia rápida.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **Google GenAI SDK (`google-genai`)** - Modelo `gemini-3.6-flash`
- **Flask** (Framework Web)
- **pypdf** (Extração e leitura de PDFs)
- **python-dotenv** (Gerenciamento de variáveis de ambiente)
- **Gunicorn** (WSGI HTTP Server)
- **Nginx** (Reverse Proxy na porta 80)
- **Oracle Cloud Infrastructure (OCI)** (Hospedagem da VM)

---

## 📂 Estrutura do Projeto

```text
Challenge/
├── Image/
│   ├── IMGA.png           # Captura da interface principal
│   └── IMGb.png           # Captura dos chunks processados
├── pdf/                   # Diretório de armazenamento dos documentos PDF
├── src/
│   ├── main.py            # Aplicação principal Flask e rotas (/ e /analisar)
│   ├── gemini_analyzer.py # Serviço de integração analítica com Gemini 3.6 Flash
│   └── document_loader.py # Lógica de extração, segmentação e filtros de PDFs
├── templates/
│   └── index.html         # Interface HTML (Jinja2 + marked.js)
├── .env                   # Chave de API do Gemini (GEMINI_API_KEY)
├── requirements.txt       # Dependências do projeto
├── start.sh               # Script de inicialização em produção
└── README.md
```

---

## ⚙️ Instalação e Execução Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/GersonESantos/Challenge.git
   cd Challenge
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # No Linux/macOS:
   source venv/bin/activate
   # No Windows:
   venv\Scripts\activate
   ```

3. **Configure a chave de API do Gemini no `.env`:**
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   GEMINI_API_KEY=sua_chave_aqui
   ```

4. **Instale as dependências:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Execute o servidor de desenvolvimento:**
   ```bash
   python src/main.py
   ```

6. **Acesse no navegador:**
   ```text
   http://127.0.0.1:5000
   ```

---

## ☁️ Deploy em Produção (Oracle Linux / SELinux)

Em ambiente de produção, a aplicação roda gerenciada via **systemd** e **Gunicorn**, com **Nginx** atuando como proxy reverso na porta 80:

```bash
# Execução via Gunicorn
python -m gunicorn --workers 2 --bind 127.0.0.1:5000 --chdir src main:app
```

---

## 👤 Autor

Desenvolvido por **[Gerson Eustaquio dos Santos](https://github.com/GersonESantos)**.