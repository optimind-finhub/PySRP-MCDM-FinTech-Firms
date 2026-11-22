import io
import pandas as pd

def generate_excel_report(df_rank, R, Theta):

    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:

        df_rank.to_excel(writer, sheet_name="Final Ranking", index=False)
        pd.DataFrame(R).to_excel(writer, sheet_name="Ranking Matrix", index=False)
        pd.DataFrame(Theta).to_excel(writer, sheet_name="Weighted Matrix", index=False)

    buffer.seek(0)

    return buffer.getvalue()
