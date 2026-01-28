import pdfplumber
import camelot
import pandas as pd
import re
import sys


def processar_pdf_para_excel(pdf_path, output_excel="tabela_tratada.xlsx"):
    paginas = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            texto = page.extract_text()
            if texto and texto.strip():
                paginas.append(i)

    if not paginas:
        raise ValueError("Nenhuma página com conteúdo encontrado no PDF.")

    tables = camelot.read_pdf(
        pdf_path,
        pages=",".join(map(str, paginas)),
        flavor="stream",
        split_text=False,
        row_tol=15
    )

    dataframes = []

    for table in tables:
        df = table.df.copy()
        coluna_quebra = 1
        linhas_para_remover = []

        for j in range(1, len(df)):
            if df.iloc[j, coluna_quebra] and not df.iloc[j - 1, coluna_quebra]:
                df.iloc[j - 1, coluna_quebra] += " " + df.iloc[j, coluna_quebra]
                linhas_para_remover.append(j)

        df.drop(index=linhas_para_remover, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df = df.replace("\n", " ", regex=True)

        dataframes.append(df)

    df = pd.concat(dataframes, ignore_index=True)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    df.columns = df.columns.str.strip()

    df['Modalidade'] = None
    df['Bandeira'] = None
    df['Parcelas'] = None

    df.loc[df['Forma'].str.contains('CRÉDITO', case=False, na=False), 'Modalidade'] = 'Crédito'
    df.loc[df['Forma'].str.contains('DÉBITO', case=False, na=False), 'Modalidade'] = 'Débito'

    df['Bandeira'] = df['Forma'].str.extract(
        r'(Mastercard|Visa|Elo|Amex)', flags=re.IGNORECASE
    )

    df['Parcelas'] = (
        df['Forma']
        .str.extract(r'(\d+)\s*[xX]', expand=False)
        .fillna(1)
        .astype(int)
    )

    colunas = list(df.columns)
    i = colunas.index('Forma') + 1

    for col in ['Modalidade', 'Bandeira', 'Parcelas']:
        colunas.remove(col)
        colunas.insert(i, col)
        i += 1

    df = df[colunas]
    df.to_excel(output_excel, index=False)

    return output_excel


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    processar_pdf_para_excel(pdf_path)
