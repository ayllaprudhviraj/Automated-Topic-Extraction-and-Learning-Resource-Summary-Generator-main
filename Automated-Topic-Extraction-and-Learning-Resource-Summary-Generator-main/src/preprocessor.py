import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.python_keywords = {
            "def", "import", "from", "return", "class", "try", "except",
            "if", "else", "elif", "for", "while", "print", "none", "true", "false"
        }

    def remove_noise(self, text):
        text = re.sub(r'(?i)^\s*(page|chapter|unit)\s*\d+.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'\S+@\S+', '', text)
        return text

    def remove_code_snippets(self, text):
        lines = text.split('\n')
        cleaned_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith(('import ', 'from ', 'def ', 'class ')):
                continue
            if stripped in self.python_keywords:
                continue
            cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    def normalize_elongated_words(self, text):
        pattern = re.compile(r"(.)\1{2,}")
        return pattern.sub(r"\1\1", text)

    def clean_and_process(self, text):
        text = text.lower()
        text = self.remove_noise(text)
        text = self.remove_code_snippets(text)
        text = self.normalize_elongated_words(text)

        tokens = word_tokenize(text)

        processed_tokens = [
            self.lemmatizer.lemmatize(word)
            for word in tokens
            if word.isalpha()
            and word not in self.stop_words
            and word not in self.python_keywords
            and len(word) > 2
        ]

        return " ".join(processed_tokens)

if __name__ == "__main__":
    processor = TextPreprocessor()

    sample_text = """
    Page 12
    Chapter 3: Introduction to ML
    import pandas as pd
    The modellll is trained using backpropagation.
    def train_model():
    It is very goooood for accuraccy.
    """

    clean_text = processor.clean_and_process(sample_text)
    print(clean_text)
