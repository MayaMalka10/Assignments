import csv
from pathlib import Path


def calculate_fold_change(
    control_target_ct: float,
    control_reference_ct: float,
    treated_target_ct: float,
    treated_reference_ct: float,
) -> float:
    """Calculate fold change using the 2^(-delta delta Ct) method."""
    control_delta_ct = control_target_ct - control_reference_ct
    treated_delta_ct = treated_target_ct - treated_reference_ct
    delta_delta_ct = treated_delta_ct - control_delta_ct
    return 2 ** (-delta_delta_ct)


def read_qpcr_data(file_path: Path) -> dict[str, tuple[float, float]]:
    with file_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required_columns = {"Sample", "Target_Ct", "Reference_Ct"}
        if reader.fieldnames is None or not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                "The CSV file must contain Sample, Target_Ct, and Reference_Ct columns."
            )

        samples = {}
        for row in reader:
            sample = row["Sample"]
            if not sample:
                raise ValueError("Each row must contain a sample name.")
            samples[sample] = (float(row["Target_Ct"]), float(row["Reference_Ct"]))

    return samples


if __name__ == "__main__":
    data = read_qpcr_data(Path(__file__).with_name("qpcr_data.csv"))

    try:
        control_target, control_reference = data["Control"]
        treated_target, treated_reference = data["Treated"]
    except KeyError as error:
        raise ValueError("The CSV file must contain Control and Treated samples.") from error

    fold_change = calculate_fold_change(
        control_target,
        control_reference,
        treated_target,
        treated_reference,
    )
    print(f"Fold Change for Treated: {fold_change:.2f}")