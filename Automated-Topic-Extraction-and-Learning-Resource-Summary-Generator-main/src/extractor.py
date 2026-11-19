import os
import re

import pandas as pd
from keybert import KeyBERT
from rake_nltk import Rake


class TopicExtractor:
    def __init__(self, domain_keywords_path=None):
        print("Loading KeyBERT model...")
        self.kw_model = KeyBERT(model="all-MiniLM-L6-v2")
        self.rake = Rake()
        self.domain_keywords = set()

        # Filter out common presentation / academic paper metadata noise
        self.ignored_words = {
            "slide", "slides", "chapter", "presentation", "author", "authors",
            "university", "department", "lecture", "overview", "introduction",
            "conclusion", "summary", "thank", "thanks", "questions", "agenda",
            "outline", "page", "figure", "table", "et al", "content", "contents",
            "section", "journal", "proceeding", "proceedings", "conference",
            "international", "vol", "doi", "issn", "isbn", "abstract", "paper",
            "research", "review", "system", "systems", "approach", "proposed",
            "method", "result", "results", "technique", "techniques", "based"
        }

        if domain_keywords_path and os.path.exists(domain_keywords_path):
            try:
                df = pd.read_csv(domain_keywords_path)
                col = 'keyword' if 'keyword' in df.columns else df.columns[0]
                self.domain_keywords = set(df[col].dropna().str.lower().tolist())
            except Exception as e:
                print(f"Warning: Could not load domain keywords: {e}")

    def _is_meaningful_topic(self, topic):
        t = topic.lower().strip()
        # Must be between 5 and 35 characters
        if len(t) < 5 or len(t) > 35:
            return False
        # No pure numbers or junk
        if re.search(r'\d{3,}', t) or re.search(r'[^\w\s-]', t):
            return False
        words = t.split()
        # Prefer 2-3 word conceptual phrases
        if len(words) < 2 or len(words) > 3:
            return False
        # Do not allow if words are purely metadata words
        if any(w in self.ignored_words for w in words):
            return False
        return True

    def extract_with_keybert(self, text, top_n=8):
        try:
            # Use candidate keywords of 2-3 grams with diversity
            keywords = self.kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=(2, 3),
                stop_words='english',
                use_mmr=True,
                diversity=0.7,
                top_n=top_n * 3
            )
            clean_list = []
            seen = set()
            for kw, score in keywords:
                kw_clean = kw.strip().title()
                if self._is_meaningful_topic(kw) and kw_clean.lower() not in seen:
                    clean_list.append((kw_clean, round(score, 2)))
                    seen.add(kw_clean.lower())
                if len(clean_list) >= top_n:
                    break
            return clean_list
        except Exception as e:
            print(f"KeyBERT extraction note: {e}")
            return []

    def hybrid_extraction(self, text, top_n=8):
        if not text or len(text.strip()) < 30:
            return []

        # High-quality KeyBERT extraction
        topics = self.extract_with_keybert(text, top_n=top_n)

        # Fallback to domain keywords if available in document
        text_lower = text.lower()
        extracted_names = {t[0].lower() for t in topics}

        for domain_kw in self.domain_keywords:
            if domain_kw in text_lower and domain_kw not in extracted_names:
                topics.append((domain_kw.title(), 0.95))

        # Sort by score descending
        topics = sorted(topics, key=lambda x: x[1], reverse=True)
        return topics[:top_n]

if __name__ == "__main__":
    extractor = TopicExtractor()
