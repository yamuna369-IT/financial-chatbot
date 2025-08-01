import os
import re
import xml.etree.ElementTree as ET

def get_company_files(company):
    """Find all XML files for a company with improved year extraction"""
    company = company.lower()
    files = []
    
    company_patterns = {
        'apple': ['aapl'],
        'microsoft': ['msft'],
        'tesla': ['tsla']
    }
    
    for filename in os.listdir('data'):
        if not filename.lower().endswith('.xml'):
            continue
            
        filename_lower = filename.lower()
        for pattern in company_patterns.get(company, []):
            if pattern in filename_lower:
                # Improved year extraction (handles YYYYMMDD and YYYY formats)
                year_match = re.search(r'(20\d{2})(?:\d{4})?(?:_|$)', filename)
                if year_match:
                    files.append({
                        'path': os.path.join('data', filename),
                        'year': year_match.group(1),
                        'quarter': filename.split('-')[1][4:6] if '-' in filename else None
                    })
                break
    
    return sorted(files, key=lambda x: x['year'], reverse=True)

def parse_xml(filepath):
    """Enhanced XML parser with more financial metrics"""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Remove namespaces
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        
        # Expanded financial metrics
        metrics = {
            'revenue': ['Revenues', 'Revenue', 'SalesRevenueNet'],
            'net_income': ['NetIncomeLoss', 'NetIncome', 'ProfitLoss'],
            'assets': ['Assets', 'TotalAssets'],
            'liabilities': ['Liabilities', 'TotalLiabilities'],
            'operating_income': ['OperatingIncomeLoss'],
            'cash': ['CashAndCashEquivalentsAtCarryingValue'],
            'eps': ['EarningsPerShareBasic', 'EarningsPerShareDiluted'],
            'r&d': ['ResearchAndDevelopmentExpense']
        }
        
        results = {}
        for metric, tags in metrics.items():
            for tag in tags:
                elem = root.find(f'.//{tag}')
                if elem is not None and elem.text and elem.text.strip():
                    results[metric] = elem.text.strip()
                    break
        
        return results
        
    except Exception as e:
        print(f"Error parsing {filepath}: {str(e)}")
        return {}