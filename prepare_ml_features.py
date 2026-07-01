#!/usr/bin/env python3

"""
Prepare Panaroo GWAS results for ML

Inputs:
    Panaroo_GWAS_results.csv
    panaroo_mapping.csv

Outputs:
    Panaroo_ML_ready.csv

No statistical filtering is applied.
Only gene-name cleanup and annotation mapping.
"""

import re
import pandas as pd

print("=" * 80)
print("PREPARING PANAROO FEATURES FOR ML")
print("=" * 80)

# ----------------------------------------------------
# Load files
# ----------------------------------------------------

gwas = pd.read_csv("Panaroo_GWAS_results.csv")
mapping = pd.read_csv("panaroo_mapping.csv")

print(f"GWAS rows    : {len(gwas)}")
print(f"Mapping rows : {len(mapping)}")

# ----------------------------------------------------
# Clean mapping table
# ----------------------------------------------------

mapping["Gene_Name"] = (
    mapping["Gene_Name"]
    .fillna("")
    .astype(str)
)

mapping["Annotation"] = (
    mapping["Annotation"]
    .fillna("")
    .astype(str)
)

# fallback to original cluster ID if Gene_Name missing
mapping.loc[
    mapping["Gene_Name"].str.strip() == "",
    "Gene_Name"
] = mapping.loc[
    mapping["Gene_Name"].str.strip() == "",
    "Gene"
]

mapping_lookup = mapping.set_index("Gene")

# ----------------------------------------------------
# Canonicalize merged names
# ----------------------------------------------------

def clean_gene_name(x):

    if pd.isna(x):
        return ""

    tokens = str(x).split(";")

    cleaned = []

    for token in tokens:

        token = token.strip()

        if token == "":
            continue

        # remove suffix _1 _2 _3 etc
        token = re.sub(r"_[0-9]+$", "", token)

        cleaned.append(token)

    cleaned = sorted(set(cleaned))

    return ";".join(cleaned)

gwas["ML_Gene"] = gwas["Gene"].apply(clean_gene_name)

# ----------------------------------------------------
# Add annotation
# ----------------------------------------------------

gene_names = []
annotations = []

for gene in gwas["Gene"]:

    if gene in mapping_lookup.index:

        gene_names.append(
            mapping_lookup.loc[gene, "Gene_Name"]
        )

        annotations.append(
            mapping_lookup.loc[gene, "Annotation"]
        )

    else:

        gene_names.append(gene)
        annotations.append("")

gwas["Mapped_Gene_Name"] = gene_names
gwas["Annotation"] = annotations

# ----------------------------------------------------
# Reorder columns
# ----------------------------------------------------

priority = [
    "Gene",
    "ML_Gene",
    "Mapped_Gene_Name",
    "Annotation"
]

remaining = [
    c for c in gwas.columns
    if c not in priority
]

gwas = gwas[
    priority + remaining
]

# ----------------------------------------------------
# Save
# ----------------------------------------------------

gwas.to_csv(
    "Panaroo_ML_ready.csv",
    index=False
)

print()
print("=" * 80)
print("DONE")
print("=" * 80)
print(f"Rows retained : {len(gwas)}")
print("No genes removed.")
print("Output: Panaroo_ML_ready.csv")
print("=" * 80)

