.PHONY: all pdf html clean figures help env mkdocs

# Directory configuration
MARKDOWN_DIR = markdown
BUILD_DIR = build
BUILD_PROCESSED_DIR = $(BUILD_DIR)/processed
BUILD_PDF_DIR = $(BUILD_DIR)/pdf
CONFIG_DIR = config
DOCS_DIR = docs
FIGURES_DIR = figures
SCRIPTS_DIR = scripts
EXCEL_FILE = figures.xlsx

# File paths
FIGURE_SCRIPT = $(SCRIPTS_DIR)/input_figures.py
CONFIG = $(CONFIG_DIR)/config.yaml
COMBINED_MD = $(BUILD_PROCESSED_DIR)/combined.md
BIB_FILE = $(CONFIG_DIR)/references.bib
FILTERED_BIB_FILE = $(CONFIG_DIR)/references_filtered.bib
PYTHON_SCRIPT = $(SCRIPTS_DIR)/filter_bib.py

# Build configuration
TEX_ENGINE = xelatex

# Export variables for Python scripts
export MARKDOWN_DIR BUILD_DIR BUILD_PROCESSED_DIR BUILD_PDF_DIR CONFIG_DIR DOCS_DIR FIGURES_DIR EXCEL_FILE BIB_FILE FILTERED_BIB_FILE

all: pdf mkdocs

env-update:
	mamba env update -f environment.yml

# Process figures and generate markdown files
figures:
	python $(FIGURE_SCRIPT)

# Rule to filter the .bib file
fbib: 
	@echo "🔍 Filtering .bib file based on citations in Markdown files..."
	python $(PYTHON_SCRIPT)

# Build PDF with appropriate thesis styling
pdf: figures fbib
	@echo "Building PDF output..."
	@mkdir -p $(BUILD_PDF_DIR)
	# Copy bibliography file to build directory
	cp $(FILTERED_BIB_FILE) $(BUILD_PDF_DIR)/
	pandoc \
		--defaults=$(CONFIG) \
		--lua-filter=$(CONFIG_DIR)/replace-emph.lua \
		--biblatex \
		--number-sections \
		--top-level-division=chapter \
		-o $(BUILD_PDF_DIR)/thesis.tex \
		$(COMBINED_MD)
	cd $(BUILD_PDF_DIR) && $(TEX_ENGINE) thesis.tex	
	cd $(BUILD_PDF_DIR) && biber --input-directory=. thesis
	cd $(BUILD_PDF_DIR) && $(TEX_ENGINE) thesis.tex
	cd $(BUILD_PDF_DIR) && $(TEX_ENGINE) thesis.tex
	# Clean up copied bibliography file
	rm $(BUILD_PDF_DIR)/references_filtered.bib

mkdocs: figures fbib
	mkdocs build

serve: figures fbib
	mkdocs serve

clean:
	rm -rf $(BUILD_DIR)/*
	rm -rf build/pdf/*.{aux,bbl,bcf,blg,log,out,run.xml,toc}
	rm -rf site/
	rm -rf build/processed/*
	rm -f $(FILTERED_BIB_FILE)

# Show help
help:
	@echo "Available targets:"
	@echo "  make env       - Create mamba environment"
	@echo "  make env-update - Update mamba environment"
	@echo "  make figures  - Process figures from Excel and update markdown"
	@echo "  make pdf     - Build PDF version of the thesis"
	@echo "  make html    - Build HTML version of the thesis"
	@echo "  make mkdocs  - Start mkdocs development server"
	@echo "  make all     - Build both PDF and HTML versions"
	@echo "  make clean   - Remove generated files"