
from serpapi import GoogleSearch


class WebResourceFetcher:
    def __init__(self, api_keys):
        self.api_keys = [k.strip() for k in api_keys if k and k.strip()]
        self.current_key_index = 0

    def _get_current_key(self):
        if not self.api_keys:
            return None
        return self.api_keys[self.current_key_index]

    def _rotate_key(self):
        if self.api_keys:
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            print(f"(!) Switching to API Key index: {self.current_key_index}")

    def fetch_links(self, query, num_results=5):
        key = self._get_current_key()
        attempt_count = 0
        max_attempts = max(1, len(self.api_keys))
        educational_query = f"{query} tutorial concept explanation"

        while attempt_count < max_attempts and key:
            try:
                params = {
                    "engine": "google",
                    "q": educational_query,
                    "api_key": key,
                    "num": num_results
                }
                search = GoogleSearch(params)
                results = search.get_dict()

                if "error" in results:
                    raise Exception(results["error"])

                links = []
                if "organic_results" in results:
                    for item in results["organic_results"]:
                        raw_link = item.get("link", "")
                        title = item.get("title", "")
                        snippet = item.get("snippet", "")
                        links.append({
                            "title": title,
                            "link": raw_link,
                            "snippet": snippet
                        })
                if links:
                    return links

            except Exception as e:
                print(f"Error with key #{self.current_key_index}: {e}")
                self._rotate_key()
                key = self._get_current_key()
                attempt_count += 1

        # Curated fallbacks
        return [
            {
                "title": f"Wikipedia: {query.title()}",
                "link": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
                "snippet": f"Encyclopedia article and concepts covering {query}."
            },
            {
                "title": f"GeeksforGeeks Guide: {query.title()}",
                "link": f"https://www.google.com/search?q=site%3Ageeksforgeeks.org+{query}",
                "snippet": f"Tutorials and technical deep dive into {query}."
            },
            {
                "title": f"Scholar Search: {query.title()}",
                "link": f"https://scholar.google.com/scholar?q={query}",
                "snippet": f"Academic papers and research literature on {query}."
            }
        ]

    def fetch_youtube_videos(self, query, max_results=3):
        key = self._get_current_key()
        if not key:
            return []
        try:
            params = {
                "engine": "youtube",
                "search_query": f"{query} tutorial",
                "api_key": key
            }
            search = GoogleSearch(params)
            res = search.get_dict()
            video_list = []
            if "video_results" in res:
                for item in res["video_results"][:max_results]:
                    video_list.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "channel": item.get("channel", {}).get("name", "YouTube"),
                        "thumbnail": item.get("thumbnail", {}).get("static", "")
                    })
            return video_list
        except Exception as e:
            print(f"YouTube search warning: {e}")
            return []

if __name__ == "__main__":
    pass
