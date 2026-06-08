import requests

def scrape_remoteok(role: str):
    """
    Scrapes live remote jobs using RemoteOK's official open JSON endpoint feed.
    """
    jobs = []
    url = "https://remoteok.com/api"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"RemoteOK API block or error: Status {response.status_code}")
            return []
            
        data = response.json()
        
        # The first item in RemoteOK's API response is a legal/info string container, skip it
        raw_listings = data[1:] if len(data) > 1 else []
        
        target_keyword = role.lower().strip()
        
        for item in raw_listings:
            position = item.get("position", "")
            tags = [t.lower() for t in item.get("tags", [])]
            
            # Match via title string or embedded metadata array tags
            if target_keyword in position.lower() or any(target_keyword in tag for tag in tags):
                # Clean up dirty HTML markup blocks native to RemoteOK API descriptions
                raw_desc = item.get("description", "")
                clean_desc = "".join(BeautifulSoup(raw_desc, "html.parser").findAll(text=True)) if raw_desc else ""
                clean_desc = " ".join(clean_desc.split())
                
                jobs.append({
                    "title": position.strip(),
                    "company": item.get("company", "Remote Tech Org").strip(),
                    "description": clean_desc if clean_desc else f"Remote opening for a expert {role}.",
                    "url": item.get("url", "https://remoteok.com")
                })
                
                if len(jobs) >= 5: # Limit processing queue sizes
                    break
                    
    except Exception as e:
        print(f"Error executing real-time RemoteOK API network call: {e}")
        
    return jobs