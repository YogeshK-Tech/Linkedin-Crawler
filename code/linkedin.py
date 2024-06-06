import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

def build_search_url(keywords, base_url="https://www.google.com/search", query_prefix="site:linkedin.com/in/"):
    encoded_keywords = [urllib.parse.quote(f'"{keyword}"') for keyword in keywords]
    query = f"{query_prefix}+({' + '.join(encoded_keywords)})"
    return f"{base_url}?q={query}"

def fetch_linkedin_profiles(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        linkedin_url_pattern = re.compile(r'https://www\.linkedin\.com/in/[\w-]+')
        linkedin_profiles = []
        for link in links:
            match = linkedin_url_pattern.search(link['href'])
            if match:
                profile_url = match.group(0)  # Extract the matched URL
                linkedin_profiles.append(profile_url)
        return linkedin_profiles
    else:
        return []

def save_profiles_to_file(profiles, file_name='linkedin_profiles.txt'):
    with open(file_name, 'w') as file:
        for profile in profiles:
            file.write(profile + '\n')

if __name__ == "__main__":
    keywords = ["Chief Product Officer", "United States", "Insurance"]  # Add your keywords here
    url = build_search_url(keywords)
    print(url)
    linkedin_profiles = fetch_linkedin_profiles(url)
    if linkedin_profiles:
        save_profiles_to_file(linkedin_profiles)
        print(f'Found {len(linkedin_profiles)} LinkedIn profiles. Check linkedin_profiles.txt for the URLs.')
    else:
        print('No LinkedIn profiles found.')
