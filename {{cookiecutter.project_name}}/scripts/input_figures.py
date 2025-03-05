import pandas as pd
import os
import shutil

# Get paths from environment variables
MARKDOWN_DIR = os.getenv('MARKDOWN_DIR', 'markdown')
BUILD_PROCESSED_DIR = os.getenv('BUILD_PROCESSED_DIR', 'build/processed')
DOCS_DIR = os.getenv('DOCS_DIR', 'docs')
FIGURES_DIR = os.getenv('FIGURES_DIR', 'figures')
EXCEL_FILE = os.getenv('EXCEL_FILE', 'figures.xlsx')

# Load figure tracking data
df = pd.read_excel(EXCEL_FILE)

# Define figure templates
final_figure_template = """
{% raw %}![Figure {num}: {fig_name}]({FIGURES_DIR}/{folder}/{filename}){{#fig:{label} width=80%}}{% endraw %}

*{fig_description}*
"""

draft_figure_template = """
> **DRAFT FIGURE {num}: {label}**  
> _{fig_description}_  
"""

# Dictionary to store figure replacements
figure_dict = {}
main_count = 1
supp_count = 1

# Check for missing figures
missing_figures = []

for _, row in df.iterrows():
    label = row["Label"].strip()
    filename = row["Filename"].strip()
    fig_name = row["Figure Name"].strip()
    fig_description = row["Figure Description"].strip()
    status = row["Status"].strip().lower()
    folder = row["Folder"].strip().lower()
    category = row["Category"].strip().lower()

    file_path = os.path.join(FIGURES_DIR, folder, filename)

    # Check if figure file exists (only for final figures)
    if status == "final" and not os.path.exists(file_path):
        missing_figures.append(f"{filename} (Label: {label})")

    # Assign correct numbering
    if category == "supplemental":
        figure_num = f"S{supp_count}"
        supp_count += 1
    else:
        figure_num = str(main_count)
        main_count += 1

    # Choose correct template and store in dictionary
    if status == "draft":
        figure_block = draft_figure_template.format(
            num=figure_num,
            label=label,
            fig_description=fig_description
        )
    else:
        figure_block = final_figure_template.format(
            num=figure_num,
            folder=folder,
            filename=filename,
            fig_name=fig_name,
            fig_description=fig_description,
            label=label,
            FIGURES_DIR=FIGURES_DIR
        )
    
    {% raw %}figure_dict[f"{{FIG:{label}}}"] = figure_block{% endraw %}

def process_files(input_folder, output_folder, file_order=None):
    """Process markdown files from input folder and save to output folder"""
    os.makedirs(output_folder, exist_ok=True)
    combined_content = ""
    
    if file_order is None:
        file_order = sorted([f for f in os.listdir(input_folder) if f.endswith('.md')])
    
    for filename in file_order:
        input_path = os.path.join(input_folder, filename)
        if os.path.exists(input_path):
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Replace figure placeholders
                processed_content = content
                for placeholder, figure_block in figure_dict.items():
                    processed_content = processed_content.replace(placeholder, figure_block)
                
                # Save processed file to output directory
                output_path = os.path.join(output_folder, filename)
                with open(output_path, "w", encoding="utf-8") as out_f:
                    out_f.write(processed_content)
                
                # Add to combined content only for processed_markdown
                if output_folder == BUILD_PROCESSED_DIR:
                    combined_content += f"\n\n{processed_content}\n\n"
    
    return combined_content

# Get ordered list of markdown files based on numerical prefixes
def get_ordered_files(directory):
    """Get list of markdown files ordered by their numerical prefix"""
    files = [f for f in os.listdir(directory) if f.endswith('.md')]
    # Sort files based on numerical prefix (if present) or filename
    return sorted(files, key=lambda x: (
        # Extract number from start of filename, default to 999 if no number
        int(''.join(filter(str.isdigit, x.split('_')[0])) or '999'),
        x  # Secondary sort by full filename
    ))

# Process files for PDF/HTML output (combined file)
file_order = get_ordered_files(MARKDOWN_DIR)
combined_content = process_files(MARKDOWN_DIR, BUILD_PROCESSED_DIR, file_order)

# Save combined file
with open(os.path.join(BUILD_PROCESSED_DIR, "combined.md"), "w", encoding="utf-8") as f:
    f.write(combined_content.strip())

# Process files for mkdocs (individual files)
process_files(MARKDOWN_DIR, DOCS_DIR, file_order)

# Print missing figure warnings
if missing_figures:
    print("\n⚠️ WARNING: The following figure files are missing:")
    for missing in missing_figures:
        print(f"  - {missing}")

print("\n✅ Figures inserted and missing figures checked.")
print(f"Files processed for both PDF/HTML ({BUILD_PROCESSED_DIR}/) and mkdocs ({DOCS_DIR}/)")
