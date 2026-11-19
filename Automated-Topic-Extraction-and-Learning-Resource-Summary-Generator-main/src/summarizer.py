import re

import requests
import wikipedia
from bs4 import BeautifulSoup
from newspaper import Article


class ContentSummarizer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

    def _extract_text_heuristic(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        # Remove scripts, styles, nav, headers, footers
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form', 'noscript']):
            tag.decompose()

        # Find paragraphs
        paras = [p.get_text().strip() for p in soup.find_all('p') if len(p.get_text().strip()) > 40]
        if paras:
            joined = " ".join(paras[:8])
            # Return roughly 3-5 sentences
            sentences = re.split(r'(?<=[.!?])\s+', joined)
            return " ".join(sentences[:5])
        return ""

    def get_wiki_summary(self, topic):
        """Fetch a reliable encyclopedic summary directly from Wikipedia as a companion/fallback."""
        try:
            results = wikipedia.search(topic, results=1)
            if results:
                page_title = results[0]
                summary = wikipedia.summary(page_title, sentences=4, auto_suggest=False)
                return {
                    "title": f"Wikipedia: {page_title}",
                    "summary": summary,
                    "url": f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}",
                    "status": "success"
                }
        except Exception as e:
            print(f"Wikipedia lookup fallback failed for '{topic}': {e}")
        return None

    def get_summary(self, url, fallback_topic=None, snippet=""):
        try:
            print(f"Summarizing: {url}")
            # Step 1: Attempt standard request with real browser headers
            resp = requests.get(url, headers=self.headers, timeout=8)
            title = ""
            summary = ""

            if resp.status_code == 200:
                html_text = resp.text
                try:
                    article = Article(url)
                    article.download(input_html=html_text)
                    article.parse()
                    article.nlp()
                    title = article.title
                    summary = article.summary
                except Exception as inner_e:
                    print(f"Newspaper parse warning: {inner_e}")

                if not summary or len(summary.strip()) < 50:
                    summary = self._extract_text_heuristic(html_text)
                if not title:
                    soup = BeautifulSoup(html_text, 'html.parser')
                    title = soup.title.string.strip() if soup.title and soup.title.string else "Article Resource"

            if summary and len(summary.strip()) >= 50:
                return {
                    "title": title or "Web Resource",
                    "summary": summary,
                    "status": "success"
                }

        except Exception as e:
            print(f"Direct web fetch failed for {url}: {e}")

        # Step 2: Intelligent Fallback
        # If web scraping was blocked (403, Cloudflare) or empty, use snippet or Wikipedia
        if fallback_topic:
            wiki_res = self.get_wiki_summary(fallback_topic)
            if wiki_res:
                combined_summary = wiki_res['summary']
                if snippet:
                    combined_summary = f"**Web Excerpt:** {snippet}\n\n**Educational Overview ({wiki_res['title']}):**\n{wiki_res['summary']}"
                return {
                    "title": wiki_res["title"],
                    "summary": combined_summary,
                    "status": "success"
                }

        if snippet:
            return {
                "title": "Web Excerpt",
                "summary": f"{snippet}\n\n*(Note: Full article blocked external scraping, but search preview excerpt was recovered above.)*",
                "status": "success"
            }

        return {
            "title": "Access Restricted",
            "summary": "This site prevents automated scraping (HTTP 403 / anti-bot). You can click the direct link to read it on the publisher's website.",
            "status": "failed"
        }

if __name__ == "__main__":
    summarizer = ContentSummarizer()
    res = summarizer.get_wiki_summary("resource extraction")
    print(res)
