# 📄 PDF to Excel (Python + Docker)

Este projeto realiza a extração automática de tabelas a partir de arquivos PDF textuais
e consolida os dados em um arquivo Excel (.xlsx).

A solução utiliza Python, Camelot, Pandas e Docker, garantindo execução reproduzível
e independente do ambiente local.

---

## 🎯 Objetivo

- Extrair tabelas estruturadas de PDFs não escaneados
- Normalizar e consolidar os dados em um único arquivo Excel
- Executar todo o processo via Docker, sem dependências locais

---

## 🧰 Tecnologias utilizadas

- Python 3.11
- Camelot
- pdfplumber
- Pandas
- Docker

---

## ✅ Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Docker (versão 20 ou superior)
- Sistema operacional Linux, Windows ou macOS

⚠️ Não é necessário instalar Python nem bibliotecas localmente.  
Todo o ambiente é provisionado via Docker.

---

## 📂 Estrutura do projeto

pdf-to-excel/
├── app/
│   └── main.py
├── sample/
│   └── teste.pdf
├── Dockerfile
├── requirements.txt
├── README.md

---

## 🐳 Build da imagem Docker

Na raiz do projeto, execute:

docker build --no-cache -t pdf-to-excel .

Esse comando cria a imagem Docker do projeto com todas as dependências necessárias.

---

## ▶️ Executar o código (converter PDF para Excel)

### Sintaxe geral

docker run --rm \
  -v $(pwd):/data \
  pdf-to-excel \
  /data/caminho/arquivo.pdf /data/saida.xlsx

### Exemplo prático

docker run --rm \
  -v $(pwd):/data \
  pdf-to-excel \
  /data/sample/teste.pdf /data/resultado.xlsx

Explicação:
- --rm remove o container após a execução
- -v $(pwd):/data monta o diretório atual no container
- /data/sample/teste.pdf é o PDF de entrada
- /data/resultado.xlsx é o arquivo Excel gerado no host

---

## 📊 Resultado

Após a execução, o arquivo resultado.xlsx será criado na raiz do projeto,
contendo todas as tabelas extraídas e consolidadas.

Para abrir:

libreoffice resultado.xlsx

Ou utilize Excel / Google Sheets.

---

## ⚠️ Observações importantes

- O projeto funciona apenas com PDFs textuais
- PDFs escaneados (imagem) não são suportados
- Para verificar se o PDF é textual:
  - tente selecionar o texto no visualizador de PDF
  - ou use:
    pdftotext arquivo.pdf -

---

## 🧪 Problemas comuns

Nenhuma tabela detectada:
- O PDF não possui tabelas estruturadas
- O layout do documento não é compatível com extração automática

PDF sem conteúdo textual:
- O arquivo é escaneado
- Será necessário OCR (não incluído neste projeto)

---

## 📌 Licença

Projeto de uso livre para fins educacionais, internos ou experimentais.
