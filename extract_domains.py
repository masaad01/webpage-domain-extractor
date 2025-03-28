import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_domains_from_html(content, output_file):
    """Extract domains from HTML content and write them to a file."""
    soup = BeautifulSoup(content, 'html.parser')

    # Set to store unique domains
    domains = set()

    # Regex pattern to extract valid domains
    domain_pattern = re.compile(r'https?://([A-Za-z0-9.-]+)')

    # Find all anchor tags with href attributes and extract domains
    for link in soup.find_all('a', href=True):
        href = link['href']
        match = domain_pattern.match(href)
        if match:
            domains.add(match.group(1))

    # Write the domains to the output file
    with open(output_file, 'w') as file:
        for domain in domains:
            file.write(f"{domain}\n")

    print(f"Domains have been saved to {output_file}")

def extract_domains(input_source, output_file):
    """Auto-detect whether input_source is a URL or an HTML file and process accordingly."""
    if is_valid_url(input_source):
        print(f"Processing URL: {input_source}")
        # Process as URL
        response = requests.get(input_source)
        if response.status_code == 200:
            extract_domains_from_html(response.text, output_file)
        else:
            print(f"Failed to retrieve the webpage: {input_source}")
    elif os.path.isfile(input_source):
        print(f"Processing HTML file: {input_source}")
        # Process as HTML file
        with open(input_source, 'r', encoding='utf-8') as file:
            content = file.read()
        extract_domains_from_html(content, output_file)
    else:
        print(f"Invalid input source: {input_source}. Please provide a valid URL or HTML file.")

def is_valid_url(url):
    """Check if a given string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])  # Check if the URL has a scheme (http/https) and a netloc (domain)
    except ValueError:
        return False

# Example usage:
input_source = 'https://example.com'  # Replace with the URL or HTML file path
output_file = 'test2.txt'  # Replace with desired output file
extract_domains(input_source, output_file)
