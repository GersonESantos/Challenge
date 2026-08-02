# Roteiro do deploy do Challenge na OCI

## 1. Cenário inicial
Eu tinha uma instância OCI que já estava servindo um `index.html` estático no navegador.

Esse `index.html` era apenas uma página fixa, sem backend, sem processamento de arquivos e sem lógica de aplicação web.

## 2. Objetivo
Queria substituir esse `index.html` por um aplicativo web chamado **Challenge**, para que a OCI passasse a servir a aplicação real em vez da página estática.

## 3. O que foi feito
### 3.1 Estrutura do projeto
Foi preparado um projeto Python com:
- leitura de PDFs
- processamento em chunks
- interface web com Flask
- arquivos de deploy para Linux/OCI

### 3.2 Aplicação web
O app foi transformado em uma aplicação Flask com:
- rota principal para abrir a interface no navegador
- rota para processar PDFs
- template HTML para a interface web

### 3.3 Deploy na OCI
Na máquina virtual da OCI:
- o projeto foi copiado para a instância
- o ambiente virtual `.venv` foi criado
- as dependências foram instaladas
- o app foi executado com `gunicorn`
- o Nginx foi configurado como proxy reverso
- o `systemd` foi usado para manter o serviço ativo

## 4. Problemas encontrados e resolvidos
### 4.1 Copia de arquivos
No começo houve erro com `scp` porque ele foi executado dentro da VM em vez de no Windows local.

### 4.2 Caminhos incorretos
Os caminhos do `systemd` estavam errados porque o projeto ficou em:
- `/opt/alura-agent/Challenge`

e não em:
- `/opt/alura-agent`

### 4.3 Conflito na porta 80
A porta 80 já estava ocupada por `httpd`, então o Nginx não conseguia subir.

Foi necessário parar/desabilitar o `httpd` para liberar a porta.

### 4.4 Erro 502
Depois disso ainda apareceu `502 Bad Gateway`, porque o Nginx não estava conseguindo conversar com o backend.

Isso foi resolvido ajustando:
- o service do `systemd`
- o `nginx.conf`
- o restart do `alura-agent` e do `nginx`

### 4.5 Conflito de `server_name`
Apareceu aviso de conflito com `server_name _`, mas isso não impedia o funcionamento da aplicação.

## 5. Resultado final
No final:
- a aplicação web Challenge ficou no ar
- o Nginx passou a servir a aplicação
- o backend Python respondeu corretamente
- a URL pública da OCI passou a mostrar o app web, substituindo o `index.html`

## 6. Passos resumidos para repetir
1. Preparar o app Python/Flask.
2. Copiar o projeto para a OCI.
3. Criar e ativar o ambiente virtual.
4. Instalar dependências.
5. Rodar o app com `gunicorn`.
6. Configurar `systemd` para manter o serviço.
7. Configurar o Nginx como proxy reverso.
8. Garantir que a porta 80 esteja livre.
9. Reiniciar os serviços.
10. Testar o acesso pelo navegador.