#!/usr/bin/env python3
"""
Publication Metadata to Jekyll Markdown Converter

Fetches publication metadata from DOI or PubMed ID and generates
a Jekyll markdown file for lab websites.

Usage:
    python pubmed_to_jekyll.py --doi 10.1038/s41467-025-59244-w
    python pubmed_to_jekyll.py --pmid 40533454
    python pubmed_to_jekyll.py --doi 10.1038/s41467-025-59244-w --output custom_name.md
"""

import argparse
import requests
import sys
import re
from datetime import datetime
from pathlib import Path


class PublicationFetcher:
    """Fetch and format publication metadata from various sources."""
    
    def __init__(self):
        self.crossref_api = "https://api.crossref.org/works/"
        self.datacite_api = "https://api.datacite.org/dois/"
        self.pubmed_api = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        
    def fetch_from_doi(self, doi):
        """Fetch metadata from CrossRef or DataCite using DOI."""
        # Clean DOI
        doi = doi.replace("https://doi.org/", "").replace("http://dx.doi.org/", "")
        
        metadata = None
        
        # Try CrossRef first
        try:
            response = requests.get(f"{self.crossref_api}{doi}")
            response.raise_for_status()
            data = response.json()
            print("Found in CrossRef")
            metadata = self._parse_crossref(data['message'], doi)
        except requests.exceptions.RequestException as e:
            print(f"Not found in CrossRef, trying DataCite...")
        
        # Try DataCite as fallback
        if not metadata:
            try:
                response = requests.get(f"{self.datacite_api}{doi}")
                response.raise_for_status()
                data = response.json()
                print("Found in DataCite")
                metadata = self._parse_datacite(data['data'], doi)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching from DataCite: {e}", file=sys.stderr)
                return None
        
        # If we got metadata but no PMID, try to find it
        if metadata and not metadata.get('pmid'):
            print("Searching PubMed for PMID...")
            pmid, abstract = self.search_pmid_by_doi(doi)
            if pmid:
                print(f"Found PMID: {pmid}")
                metadata['pmid'] = pmid
                if abstract:
                    print("Found abstract")
                    metadata['abstract'] = abstract
            else:
                print("No PMID found in PubMed")
        
        return metadata
    
    def search_pmid_by_doi(self, doi):
        """Search PubMed for PMID using DOI, and fetch abstract if found."""
        try:
            search_url = f"{self.pubmed_api}esearch.fcgi"
            params = {
                'db': 'pubmed',
                'term': f'{doi}[DOI]',
                'retmode': 'json'
            }
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Check if we got any results
            id_list = data.get('esearchresult', {}).get('idlist', [])
            if id_list:
                pmid = id_list[0]
                
                # Fetch full record to get abstract
                fetch_url = f"{self.pubmed_api}efetch.fcgi"
                fetch_params = {
                    'db': 'pubmed',
                    'id': pmid,
                    'rettype': 'xml',
                    'retmode': 'xml'
                }
                fetch_response = requests.get(fetch_url, params=fetch_params)
                fetch_response.raise_for_status()
                
                # Extract abstract from XML
                abstract = self._extract_abstract_from_xml(fetch_response.text)
                
                return pmid, abstract
            return None, None
        except requests.exceptions.RequestException as e:
            print(f"Could not search PubMed for PMID: {e}", file=sys.stderr)
            return None, None
    
    def _extract_abstract_from_xml(self, xml_text):
        """Extract abstract from PubMed XML."""
        # Look for AbstractText tags
        abstract_parts = []
        
        # Handle both simple abstracts and structured abstracts
        abstract_pattern = r'<AbstractText[^>]*>(.*?)</AbstractText>'
        matches = re.finditer(abstract_pattern, xml_text, re.DOTALL)
        
        for match in matches:
            text = match.group(1)
            # Remove any HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            # Decode HTML entities
            text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            abstract_parts.append(text.strip())
        
        if abstract_parts:
            return ' '.join(abstract_parts)
        
        return None
    
    def fetch_from_pmid(self, pmid):
        """Fetch metadata from PubMed using PMID."""
        try:
            # Fetch PubMed data
            fetch_url = f"{self.pubmed_api}efetch.fcgi"
            params = {
                'db': 'pubmed',
                'id': pmid,
                'rettype': 'xml',
                'retmode': 'xml'
            }
            response = requests.get(fetch_url, params=params)
            response.raise_for_status()
            
            # Parse XML (basic parsing - for production, use xml.etree or lxml)
            return self._parse_pubmed_xml(response.text, pmid)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching PMID: {e}", file=sys.stderr)
            return None
    
    def _parse_crossref(self, data, doi):
        """Parse CrossRef JSON response."""
        # Extract authors
        authors = []
        if 'author' in data:
            for author in data['author']:
                given = author.get('given', '')
                family = author.get('family', '')
                if given and family:
                    # Use initials for given names
                    initials = ''.join([n[0].upper() for n in given.split()])
                    authors.append(f"{family} {initials}")
                elif family:
                    authors.append(family)
        
        # Extract year
        year = None
        if 'published-print' in data:
            year = data['published-print']['date-parts'][0][0]
        elif 'published-online' in data:
            year = data['published-online']['date-parts'][0][0]
        elif 'created' in data:
            year = data['created']['date-parts'][0][0]
        
        # Extract journal info
        journal = data.get('container-title', [''])[0] if data.get('container-title') else ''
        short_journal_list = data.get('short-container-title', [])
        short_journal = short_journal_list[0] if short_journal_list else journal
        
        # Volume and issue
        volume = data.get('volume', '')
        issue = data.get('issue', '')
        page = data.get('page', '')
        
        # Build journal citation string
        journal_cite = short_journal
        if volume:
            journal_cite += f" {volume}"
            if issue:
                journal_cite += f"({issue})"
        if page:
            journal_cite += f", {page}"
        
        # Extract title
        title_list = data.get('title', [])
        title = title_list[0] if title_list else ''
        
        return {
            'title': title,
            'authors': authors,
            'year': year,
            'journal': journal_cite,
            'doi': f"https://doi.org/{doi}",
            'pmid': None,  # Not available from CrossRef
            'abstract': None,  # Will be fetched from PubMed if available
        }
    
    def _parse_datacite(self, data, doi):
        """Parse DataCite JSON response."""
        attributes = data.get('attributes', {})
        
        # Extract authors
        authors = []
        creators = attributes.get('creators', [])
        for creator in creators:
            # DataCite can have name or givenName/familyName
            if 'familyName' in creator:
                family = creator.get('familyName', '')
                given = creator.get('givenName', '')
                if given and family:
                    # Use initials for given names
                    initials = ''.join([n[0].upper() for n in given.split()])
                    authors.append(f"{family} {initials}")
                elif family:
                    authors.append(family)
            elif 'name' in creator:
                # Try to parse "LastName, FirstName" format
                name = creator['name']
                if ',' in name:
                    parts = name.split(',', 1)
                    family = parts[0].strip()
                    given = parts[1].strip()
                    initials = ''.join([n[0].upper() for n in given.split()])
                    authors.append(f"{family} {initials}")
                else:
                    authors.append(name)
        
        # Extract year
        year = None
        publication_year = attributes.get('publicationYear')
        if publication_year:
            year = int(publication_year)
        else:
            # Try to parse from dates
            dates = attributes.get('dates', [])
            for date in dates:
                if date.get('dateType') == 'Issued':
                    date_str = date.get('date', '')
                    if date_str:
                        year = int(date_str[:4])
                        break
        
        # Extract title
        titles = attributes.get('titles', [])
        title = titles[0].get('title', '') if titles else ''
        
        # Extract journal/publisher info
        # DataCite uses "container" for journal info
        container = attributes.get('container', {})
        journal = container.get('title', '')
        
        # If no container, use publisher
        if not journal:
            journal = attributes.get('publisher', '')
        
        # Volume, issue, pages from container
        volume = container.get('volume', '')
        issue = container.get('issue', '')
        first_page = container.get('firstPage', '')
        last_page = container.get('lastPage', '')
        
        # Build journal citation string
        journal_cite = journal
        if volume:
            journal_cite += f" {volume}"
            if issue:
                journal_cite += f"({issue})"
        if first_page:
            if last_page and last_page != first_page:
                journal_cite += f", {first_page}-{last_page}"
            else:
                journal_cite += f", {first_page}"
        
        # Try to get related identifiers (like PMID)
        pmid = None
        related_identifiers = attributes.get('relatedIdentifiers', [])
        for identifier in related_identifiers:
            if identifier.get('relatedIdentifierType') == 'PMID':
                pmid = identifier.get('relatedIdentifier')
                break
        
        return {
            'title': title,
            'authors': authors,
            'year': year,
            'journal': journal_cite,
            'doi': f"https://doi.org/{doi}",
            'pmid': pmid,
            'abstract': None,  # Will be fetched from PubMed if available
        }
    
    def _parse_pubmed_xml(self, xml_text, pmid):
        """Parse PubMed XML response (basic implementation)."""
        # This is a simplified parser. For production, use xml.etree.ElementTree
        
        # Extract title
        title_match = re.search(r'<ArticleTitle>(.*?)</ArticleTitle>', xml_text, re.DOTALL)
        title = title_match.group(1) if title_match else ''
        title = re.sub(r'<[^>]+>', '', title)  # Remove any HTML tags
        
        # Extract authors
        authors = []
        author_pattern = r'<Author[^>]*>.*?<LastName>(.*?)</LastName>.*?<Initials>(.*?)</Initials>.*?</Author>'
        for match in re.finditer(author_pattern, xml_text, re.DOTALL):
            lastname, initials = match.groups()
            authors.append(f"{lastname} {initials}")
        
        # Extract year
        year_match = re.search(r'<PubDate>.*?<Year>(\d{4})</Year>', xml_text, re.DOTALL)
        year = int(year_match.group(1)) if year_match else None
        
        # Extract journal
        journal_match = re.search(r'<ISOAbbreviation>(.*?)</ISOAbbreviation>', xml_text)
        if not journal_match:
            journal_match = re.search(r'<Title>(.*?)</Title>', xml_text)
        journal = journal_match.group(1) if journal_match else ''
        
        # Extract volume, issue, pages
        volume_match = re.search(r'<Volume>(.*?)</Volume>', xml_text)
        volume = volume_match.group(1) if volume_match else ''
        
        issue_match = re.search(r'<Issue>(.*?)</Issue>', xml_text)
        issue = issue_match.group(1) if issue_match else ''
        
        pages_match = re.search(r'<MedlinePgn>(.*?)</MedlinePgn>', xml_text)
        pages = pages_match.group(1) if pages_match else ''
        
        # Build journal citation
        journal_cite = journal
        if volume:
            journal_cite += f" {volume}"
            if issue:
                journal_cite += f"({issue})"
        if pages:
            journal_cite += f", {pages}"
        
        # Extract DOI
        doi_match = re.search(r'<ArticleId IdType="doi">(.*?)</ArticleId>', xml_text)
        doi = f"https://doi.org/{doi_match.group(1)}" if doi_match else None
        
        # Extract abstract
        abstract = self._extract_abstract_from_xml(xml_text)
        
        return {
            'title': title,
            'authors': authors,
            'year': year,
            'journal': journal_cite,
            'doi': doi,
            'pmid': pmid,
            'abstract': abstract,
        }


class JekyllMarkdownGenerator:
    """Generate Jekyll markdown files from publication metadata."""
    
    def format_authors(self, authors):
        """Format author list with Font Awesome annotations for first and last authors."""
        if not authors:
            return ""
        
        formatted = []
        for i, author in enumerate(authors):
            if i == 0:  # First author
                formatted.append(f"{author} <sup><i class=\"small fa fa-asterisk\"></i></sup>")
            elif i == len(authors) - 1:  # Last author
                formatted.append(f"{author} <sup><i class=\"small fa fa-envelope\"></i></sup>")
            else:
                formatted.append(author)
        
        return ", ".join(formatted) + "."
    
    def generate_ref_string(self, authors, year):
        """Generate reference string (FirstAuthor et al. Year, Journal)."""
        if not authors:
            return ""
        
        first_author = authors[0].split()[0]  # Get last name
        ref = f"{first_author}"
        
        if len(authors) > 1:
            ref += " et al."
        
        if year:
            ref += f" {year}"
        
        return ref
    
    def generate_filename(self, authors, year):
        """Generate filename from first author and year."""
        if not authors or not year:
            return f"paper-{datetime.now().strftime('%Y%m%d')}.md"
        
        first_author = authors[0].split()[0].lower()  # Get last name, lowercase
        return f"{first_author}-{year}.md"
    
    def generate_markdown(self, metadata, output_file=None):
        """Generate Jekyll markdown file from metadata."""
        
        # Format authors
        authors_formatted = self.format_authors(metadata['authors'])
        
        # Generate reference string
        ref = self.generate_ref_string(metadata['authors'], metadata['year'])
        
        # Determine output filename
        if not output_file:
            output_file = self.generate_filename(metadata['authors'], metadata['year'])
        
        # Build YAML frontmatter
        yaml_lines = [
            "---",
            "layout: paper",
            f"title: {metadata['title']}",
            "image: /images/papers/",  # To be filled manually
            f"authors: {authors_formatted}",
            f"year: {metadata['year'] or ''}",
            f"ref: {ref}",
            f"journal: \"{metadata['journal']}\"",
            "pdf: /pdfs/papers/",  # To be filled manually
            "supplement: ",  # To be filled manually
            "preprint: ",  # To be filled manually
        ]
        
        # Add DOI if available
        if metadata.get('doi'):
            yaml_lines.append(f"doi: {metadata['doi']}")
        else:
            yaml_lines.append("doi: ")
        
        # Add PMID if available
        if metadata.get('pmid'):
            yaml_lines.append(f"pmid: {metadata['pmid']}")
        else:
            yaml_lines.append("pmid: ")
        
        yaml_lines.extend([
            "github: ",  # To be filled manually
            "category: ",  # To be filled manually
            "---",
            "### Abstract ###",
            "",
        ])
        
        # Add abstract if available
        if metadata.get('abstract'):
            yaml_lines.append(metadata['abstract'])
        else:
            yaml_lines.append("<!-- Add abstract here -->")
        
        yaml_lines.append("")
        
        markdown_content = "\n".join(yaml_lines)
        
        # Write to file
        output_path = Path(output_file)
        output_path.write_text(markdown_content)
        
        print(f"Generated: {output_file}")
        return output_file


def main():
    parser = argparse.ArgumentParser(
        description='Fetch publication metadata and generate Jekyll markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --doi 10.1038/s41467-025-59244-w
  %(prog)s --pmid 40533454
  %(prog)s --doi 10.1038/s41467-025-59244-w --output custom.md
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--doi', help='DOI of the publication')
    group.add_argument('--pmid', help='PubMed ID of the publication')
    
    parser.add_argument('--output', '-o', help='Output filename (auto-generated if not specified)')
    
    args = parser.parse_args()
    
    # Fetch metadata
    fetcher = PublicationFetcher()
    
    if args.doi:
        print(f"Fetching metadata for DOI: {args.doi}")
        metadata = fetcher.fetch_from_doi(args.doi)
    else:
        print(f"Fetching metadata for PMID: {args.pmid}")
        metadata = fetcher.fetch_from_pmid(args.pmid)
    
    if not metadata:
        print("Failed to fetch metadata", file=sys.stderr)
        sys.exit(1)
    
    # Generate markdown
    generator = JekyllMarkdownGenerator()
    generator.generate_markdown(metadata, args.output)
    
    print("\nNote: Please fill in the following fields manually:")
    print("  - image")
    print("  - pdf")
    print("  - supplement (if applicable)")
    print("  - preprint (if applicable)")
    print("  - github (if applicable)")
    print("  - category")
    print("  - abstract")


if __name__ == "__main__":
    main()
