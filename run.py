from pathlib import Path
import pandas as pd

from scripts.notebooks.combine_functions import clean_supplier1, clean_supplier2, merge_suppliers
from scripts.notebooks.rfq_similarity_functions import prepare_rfq_reference, compute_similarity_top3


def main():
    # === Paths
    DATA = Path("data")
    OUTPUT = Path("output")
    OUTPUT.mkdir(exist_ok=True)

    # === Step 1: Clean & combine supplier data
    df1 = pd.read_excel(DATA / "supplier_data1.xlsx")
    df2 = pd.read_excel(DATA / "supplier_data2.xlsx")

    df1_clean = clean_supplier1(df1)
    df2_clean = clean_supplier2(df2)
    inventory = merge_suppliers(df1_clean, df2_clean)
    inventory.to_csv(OUTPUT / "inventory_dataset.csv", index=False)

    # === Step 2: Enrich RFQ and compute similarities
    df_rfq = pd.read_csv(DATA / "rfq.csv")
    df_ref = pd.read_csv(DATA / "reference_properties.tsv", sep="\t")

    df_joined = prepare_rfq_reference(df_rfq, df_ref)
    top3 = compute_similarity_top3(df_joined)
    top3.to_csv(OUTPUT / "top3.csv", index=False)

    print("✅ Pipeline completed: inventory_dataset.csv and top3.csv generated.")


if __name__ == "__main__":
    main()