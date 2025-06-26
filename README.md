# Linguistic Evolution in Scientific Abstracts (1950–2024)

This repository accompanies a Master’s thesis examining diachronic shifts in the readability, linguistic structure, and rhetorical features of scientific abstracts. The study focuses on the disciplines of Environmental Science, Earth and Planetary Science, and Agricultural and Biological Science, drawing from a corpus of over 50,000 abstracts published between 1950 and 2024.

## Project Overview

The research investigates long-term changes in scientific communication, particularly within abstract writing, and assesses stylistic differences between Open Access and Conventional publishing models. Key variables include:

- Readability indices (e.g., Flesch Reading Ease, Flesch-Kincaid Grade Level, SMOG, Gunning Fog Index)
- Linguistic and rhetorical markers (e.g., passive voice ratio, hedging frequency, nominalisation)
- Lexical density and complexity trends
- Temporal evolution and stylistic convergence between access types

Data analysis was conducted using Python and Microsoft Excel, with visualisation supported by Google Colab and JuliusAI.

## Repository Structure

```
linguistic-evolution-abstracts/
├── data/
│   ├── combined_abstracts.csv              # Full dataset of processed abstracts
│   ├── raw/
│   │   ├── 1_EnvSci.7z
│   │   ├── 2_EarthandPlanSci.7z
│   │   └── 3_AgriBioSci.7z
│   └── processed/                          # Output datasets (normalised, stratified)
├── scripts/
│   └── python/                             # Analysis scripts and Colab notebooks
├── search_schema/
│   └── 0_ScopusSearchSchema/              # Original query filters and parameters
├── thesis/                                 # Final thesis manuscript (if included)
├── README.md                               # Project summary and guidance
└── LICENSE                                 # Usage and licensing information
```

## Archived Raw Data

To reduce upload volume and improve repository performance, all subject-specific raw datasets have been archived into `.7z` files. These can be found in:

- `data/raw/1_EnvSci.7z`
- `data/raw/2_EarthandPlanSci.7z`
- `data/raw/3_AgriBioSci.7z`

Each archive contains Scopus-exported CSVs used in the study. Extract using 7-Zip or any compatible decompression tool.

## Tools and Methods

- **Python** – for preprocessing, tokenisation, and metric computation (NLTK, spaCy, textstat, pandas)
- **Excel** – for cross-validation and formula-based linguistic analysis
- **Google Colab** – for scalable script execution and graph generation
- **JuliusAI** – for trend diagnostics and plotting verification

## Reproducibility

To reproduce the results:

1. Download or clone this repository
2. Navigate to `/scripts/python/` for notebooks and scripts
3. Use the combined dataset located in `/data/combined_abstracts.csv`
4. Ensure all necessary Python dependencies are installed
5. Execute the cells for metric generation, normalisation, and trend analysis

Paths may need to be updated depending on the runtime environment (e.g., local, Colab).

## Citation

If referencing this work or its analytical framework, please cite:

> Manuel, M. (2025). *Linguistic evolution in scientific abstracts across environmental sciences (1950–2024)* [Master’s thesis, Auckland University of Technology]. GitHub. https://github.com/thg2177/linguistic-evolution-abstracts

## License

This repository is distributed under the MIT License. Users are permitted to use, modify, and share this material with appropriate credit.

## Contact

For academic or research-related queries, please contact: your_email@domain.com
