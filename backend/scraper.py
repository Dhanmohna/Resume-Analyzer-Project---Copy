import requests
from bs4 import BeautifulSoup

def scrape_jobs(role):
    query = role.replace(" ", "+")
    
    url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&txtKeywords={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    job_listings = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")

    for job in job_listings[:10]:
        title_tag = job.find("h2")
        company_tag = job.find("h3")
        desc_tag = job.find("ul", class_="list-job-dtl")

        title = title_tag.text.strip() if title_tag else "N/A"
        company = company_tag.text.strip() if company_tag else "N/A"
        description = desc_tag.text.strip() if desc_tag else "N/A"

        link = title_tag.a["href"] if title_tag and title_tag.a else "#"

        jobs.append({
            "title": title,
            "company": company,
            "description": description,
            "url": link
        })

        

    return jobs