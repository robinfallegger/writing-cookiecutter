import os
import re

# Get paths from environment variables
BIB_FILE = os.getenv('BIB_FILE', 'config/references.bib')
FILTERED_BIB_FILE = os.getenv('FILTERED_BIB_FILE', 'config/references_filtered.bib')
MARKDOWN_DIR = os.getenv('MARKDOWN_DIR', 'markdown')

def extract_citation_keys(md_folder):
    """Extract all citation keys from Markdown files."""
    citation_keys = set()
    citation_pattern = re.compile(r"@([\w\-_:.]+)")  # Support letters, numbers, _, -, :

    for filename in os.listdir(md_folder):
        if filename.endswith(".md"):
            with open(os.path.join(md_folder, filename), "r", encoding="utf-8") as f:
                content = f.read()
                matches = citation_pattern.findall(content)
                citation_keys.update(matches)

    if not citation_keys:
        print("⚠️ No citation keys found! Check your Markdown files.")

    return citation_keys

def filter_bib_file(bib_file, citation_keys, output_file):
    """Create a new .bib file containing only the cited references."""
    with open(bib_file, "r", encoding="utf-8") as f:
        bib_entries = re.split(r"\n(?=@)", f.read())

    filtered_entries = []
    for entry in bib_entries:
        match = re.search(r"@\w+\s*\{\s*([\w\-_:.]+)\s*,", entry)
        if match:
            key = match.group(1).strip()
            if key in citation_keys:
                filtered_entries.append(entry.strip())  # Add "@" back

    if not filtered_entries:
        print("⚠️ No matching BibTeX entries found! Your .bib file may not have these citations.")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(filtered_entries) + "\n")

    print(f"✅ Filtered .bib file saved as: {output_file}")

if __name__ == "__main__":
    print("🔍 Extracting citation keys from Markdown files...")
    citation_keys = extract_citation_keys(MARKDOWN_DIR)
    # print(f"📌 Found {len(citation_keys)} unique citation keys: {citation_keys}")

    print("📖 Filtering the .bib file...")
    filter_bib_file(BIB_FILE, citation_keys, FILTERED_BIB_FILE)

    print("🎉 Done! Your new `references_filtered.bib` file is ready.")
