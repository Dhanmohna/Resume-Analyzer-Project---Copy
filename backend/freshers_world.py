import requests
from bs4 import BeautifulSoup

def scrape_freshersworld(role: str):
    """
    Directly scrapes live technical listings inside India from Freshersworld.
    """
    jobs = []
    # Format role query parameter
    search_query = role.lower().replace(" ", "-")
    url = f"https://www.freshersworld.com/jobs/jobsearch/{search_query}-jobs"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        # Target the core main job listing block elements
        job_cards = soup.find_all('div', class_='job-container')
        
        for card in job_cards[:3]:  # Capture the top 3 dynamic items
            title_el = card.find('span', class_='wrap-title')
            company_el = card.find('div', class_='company-name')
            desc_el = card.find('span', class_='desc')
            link_el = card.find('a', href=True)
            
            title = title_el.text.strip() if title_el else f"Professional {role}"
            company = company_el.text.strip() if company_el else "Indian Tech Partner"
            description = desc_el.text.strip() if desc_el else f"Hiring for {role} roles across locations in India."
            job_url = link_el['href'] if link_el else "https://www.freshersworld.com"
            
            jobs.append({
                "title": title,
                "company": company,
                "description": " ".join(description.split()),
                "url": job_url
            })
    except Exception as e:
        print(f"Error reading freshersworld feed: {e}")
        
    return jobs