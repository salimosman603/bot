import requests
from urllib.parse import urlparse

def parse_ads_txt(domain: str) -> list:
    """
    Parses a domain's ads.txt file to extract authorized ad networks
    Returns list of tuples: (advertiser_domain, publisher_id, relationship_type, certification_id)
    """
    try:
        # Normalize domain
        if not domain.startswith('http'):
            domain = 'https://' + domain
            
        parsed = urlparse(domain)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        ads_txt_url = f"{base_url}/ads.txt"
        
        response = requests.get(ads_txt_url, timeout=10)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        records = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) < 3:
                continue
                
            advertiser_domain = parts[0]
            publisher_id = parts[1]
            relationship_type = parts[2]
            certification_id = parts[3] if len(parts) >= 4 else None
            
            records.append((advertiser_domain, publisher_id, relationship_type, certification_id))
            
        return records
    except Exception as e:
        print(f"Error parsing ads.txt: {str(e)}")
        return []