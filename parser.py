import os
import re
import xml.etree.ElementTree as ET

def get_company_files(company):
    """Find all files for a company"""
    company = company.lower()
    files = []
    
    # Company to filename mapping
    company_files = {
        'apple': ['aapl'],
        'microsoft': ['msft'],
        'tesla': ['tsla']
    }
    
    # Check all XML files in data directory
    for filename in os.listdir('data'):
        if not filename.lower().endswith('.xml'):
            continue
            
        # Check if file belongs to requested company
        filename_lower = filename.lower()
        for pattern in company_files.get(company, []):
            if pattern in filename_lower:
                # Extract year from filename
                year_match = re.search(r'(20\d{2})', filename)
                if year_match:
                    files.append({
                        'path': os.path.join('data', filename),
                        'year': year_match.group(1)
                    })
                break
    
    return sorted(files, key=lambda x: x['year'], reverse=True)

def parse_xml(filepath):
    """Parse XML financial data"""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Remove namespaces
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        
        # Find financial data
        financials = {}
        tags = {
            'revenue': ['Revenues', 'Revenue', 'rev'],
            'net_income': ['NetIncomeLoss', 'NetIncome', 'profit'],
            'assets': ['Assets', 'TotalAssets']
        }
        
        for key, possible_tags in tags.items():
            for tag in possible_tags:
                elem = root.find(f'.//{tag}')
                if elem is not None and elem.text:
                    financials[key] = elem.text.strip()
                    break
        
        return financials
        
    except Exception as e:
        print(f"Error parsing {filepath}: {str(e)}")
        return {}