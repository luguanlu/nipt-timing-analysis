"""Create local inputs for the original NIPT analysis notebooks.

The source workbook is intentionally not distributed with this repository.
"""

import argparse
from pathlib import Path

import pandas as pd


def gestational_days(value):
    """Convert the competition's week/day notation to days."""
    if pd.isna(value):
        return pd.NA
    text = str(value).strip().lower().replace("+", "")
    if "w" in text:
        weeks, days = text.split("w", 1)
        return int(float(weeks)) * 7 + int(float(days or 0))
    return pd.to_numeric(text, errors="coerce")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Original C-problem workbook")
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    male = pd.read_excel(args.input, sheet_name="男胎检测数据")
    female = pd.read_excel(args.input, sheet_name="女胎检测数据")
    for frame in (male, female):
        frame["检测孕周"] = frame["检测孕周"].map(gestational_days)
    male = male.loc[male["GC含量"] > male["GC含量"].quantile(0.05)].copy()
    female = female.loc[female["GC含量"] > female["GC含量"].quantile(0.05)].copy()
    female["abnormal"] = female["染色体的非整倍体"].notna().astype(int)

    male.to_excel(args.output_dir / "male_filtered.xlsx", index=False)
    female.to_excel(args.output_dir / "female_filtered.xlsx", index=False)

    longitudinal_columns = ["序号", "孕妇代码", "年龄", "身高", "体重", "检测孕周", "孕妇BMI", "原始读段数", "Y染色体浓度", "怀孕次数"]
    longitudinal = male[longitudinal_columns].copy()
    longitudinal = longitudinal.rename(columns={"检测孕周": "检测孕期"})
    longitudinal.to_excel(args.output_dir / "male_longitudinal.xlsx", index=False)

    qualified = longitudinal.loc[pd.to_numeric(longitudinal["Y染色体浓度"], errors="coerce") >= 0.04].copy()
    qualified = qualified.dropna(subset=["孕妇代码", "检测孕期"])
    first = qualified.loc[qualified.groupby("孕妇代码")["检测孕期"].idxmin()].copy()
    first[["孕妇BMI", "检测孕期"]].to_excel(args.output_dir / "bmi_first_threshold.xlsx", index=False)
    first[["年龄", "检测孕期", "孕妇BMI", "原始读段数", "Y染色体浓度", "怀孕次数"]].to_excel(args.output_dir / "male_first_threshold.xlsx", index=False)
    print(f"Prepared {len(male)} male records, {len(female)} female records, and {len(first)} first-threshold records.")


if __name__ == "__main__":
    main()
