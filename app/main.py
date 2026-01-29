import sys
import pdfplumber
import camelot
import pandas as pd


def processar_pdf_para_excel(
    pdf_path,
    output_excel="tabelas_extraidas.xlsx",
    coluna_quebra=1,
    row_tol=15
):
    """
    Extrai tabelas de um PDF textual e consolida em um arquivo Excel.

    Parâmetros:
    - pdf_path: caminho do PDF
    - output_excel: nome do arquivo Excel de saída
    - coluna_quebra: índice da coluna usada para detectar quebra de linha
    - row_tol: tolerância de linha do Camelot (stream)
    """

    paginas_validas = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            texto = page.extract_text()
            if texto and texto.strip():
                paginas_validas.append(i)

    if not paginas_validas:
        raise ValueError("Nenhuma página com conteúdo textual encontrada no PDF.")

    tables = camelot.read_pdf(
        pdf_path,
        pages=",".join(map(str, paginas_validas)),
        flavor="stream",
        split_text=False,
        row_tol=row_tol
    )

    if tables.n == 0:
        raise ValueError("Nenhuma tabela detectada no PDF.")

    dataframes = []


    for table in tables:
        df = table.df.copy()

        if df.empty:
            continue

        linhas_para_remover = []

        for i in range(1, len(df)):
            atual = df.iloc[i, coluna_quebra]
            anterior = df.iloc[i - 1, coluna_quebra]

            if pd.notna(atual) and pd.isna(anterior):
                df.iloc[i - 1, coluna_quebra] = str(atual)
                linhas_para_remover.append(i)

        if linhas_para_remover:
            df.drop(index=linhas_para_remover, inplace=True)
            df.reset_index(drop=True, inplace=True)

      
        df = df.replace("\n", " ", regex=True)

        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.strip()

        dataframes.append(df)

    if not dataframes:
        raise ValueError("Nenhuma tabela válida após o processamento.")


    df_final = pd.concat(dataframes, ignore_index=True)


    primeira_linha = df_final.iloc[0].astype(str)

    if all(len(v.strip()) > 0 for v in primeira_linha):
        df_final.columns = primeira_linha
        df_final = df_final.iloc[1:].reset_index(drop=True)

    df_final.columns = (
        df_final.columns
        .astype(str)
        .str.strip()
    )


    df_final.to_excel(output_excel, index=False)

    return output_excel

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.pdf> [arquivo_saida.xlsx]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_excel = sys.argv[2] if len(sys.argv) > 2 else "tabelas_extraidas.xlsx"

    processar_pdf_para_excel(pdf_path, output_excel)
