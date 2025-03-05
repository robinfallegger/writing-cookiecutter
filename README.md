# CookieCutter template for scientific writing

A template for academic documents that can be built as both PDF (via LaTeX) and website (via MkDocs).

## Project Structure

```
.
├── README.md               # Project documentation
├── Makefile               # Build automation
├── environment.yml        # Conda environment specification
├── figures.xlsx           # Figure tracking spreadsheet
│
├── markdown/              # Source markdown content
│   ├── 01_*.md           # Numbered markdown files for automatic ordering
│   └── ...
│
├── figures/              # Figure assets
│   ├── main/            # Main document figures
│   └── supplemental/    # Supplementary figures
│
├── config/              # Configuration files
│   ├── main.tex        # LaTeX template
│   ├── config.yaml     # PDF/LaTeX configuration for Pandoc
│   ├── references.bib  # Bibliography database
│   └── apa.csl         # Citation style
│
├── scripts/            # Processing scripts
│   ├── input_figures.py # Figure processing
│   └── filter_bib.py   # Bibliography filtering
│
├── docs/              # MkDocs source (processed from markdown/)
│   └── assets/       # Site assets (CSS, JS)
│
├── build/            # Build artifacts
│   ├── pdf/         # PDF output
│   └── processed/   # Processed markdown
│
└── site/            # MkDocs generated site
```

## Configuration

### Document Settings
- Title and metadata: Edit `config/config.yaml` for pdf and `mkdocs.yml` + `docs/index.md` for mkdocs
- LaTeX template: Edit `config/main.tex`

### Figure Management
- Add figures to `figures/` directory
- Track figures in `figures.xlsx` with the following columns:
  - Label: Reference label used in markdown (e.g., "fig1")
  - Filename: Image filename
  - Figure Name: Caption title
  - Figure Description: Full caption text
  - Status: "draft" or "final"
  - Folder: "main" or "supplemental"
  - Category: "main" or "supplemental"

### Website Settings
- Site configuration: Edit `mkdocs.yml`
- Custom styling: Edit `docs/assets/stylesheets/style.css`
- JavaScript: Add to `docs/assets/javascripts/`

## Usage

1. Set up the environment:
```bash
conda env create -f environment.yml
conda activate panmkdocs
```

2. Build commands:
- PDF: `make pdf`
- Website: `make mkdocs`
- Clean build: `make clean`

## File Naming Convention

- Markdown files: Use numerical prefixes (e.g., "01_introduction.md")
- Figures: Use descriptive names matching figures.xlsx entries
- Keep original files in `markdown/` directory

## Dependencies

- Python 3.10+
- Conda/Mamba
- LaTeX distribution
- Required Python packages in environment.yml