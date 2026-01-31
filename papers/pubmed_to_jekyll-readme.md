# Publication Metadata to Jekyll Markdown Converter

A Python script to fetch publication metadata from DOI or PubMed ID and generate Jekyll markdown files for lab websites.

## Features

- ✅ Fetch metadata from DOI (via CrossRef API)
- ✅ Fetch metadata from DOI (via DataCite API as fallback)
- ✅ Automatic PMID lookup when using DOI (searches PubMed)
- ✅ Automatic abstract extraction from PubMed
- ✅ Fetch metadata from PubMed ID (via NCBI E-utilities)
- ✅ Auto-format author lists with Font Awesome icons for first/last authors
- ✅ Generate Jekyll-compatible YAML frontmatter
- ✅ Auto-generate filenames based on first author and year

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Make script executable (optional)
chmod +x pubmed_to_jekyll.py
```

## Usage

### Basic Usage

Fetch by DOI:
```bash
python pubmed_to_jekyll.py --doi 10.1038/s41467-025-59244-w
```

Fetch by PubMed ID:
```bash
python pubmed_to_jekyll.py --pmid 40533454
```

### Specify Output Filename

```bash
python pubmed_to_jekyll.py --doi 10.1038/s41467-025-59244-w --output snyder-2025.md
```

### Command Line Options

```
--doi DOI           DOI of the publication
--pmid PMID         PubMed ID of the publication
--output, -o FILE   Output filename (auto-generated if not specified)
```

## Output Format

The script generates a Jekyll markdown file with the following structure:

```markdown
---
layout: paper
title: Your Paper Title
image: /images/papers/
authors: LastName1 AB <sup><i class="small fa fa-asterisk"></i></sup>, LastName2 CD, LastName3 EF <sup><i class="small fa fa-envelope"></i></sup>.
year: 2025
ref: LastName1 et al. 2025
journal: "Journal Name Vol(Issue), Pages"
pdf: /pdfs/papers/
supplement: 
preprint: 
doi: https://doi.org/10.xxxx/xxxxx
pmid: 12345678
github: 
category: 
---
### Abstract ###

<!-- Add abstract here -->
```

### Author Annotations

- **First author**: Gets `<sup><i class="small fa fa-asterisk"></i></sup>` (asterisk icon)
- **Last author**: Gets `<sup><i class="small fa fa-envelope"></i></sup>` (envelope icon)

## Manual Fields

After generating the markdown file, you'll need to manually fill in:

- `image`: Path to the paper's figure/image
- `pdf`: Path to the PDF file
- `supplement`: Path to supplementary materials (if applicable)
- `preprint`: DOI or link to preprint version (if applicable)
- `github`: GitHub repository link (if applicable)
- `category`: Paper category (e.g., "selected-papers")

Note: The abstract is automatically extracted from PubMed when available. If not found, you'll need to add it manually.

## Example

Input:
```bash
python pubmed_to_jekyll.py --doi 10.1038/s41467-025-59244-w
```

Console output:
```
Fetching metadata for DOI: 10.1038/s41467-025-59244-w
Found in CrossRef
Searching PubMed for PMID...
Found PMID: 40533454
Found abstract
Generated: snyder-2025.md
```

Output file: `snyder-2025.md`

```markdown
---
layout: paper
title: Divergence in a eukaryotic transcription factor's co-TF dependence involves multiple intrinsically disordered regions
image: /images/papers/
authors: Snyder LF <sup><i class="small fa fa-asterisk"></i></sup>, O'Brien EM, Zhao J, Liang J, Bruce BJ, Zhang Y, Zhu W, Cassier TH, Schnicker NJ, Zhou X, Gordan R, He BZ <sup><i class="small fa fa-envelope"></i></sup>.
year: 2025
ref: Snyder et al. 2025
journal: "Nat Commun 16, 5340"
pdf: /pdfs/papers/
supplement: 
preprint: 
doi: https://doi.org/10.1038/s41467-025-59244-w
pmid: 40533454
github: 
category: 
---
### Abstract ###

<!-- Add abstract here -->
```

## API Information

### DOI Resolution Strategy
The script automatically tries multiple sources when given a DOI:
1. **CrossRef API** (most journal articles)
2. **DataCite API** (fallback - used by some publishers, repositories, and preprint servers)
3. **PubMed Search** (automatic lookup of PMID using the DOI)
4. **PubMed Fetch** (retrieves full record including abstract)

When you provide a DOI, the script will:
- First fetch metadata from CrossRef or DataCite
- Then automatically search PubMed using the DOI to find the corresponding PMID
- If a PMID is found, fetch the full PubMed record to extract the abstract
- If a PMID/abstract is found, it's added to the output; otherwise fields are left blank

### CrossRef API
- No API key required
- Free for academic use
- Rate limits apply (50 requests/second)

### DataCite API
- No API key required
- Free for academic use
- Used by publishers like microPublication Biology, institutional repositories, and data repositories

### PubMed E-utilities
- No API key required for basic usage
- Recommended to use API key for higher rate limits
- To add API key: Include `&api_key=YOUR_KEY` in the URL

## Troubleshooting

**Issue**: DOI not found in CrossRef
- The script will automatically try DataCite as a fallback
- Publishers like microPublication Biology use DataCite instead of CrossRef
- If both fail, verify the DOI is correct or try using the PubMed ID instead

**Issue**: Missing metadata
- Some fields may not be available from the API
- CrossRef doesn't provide PubMed IDs
- PubMed XML parsing is basic and may miss some fields

**Issue**: Incorrect author formatting
- Check if authors have middle names vs. initials
- The script uses initials from the API data

## Python vs Ruby

While Jekyll is written in Ruby, Python is preferred for this task because:

1. **Better API Libraries**: `requests` is excellent for HTTP APIs
2. **Scientific Computing**: Python is standard in scientific workflows
3. **Easier Parsing**: Better XML/JSON libraries available
4. **Community**: More examples and resources for PubMed/CrossRef APIs
5. **Integration**: Easy to integrate with other scientific Python tools

This is a standalone script that generates static files, so it doesn't need to integrate with Jekyll's Ruby runtime.

## Future Enhancements

Possible improvements:
- Add support for bioRxiv/medRxiv preprints
- Automatic abstract fetching and formatting
- Support for batch processing multiple publications
- Better XML parsing using `lxml` or `xml.etree.ElementTree`
- Fetch citation counts
- Integration with ORCID for author disambiguation

## License

This script is provided as-is for academic use.
