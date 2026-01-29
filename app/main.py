import sys
import pdfplumber
import camelot
import pandas as pd

"""
    Extrai tabelas de qualquer PDF e consolida em um Excel.
    
    Parâmetros:
    - pdf_path: caminho do PDF
    - output_excel: nome do arquivo Excel de saída
    - coluna_quebra: índice da coluna usada para detectar quebra de linha
    - row_tol: tolerância de linha do Camelot (stream)
    """

def processar_pdf_para_excel(
    pdf_path,
    output_excel="tabelas_extraidas.xlsx",
    coluna_quebra=1,
    row_tol=15
):

    paginas_validas = []

    #identificação de conteúdo
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            texto = page.extract_text()
            if texto and texto.strip():
                paginas_validas.append(i)

    if not paginas_validas:
        raise ValueError("Nenhuma página com conteúdo textual encontrada no PDF.")

    #extração de conteúdo
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

        linhas_para_remover = []

        
        for i in range(1, len(df)):
            atual = df.iloc[i, coluna_quebra]
            anterior = df.iloc[i - 1, coluna_quebra]

            if atual and not anterior:
                df.iloc[i - 1, coluna_quebra] = f"{anterior} {atual}".strip()
                linhas_para_remover.append(i)

        df.drop(index=linhas_para_remover, inplace=True)
        df.reset_index(drop=True, inplace=True)

        # Limpeza básica
        df = df.replace("\n", " ", regex=True)
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        dataframes.append(df)

   
    df_final = pd.concat(dataframes, ignore_index=True)

    #se a primeira linha parecer cabeçalho, usa como coluna
    if df_final.iloc[0].duplicated().sum() == 0:
        df_final.columns = df_final.iloc[0]
        df_final = df_final[1:].reset_index(drop=True)

    df_final.columns = df_final.columns.astype(str).str.strip()

    df_final.to_excel(output_excel, index=False)

    return output_excel


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    processar_pdf_para_excel(pdf_path)
