# Example Dataset

This folder contains a small example dataset for testing the PanarooMLPrep workflow.

The files are reduced subsets of real Panaroo outputs and are intended only for demonstration purposes.

Contents:

- `gene_presence_absence.csv`
- `gene_presence_absence.Rtab`
- `Panaroo_GWAS_results.csv`

Run the example:

```bash
python scripts/panaroo_clean.py
python scripts/prepare_ml_features.py
```
