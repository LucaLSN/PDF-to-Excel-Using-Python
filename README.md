# PDF to Excel using Python

Este projeto converte tabelas presentes em arquivos **PDF** para um arquivo **Excel (.xlsx)** estruturado e tratado, aplicando regras de negócio automaticamente (modalidade, bandeira e número de parcelas).

O processamento foi desenvolvido para lidar com PDFs reais, incluindo:
- múltiplas páginas,
- quebras de linha em células,
- tabelas mal formatadas,
- textos fragmentados.

---

## 🚀 Funcionalidades

- 📄 Detecta automaticamente páginas com conteúdo no PDF
- 📊 Extrai tabelas usando **Camelot**
- 🧹 Corrige quebras de linha em células
- 📈 Consolida todas as tabelas em um único Excel
- 🐳 Executável via **Docker** (sem dependências locais)

---

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- pdfplumber
- camelot
- pandas
- Docker

---

## 📁 Estrutura do Projeto

pdf-to-excel-using-python/
├── app/
│ ├── init.py
│ └── main.py
├── sample/
├── Dockerfile
├── requirements.txt
└── README.md
