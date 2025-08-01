import re
from data_loader import get_company_files, parse_xml
def find_best_year_match(data, target_year):
    if not data:
        return None
    if target_year:
        # Match exact year
        for year in data:
            if target_year in year:
                return year
    # fallback to latest available
    return sorted(data.keys(), reverse=True)[0]


def answer_question(question):
    question = question.lower().strip("?.,!")
    
    # Enhanced company detection
    companies = {
        'apple': ['aapl', 'apple'],
        'microsoft': ['msft', 'microsoft'],
        'tesla': ['tsla', 'tesla']
    }
    
    detected_company = None
    for word in re.split(r'\W+', question):
        for company, keywords in companies.items():
            if any(keyword == word for keyword in keywords):
                detected_company = company
                break
        if detected_company:
            break
    
    if not detected_company:
        return "Please specify: Apple, Microsoft, or Tesla"
    
    # Improved year and quarter detection
    year = None
    quarter = None
    for word in re.split(r'\W+', question):
        if word.isdigit():
            if len(word) == 4 and word.startswith('20'):
                year = word
            elif len(word) == 1 or len(word) == 2:
                quarter = word.zfill(2)
    
    # Expanded metrics with synonyms
    metrics = {
        "revenue": ["revenue", "sales", "total revenue"],
    "net income": ["net income", "profit", "earnings"],
    "assets": ["assets", "total assets"],
    "liabilities": ["liabilities", "total liabilities", "current liabilities"],
    "operating income": ["operating income", "income from operations"],
    "cash": ["cash", "cash and cash equivalents"],
    "eps": ["eps", "earnings per share"],
    "r&d": ["r&d", "research", "research and development"],
    "equity": ["equity", "shareholder equity"],
    "gross profit": ["gross profit"],
    "operating expenses": ["operating expenses", "opex"]
    }
    
    detected_metric = None
    for metric, keywords in metrics.items():
        if any(keyword in question for keyword in keywords):
            detected_metric = metric
            break
    
    if not detected_metric:
        available = [m.replace('_', ' ') for m in metrics.keys()]
        return f"Available metrics: {', '.join(available)}"
    
    # Get matching files
    files = get_company_files(detected_company)
    if not files:
        return f"No data files found for {detected_company}"
    
    

    # Find best matching file
    target_file = None
    if year:
        if quarter:
            target_file = next(
                (f for f in files 
                 if f['year'] == year and f['quarter'] == quarter),
                None
            )
        if not target_file:
            target_file = next(
                (f for f in files if f['year'] == year),
                files[0]
            )
    else:
        target_file = files[0]
    
    if not target_file:
        available_years = list(set(f['year'] for f in files))
        return f"No data for requested period. Available years: {', '.join(available_years)}"
    
    # Parse and return data
    financials = parse_xml(target_file['path'])
    if not financials:
        return "Could not parse financial data"
    
    value = financials.get(detected_metric)
    if not value:
        return f"No {detected_metric.replace('_', ' ')} data available"
    
    # Format response
    try:
        if detected_metric == 'eps':
            formatted_value = "${:,.2f}".format(float(value))
        else:
            formatted_value = "${:,.0f}".format(float(value))
    except ValueError:
        formatted_value = value
    
    period = target_file['year']
    if target_file['quarter']:
        period += f" Q{target_file['quarter']}"
    
    return f"{detected_company.title()} {detected_metric.replace('_', ' ')} ({period}): {formatted_value}"