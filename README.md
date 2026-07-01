# PanarooMLPrep
A preprocessing toolkit for cleaning, filtering, and preparing Panaroo pangenome outputs for downstream GWAS and machine learning analyses.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)]()

A Python toolkit for preprocessing **Panaroo** pangenome outputs for downstream **genome-wide association studies (GWAS)** and **machine learning (ML)** analyses.

This toolkit standardizes gene annotations, removes low-information genes, merges duplicated gene names, filters rare genes, and prepares clean feature matrices suitable for biomarker discovery.

---

## Features

- Clean Panaroo gene presence/absence matrices
- Remove low-information genes
  - Hypothetical proteins
  - Mobile genetic elements
  - Transposases
  - Integrases
  - Recombinases
  - Phage-related genes
- Merge duplicated gene annotations
- Filter low-prevalence genes
- Generate cleaned `.Rtab` matrices
- Prepare Panaroo GWAS output for downstream ML analysis
- Preserve annotation information for biological interpretation

---

## Repository Structure

```
panaroo-preprocessor/
│
├── scripts/
│   ├── panaroo_clean.py
│   └── prepare_ml_features.py
│
├── docs/
│
├── example/
│
├── tests/
│
├── requirements.txt
├── environment.yml
├── LICENSE
└── README.md
```

---

# Workflow

```
                     Panaroo

          gene_presence_absence.csv
          gene_presence_absence.Rtab
                     │
                     ▼
          panaroo_clean.py
                     │
     ┌───────────────┼────────────────┐
     │               │                │
     ▼               ▼                ▼
Clean RTAB     Gene Mapping     Removed Genes
     │
     ▼
Panaroo GWAS
     │
     ▼
prepare_ml_features.py
     │
     ▼
Machine Learning Ready Dataset
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/Prasanna004/panarooMLPrep.git

cd panarooMLPrep
```

Install dependencies

```bash
pip install -r requirements.txt
```

or

```bash
conda env create -f environment.yml

conda activate panarooMLPrep
```

---

# Required Input Files

## Step 1

```
gene_presence_absence.csv

gene_presence_absence.Rtab
```

## Step 2

```
Panaroo_GWAS_results.csv

panaroo_mapping.csv
```

---

# Usage

## Step 1 – Clean Panaroo Output

```bash
python scripts/panaroo_clean.py
```

Outputs

```
panaroo_cleaned.Rtab

panaroo_mapping_clean.csv

panaroo_removed_genes.csv
```

---

## Step 2 – Prepare ML Dataset

```bash
python scripts/prepare_ml_features.py
```

Output

```
Panaroo_ML_ready.csv
```

---

# Output Files

| File | Description |
|------|-------------|
| panaroo_cleaned.Rtab | Cleaned presence/absence matrix |
| panaroo_mapping_clean.csv | Gene annotation mapping |
| panaroo_removed_genes.csv | Removed low-information genes |
| Panaroo_ML_ready.csv | Machine-learning-ready feature table |

---

# Applications

This toolkit is suitable for

- Bacterial Genome-Wide Association Studies (GWAS)
- Comparative Genomics
- Pangenome Analysis
- Biomarker Discovery
- Machine Learning
- Feature Engineering
- Gene Prioritization

---

# Tested With

- Panaroo
- Python 3.9+
- pandas
- NumPy

---

# Citation

If you use this repository in your research, please cite the repository and the associated publication (when available).

---

# Author

**Prasanna Selvam**

PhD Researcher – Institute of Bioinformatics, Bangalore


Research Interests

- Comparative Genomics
- Pangenome Analysis
- Machine Learning
- Antimicrobial Resistance
- Biomarker Discovery

GitHub:
https://github.com/Prasanna004

---

# License

This project is licensed under the MIT License.

---

## Future Development

Planned features include

- Automatic prevalence threshold selection
- Command-line interface (CLI)
- HTML reports
- Summary statistics
- Gene prevalence visualization
- Consensus feature ranking
- Direct integration with machine learning workflows
