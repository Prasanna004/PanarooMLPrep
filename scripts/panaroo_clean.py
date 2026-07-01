#!/usr/bin/env python3

import pandas as pd
import numpy as np

# ==========================
# CONFIG
# ==========================

GPA_CSV = "gene_presence_absence.csv"
RTAB = "gene_presence_absence.Rtab"

MIN_PRESENCE = max(5, int(0.005 * number_of_isolates))

REMOVE_TERMS = [
    "hypothetical protein",
    "transposase",
    "integrase",
    "recombinase",
    "phage",
    "mobile element",
    "insertion sequence",
    "is element",
    "site-specific recombinase",
    "tyrosine recombinase"
]

# ==========================
# LOAD ANNOTATION TABLE
# ==========================

print("Loading gene_presence_absence.csv ...")

gpa = pd.read_csv(GPA_CSV, low_memory=False)

mapping = gpa[
    ["Gene", "Non-unique Gene name", "Annotation"]
].copy()

mapping["Non-unique Gene name"] = (
    mapping["Non-unique Gene name"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# Prefer non-unique gene name if available
mapping["FinalGene"] = np.where(
    mapping["Non-unique Gene name"] != "",
    mapping["Non-unique Gene name"],
    mapping["Gene"]
)

# ==========================
# REMOVE NOISE
# ==========================

annotation = (
    mapping["Annotation"]
    .fillna("")
    .astype(str)
    .str.lower()
)

mask = np.ones(len(mapping), dtype=bool)

for term in REMOVE_TERMS:
    mask &= ~annotation.str.contains(term, regex=False)

mapping_clean = mapping[mask].copy()

mapping_clean.to_csv(
    "panaroo_mapping_clean.csv",
    index=False
)

removed = mapping[~mask].copy()
removed.to_csv(
    "panaroo_removed_genes.csv",
    index=False
)

print("Genes retained :", len(mapping_clean))
print("Genes removed  :", len(removed))

# ==========================
# LOAD RTAB
# ==========================

print("Loading RTAB ...")

rtab = pd.read_csv(
    RTAB,
    sep="\t",
    low_memory=False
)

gene_col = rtab.columns[0]

# keep only retained genes
rtab = rtab[
    rtab[gene_col].isin(mapping_clean["Gene"])
].copy()

# mapping dictionary
gene_map = dict(
    zip(
        mapping_clean["Gene"],
        mapping_clean["FinalGene"]
    )
)

rtab[gene_col] = rtab[gene_col].map(gene_map)

# ==========================
# MERGE DUPLICATE GENE NAMES
# ==========================

print("Merging duplicated annotations ...")

sample_cols = list(rtab.columns[1:])

merged = (
    rtab
    .groupby(gene_col)[sample_cols]
    .max()
    .reset_index()
)

# ==========================
# REMOVE RARE GENES
# ==========================

presence = merged[sample_cols].sum(axis=1)

merged = merged[
    presence >= MIN_PRESENCE
].copy()

print("Genes after rarity filter :", len(merged))

# ==========================
# SAVE CLEAN RTAB
# ==========================

merged.to_csv(
    "panaroo_cleaned.Rtab",
    sep="\t",
    index=False
)

print("\nGenerated files:")
print("  panaroo_cleaned.Rtab")
print("  panaroo_mapping_clean.csv")
print("  panaroo_removed_genes.csv")

print("\nDone.")
