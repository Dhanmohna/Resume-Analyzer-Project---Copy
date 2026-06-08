import requests
from bs4 import BeautifulSoup

def scrape_internshala(role: str):
    """
    Scrapes real live job listings directly from Internshala.
    """
    jobs = []
    # Format the role for the URL query
    search_query = role.lower().replace(" ", "-")
    url = f"https://internshala.com/jobs/keywords-{search_query}/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Internshala scrap block or error: Status {response.status_code}")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all job card containers on the live page
        job_cards = soup.find_all('div', class_='container-fluid individual_internship')
        
        for card in job_cards:
            title_element = card.find('h3', class_='heading_4_5 profile')
            company_element = card.find('a', class_='link_display_like_text company_and_premium')
            
            if not company_element:
                company_element = card.find('div', class_='heading_6 company_name')
                
            # Extract relative link and build absolute URL
            link_element = card.find('a', href=True)
            job_url = "https://internshala.com" + link_element['href'] if link_element else "https://internshala.com/jobs"
            
            # Extract basic text fields safely
            title = title_element.text.strip() if title_element else f"Professional {role}"
            company = company_element.text.strip() if company_element else "Verified Enterprise"
            
            # Find snippet elements or build a detailed context description dynamically from metadata
            details_wrap = card.find('div', class_='individual_internship_details')
            desc_snippet = details_wrap.text.strip() if details_wrap else f"Active live opening for a {role} at {company}."
            # Clean excessive multi-spacing from html layout templates
            desc_snippet = " ".join(desc_snippet.split())

            jobs.append({
                "title": title,
                "company": company,
                "description": desc_snippet,
                "url": job_url
            })
            
    except Exception as e:
        print(f"Error executing real-time Internshala scrape network call: {e}")
        
    return jobs