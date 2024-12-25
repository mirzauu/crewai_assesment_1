import requests
import json
import os
import re
from bs4 import BeautifulSoup

from langchain.tools import tool
from langchain_community.document_loaders import WebBaseLoader

class SearchTools:
  
  @tool('search internet')
  def search_internet(query: str,limit: int = 5) -> str:
    """
    Use this tool to search the internet for information. This tools returns 5 results from Google search engine.
    """
    return SearchTools.search(query,limit)
  
  @tool('search instagram')
  def search_instagram(query: str) -> str:
    """
    Use this tool to search Instagram. This tools returns 5 results from Instagram pages.
    """
    return SearchTools.search(f"site:instagram.com {query}", limit=5)
  
  @tool('analyze competitors')
  def analyze_competitors(url: str) -> str:
      """
      Analyze the marketing strategy of a competitor based on their website.
      """
      try:
          loader = WebBaseLoader(url)
          documents = loader.load()
          return f"Analysis of {url}:\n\n" + "\n".join([doc.page_content for doc in documents])
      except Exception as e:
          return f"Error: Unable to analyze competitor. Reason: {str(e)}"
  
 

    
  @tool('open page')
  def open_page(url: str) -> str:
    """
    Use this tool to open a webpage and get the content.
    """
    try:
        loader = WebBaseLoader(url)
        documents = loader.load()
        return "\n".join([doc.page_content for doc in documents])
    except Exception as e:
        return f"Error: Unable to load the webpage content. Reason: {str(e)}"

  def search(query, limit=5):

    url = "https://google.serper.dev/search"
    payload = json.dumps({
      "q": query,
      "num": limit,
    })
    headers = {
      'X-API-KEY': os.getenv("SERPER_API_KEY"),
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()['organic']
    
    string = []
    for result in results:
      string.append(f"{result['title']}\n{result['snippet']}\n{result['link']}\n\n")
      
    return f"Search results for '{query}':\n\n" + "\n".join(string)
  
  
if __name__ == "__main__":
  print(SearchTools.open_page("https://www.python.org/"))



@tool('generate hashtags')
def generate_hashtags(keywords: str) -> str:
    """
    Generate popular hashtags for Instagram based on given keywords.
    """
    try:
        hashtags = [f"#{word}" for word in keywords.split() if len(word) > 2]
        return " ".join(hashtags[:10])  # Return the top 10 hashtags
    except Exception as e:
        return f"Error: Unable to generate hashtags. Reason: {str(e)}"



@tool('scrape targeted emails')
def scrape_targeted_emails(query: str, limit: int = 5) -> str:
    """
    Scrape email addresses based on a given query. The tool searches Google for relevant pages
    and extracts email addresses from those pages.
    
    Parameters:
    - query: A search term to find relevant pages (e.g., "fashion blogs contact emails").
    - limit: The number of pages to scrape for emails.

    Returns:
    - A list of extracted email addresses or an error message.
    """
    try:
        # Search the internet for relevant pages
        search_results = SearchTools.search(query, limit)
        
        emails = set()  # To avoid duplicate email addresses
        for result in search_results:
            url = result['link']  # Extract the link from the search result
            
            # Fetch the webpage content
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Parse the page content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                page_text = soup.get_text()
                
                # Extract email addresses using regex
                found_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_text)
                emails.update(found_emails)  # Add found emails to the set
        
        # Return the list of unique emails
        if emails:
            return f"Extracted Emails:\n" + "\n".join(emails)
        else:
            return "No emails found on the scraped pages."

    except Exception as e:
        return f"Error: Unable to scrape emails. Reason: {str(e)}"