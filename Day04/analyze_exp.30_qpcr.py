from pathlib import Path

import pandas as pd


INPUT_FILE = Path(__file__).with_name("EXP.30 Results.xlsx")
REFERENCE_GENE = "GAPDH"
TARGET_GENE = "RRBP1"


def calculate_fold_change(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate dCt, ddCt, and 2^-ddCt for each treated sample."""
    required_columns = {"Sample Name", "Target Name", "Ct Mean"}
    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing_columns))}")

    measurements = data.copy()
    measurements["Sample Name"] = measurements["Sample Name"].str.strip()
    measurements["Target Name"] = measurements["Target Name"].str.strip()

    gene_cts = measurements.pivot(
        index="Sample Name",
        columns="Target Name",
        values="Ct Mean",
    )
    for gene in (REFERENCE_GENE, TARGET_GENE):
        if gene not in gene_cts.columns:
            raise ValueError(f"The input data does not contain the {gene} gene.")

    sample_cts = gene_cts[[TARGET_GENE, REFERENCE_GENE]].dropna()
    sample_cts["dCt"] = sample_cts[TARGET_GENE] - sample_cts[REFERENCE_GENE]

    treated = sample_cts.loc[
        sample_cts.index.str.startswith("siRRBP1 ")
    ].copy()
    treated["concentration"] = treated.index.str.extract(
        r"^siRRBP1\s+(.+)$", expand=False
    )
    controls = sample_cts.loc[sample_cts.index.str.startswith("siNT ")].copy()
    controls["concentration"] = controls.index.str.extract(
        r"^siNT\s+(.+)$", expand=False
    )

    if treated.empty or controls.empty:
        raise ValueError("The input data must contain siRRBP1 and siNT samples.")

    treated = treated.reset_index(names="Sample Name")
    controls = controls.reset_index(names="Control Name")
    results = treated.merge(
        controls[["Control Name", "concentration", "dCt"]],
        on="concentration",
        how="left",
        suffixes=("", "_control"),
        validate="many_to_one",
    )
    if results["dCt_control"].isna().any():
        missing = results.loc[results["dCt_control"].isna(), "concentration"].tolist()
        raise ValueError(f"No matching siNT control found for concentration(s): {missing}")

    results["ddCt"] = results["dCt"] - results["dCt_control"]
    results["Fold Change"] = 2 ** (-results["ddCt"])
    return results[["Sample Name", "Control Name", "dCt", "ddCt", "Fold Change"]]


if __name__ == "__main__":
    qpcr_data = pd.read_excel(
        INPUT_FILE,
        usecols=["Sample Name", "Target Name", "Ct Mean"],
    )
    fold_change_results = calculate_fold_change(qpcr_data)
    print(fold_change_results.to_string(index=False, float_format=lambda value: f"{value:.4f}"))