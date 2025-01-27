from langchain.tools import BaseTool
import requests
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

class SitemapProcessorTool(BaseTool):
    name = "Sitemap Processor"
    description = "Processes website sitemaps and extracts relevant content"

    def __init__(self):
        super().__init__()
        self.processed_urls = set()

    def _run(self, sitemap_url: str) -> str:
        """Process sitemap and return relevant content"""
        try:
            # Fetch and parse sitemap
            response = requests.get(sitemap_url)
            root = ET.fromstring(response.content)

            # Extract URLs from sitemap
            urls = []
            for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                urls.append(url.text)

            # Process each URL
            content = []
            for url in urls[:5]:  # Limit to 5 URLs for demonstration
                if url not in self.processed_urls:
                    page_content = self._fetch_page_content(url)
                    content.append(f"From {url}: {page_content[:500]}...")
                    self.processed_urls.add(url)

            return "\n\n".join(content) if content else "No content found in sitemap."
        except Exception as e:
            return f"Error processing sitemap: {str(e)}"

    def _fetch_page_content(self, url: str) -> str:
        """Fetch and extract content from a webpage"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            return soup.get_text()
        except Exception as e:
            return f"Error fetching page: {str(e)}"

    def _arun(self, sitemap_url: str) -> str:
        """Async implementation of run"""
        # Implement if needed
        raise NotImplementedError("Async not implemented") 