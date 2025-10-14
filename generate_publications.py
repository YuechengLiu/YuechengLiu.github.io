#!/usr/bin/env python3
"""
Script to generate publication markdown files from citations.csv
"""

import csv
import os
import re
from datetime import datetime

def clean_authors(authors_str):
    """Clean up authors string and convert from 'Last, First' to 'First Last' format"""
    # Remove trailing commas and spaces
    authors_str = authors_str.strip().rstrip(',').strip()
    
    # Split by semicolon to get individual authors
    authors = [a.strip() for a in authors_str.split(';') if a.strip()]
    
    # Convert each author from "Last, First" to "First Last"
    converted_authors = []
    for author in authors:
        if ',' in author:
            parts = author.split(',', 1)
            last_name = parts[0].strip()
            first_name = parts[1].strip() if len(parts) > 1 else ''
            converted_authors.append(f"{first_name} {last_name}".strip())
        else:
            converted_authors.append(author)
    
    return '; '.join(converted_authors)

def get_author_position(authors_str, target_name="Liu, Yuecheng"):
    """Get the position of the target author in the author list (1-indexed)"""
    authors = [a.strip() for a in authors_str.split(';') if a.strip()]
    for i, author in enumerate(authors):
        if target_name in author or "Yuecheng Liu" in author:
            return i + 1  # Return 1-indexed position
    return 999  # If not found, put at the end

def generate_slug(title):
    """Generate a URL-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:50]  # Limit length

def format_citation(authors, title, venue, year, volume="", number="", pages="", publisher=""):
    """Format citation in APA-like style"""
    # Highlight Yuecheng Liu in the authors list (now in "First Last" format)
    authors_highlighted = authors.replace("Yuecheng Liu", "<b>Yuecheng Liu</b>")
    
    citation = f'{authors_highlighted} ({year}). &quot;{title}.&quot;'
    
    if venue:
        citation += f' <i>{venue}</i>'
        if volume:
            citation += f', {volume}'
            if number:
                citation += f'({number})'
        if pages:
            citation += f', {pages}'
    
    if publisher:
        citation += f'. {publisher}'
    
    citation += '.'
    return citation

def main():
    csv_file = 'citations.csv'
    output_dir = '_publications'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read CSV file
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        publications = list(reader)
    
    # Debug: print column names
    if publications:
        print(f"CSV Columns: {list(publications[0].keys())}")
        print(f"Total publications: {len(publications)}\n")
    
    # Sort by year (newest first), then by author position (first author first)
    publications.sort(key=lambda x: (-int(x['Year']), get_author_position(x['Authors'])))
    
    # Track publications per year for numbering
    year_counts = {}
    
    # Assign dates for proper sorting (latest publications get later dates in the year)
    for i, pub in enumerate(publications):
        year = pub['Year']
        title = pub['Title'].strip()
        authors = clean_authors(pub['Authors'])
        venue = pub['Publication'].strip()
        volume = pub['Volume'].strip()
        number = pub['Number'].strip()
        pages = pub['Pages'].strip()
        publisher = pub['Publisher'].strip()
        
        # Count publications per year
        if year not in year_counts:
            year_counts[year] = 0
        year_counts[year] += 1
        
        # Generate filename
        slug = generate_slug(title)
        filename = f"{year}-paper-{year_counts[year]:02d}-{slug}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Determine category (conference or journal based on venue name)
        venue_lower = venue.lower()
        if any(keyword in venue_lower for keyword in ['conference', 'proceedings', 'workshop']):
            category = 'conferences'
        elif any(keyword in venue_lower for keyword in ['journal', 'transactions']):
            category = 'manuscripts'
        elif 'arxiv' in venue_lower or 'preprint' in venue_lower:
            category = 'preprints'
        else:
            category = 'conferences'  # Default
        
        # Format citation
        citation = format_citation(authors, title, venue, year, volume, number, pages, publisher)
        
        # Create a date that ensures proper sorting
        # Within each year, use month/day to reflect the order in the sorted list
        # Since we want first-author papers to appear first (on top) when displayed in reverse chronological order,
        # we assign later dates to papers that should appear first
        # i=0 should get the latest date in that year, i=1 should get an earlier date, etc.
        month = 12 - (i % 12)  # Distribute across months, starting from December
        day = 28 - (i % 28)  # Days within month (1-28 to avoid invalid dates)
        if month < 1:
            month = 1
        if day < 1:
            day = 1
        pub_date = f"{year}-{month:02d}-{day:02d}"
        
        # Create markdown content
        content = f"""---
title: "{title}"
collection: publications
category: {category}
permalink: /publication/{year}-{slug}
excerpt: ''
date: {pub_date}
venue: '{venue}'
citation: '{citation}'
---

{citation}
"""
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created: {filename}")
    
    print(f"\nTotal publications generated: {len(publications)}")
    print(f"Years covered: {min(year_counts.keys())} - {max(year_counts.keys())}")

if __name__ == '__main__':
    main()
