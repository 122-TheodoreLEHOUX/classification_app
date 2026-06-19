import pandas as pd
from pathlib import Path

qqa_path = Path(r"\\sfvbn607184x001\Operations\METHOD_TOOLS\040_SUPPORT_EXPERTISE\QQA_v1.xlsx")
export_path = Path(r"\\sfvbn607184x001\Operations\METHOD_TOOLS\OUT\DEV_TLX_export_repair_report\Expertise\MT_repair_report.parquet")

# ------------------------------------------------------------
# 0) Load
# ------------------------------------------------------------
df = pd.read_excel(
    qqa_path,
    sheet_name="repair_data",
    engine="openpyxl"
).dropna(subset=["Notification"])

update_df = pd.read_parquet(export_path).drop_duplicates(subset="Notification")

# Normalize key columns
df["OS"] = df["OS"].astype(str).str.strip()
update_df["OS"] = update_df["OS"].astype(str).str.strip()

df["Notification"] = df["Notification"].astype(str).str.strip()
update_df["Notification"] = update_df["Notification"].astype(str).str.strip()

print("qqa shape :", df.shape)
print("parquet shape :", update_df.shape)

# ------------------------------------------------------------
# 1) Split rows where RepairReport is empty / not empty
# ------------------------------------------------------------
repair_report_empty = (
    df["RepairReport"].isna()
    | df["RepairReport"].astype(str).str.strip().eq("")
)

no_report = df.loc[repair_report_empty].copy()
unchanged = df.loc[~repair_report_empty].copy()

# ------------------------------------------------------------
# 2) Merge only rows to process, for keep/update logic
# ------------------------------------------------------------
merged_df = pd.merge(
    no_report,
    update_df,
    on="Notification",
    how="outer",
    indicator=True,
    suffixes=("_left", "")
)

# ------------------------------------------------------------
# 3) Cases from merge
# ------------------------------------------------------------
# IMPORTANT:
# - to_keep_df and to_update_df come from no_report vs update_df
# - to_add_df must be computed against FULL df, not only no_report
to_keep_df = merged_df.loc[merged_df["_merge"].eq("left_only")].copy()
to_update_df = merged_df.loc[merged_df["_merge"].eq("both")].copy()

# Rows in update_df whose OS does not exist anywhere in df
existing_notif = set(df["Notification"])
to_add_df = update_df.loc[~update_df["Notification"].isin(existing_notif)].copy()

print("to_add:", len(to_add_df))
print("to_keep:", len(to_keep_df))
print("to_update:", len(to_update_df))

# ------------------------------------------------------------
# 4) Columns to preserve from left dataframe when row exists in both
# ------------------------------------------------------------
left_cols_to_keep = [
    "FI_classification",
    "FailureType",
    "Repa_classification",
    "Card_Comp_changed",
    "Notes",
]

# Final schema
final_columns = list(dict.fromkeys(list(df.columns) + list(update_df.columns)))

# ------------------------------------------------------------
# 5) Build updated rows
# ------------------------------------------------------------
updated_rows = pd.DataFrame(index=to_update_df.index)

for col in final_columns:
    if col in to_update_df.columns:
        updated_rows[col] = to_update_df[col]
    elif f"{col}_left" in to_update_df.columns:
        updated_rows[col] = to_update_df[f"{col}_left"]
    else:
        updated_rows[col] = pd.NA

# Override selected columns with values from LEFT dataframe
for col in left_cols_to_keep:
    left_col = f"{col}_left" if f"{col}_left" in to_update_df.columns else col
    if left_col in to_update_df.columns:
        updated_rows[col] = to_update_df[left_col]

# ------------------------------------------------------------
# 6) Helper for merged parts (left_only)
# ------------------------------------------------------------
def rebuild_frame(merged_part: pd.DataFrame, final_columns: list[str]) -> pd.DataFrame:
    rebuilt = pd.DataFrame(index=merged_part.index)

    for col in final_columns:
        if col in merged_part.columns:
            rebuilt[col] = merged_part[col]
        elif f"{col}_left" in merged_part.columns:
            rebuilt[col] = merged_part[f"{col}_left"]
        else:
            rebuilt[col] = pd.NA

    return rebuilt

kept_rows = rebuild_frame(to_keep_df, final_columns)

# ------------------------------------------------------------
# 7) Build added rows directly from update_df-based to_add_df
# ------------------------------------------------------------
added_rows = to_add_df.reindex(columns=final_columns)

# ------------------------------------------------------------
# 8) Align unchanged rows
# ------------------------------------------------------------
unchanged_aligned = unchanged.reindex(columns=final_columns)

# ------------------------------------------------------------
# 9) Final concat
# ------------------------------------------------------------
final_df = pd.concat(
    [
        unchanged_aligned,
        kept_rows,
        updated_rows,
        added_rows,
    ],
    ignore_index=True
)

final_df = final_df.drop(columns=["_merge"], errors="ignore")

# ------------------------------------------------------------
# 10) Write back ONLY repair_data sheet
# ------------------------------------------------------------
with pd.ExcelWriter(
    qqa_path,
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:
    final_df.to_excel(writer, sheet_name="repair_data", index=False)

print(f"'repair_data' sheet updated successfully in: {qqa_path}")
print("final shape :", final_df.shape)


wb = load_workbook(qqa_path)
ws = wb["repair_data"]

# Remove existing tables in the sheet (important if script runs multiple times)
if ws.tables:
    table_names = list(ws.tables.keys())
    for table_name in table_names:
        del ws.tables[table_name]

# Create table only if there is data
if ws.max_row >= 1 and ws.max_column >= 1:
    table_ref = ws.dimensions  # e.g. A1:Z245

    tab = Table(displayName="RepairDataTable", ref=table_ref)

    style = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False
    )
    tab.tableStyleInfo = style
    ws.add_table(tab)

wb.save(qqa_path)

print(f"'repair_data' sheet updated successfully as Excel table in: {qqa_path}")
