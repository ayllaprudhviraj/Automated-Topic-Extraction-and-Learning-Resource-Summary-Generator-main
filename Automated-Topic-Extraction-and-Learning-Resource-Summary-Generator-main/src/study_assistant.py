import os
import re

from groq import Groq


class StudyAssistant:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
        self.client = None
        if self.groq_api_key:
            try:
                self.client = Groq(api_key=self.groq_api_key)
                print("Connected to Groq LLM API (openai/gpt-oss-120b).")
            except Exception as e:
                print(f"Groq initialization warning: {e}")

    def generate_quiz_and_flashcards(self, topic, summary_text):
        if not summary_text or len(summary_text.strip()) < 30:
            return [], []

        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', summary_text) if len(s.strip()) > 25]
        flashcards = []
        quiz_items = []

        flashcards.append({
            "term": topic.title(),
            "definition": sentences[0] if sentences else f"Core subject in the uploaded lecture regarding {topic}."
        })

        for i, sent in enumerate(sentences[1:4]):
            words = sent.split()
            if len(words) > 5:
                flashcards.append({
                    "term": f"Key Aspect #{i+1} ({topic.title()})",
                    "definition": sent
                })

        quiz_items.append({
            "question": f"What is the primary role or definition of '{topic.title()}' based on this material?",
            "answer": sentences[0] if sentences else f"It represents a key mechanism in {topic}."
        })

        if len(sentences) > 1:
            quiz_items.append({
                "question": f"How is '{topic.title()}' structured or applied in practice?",
                "answer": sentences[1]
            })

        if len(sentences) > 2:
            quiz_items.append({
                "question": f"What key principles or methods are connected to '{topic.title()}'?",
                "answer": sentences[2]
            })

        return flashcards, quiz_items

    def answer_question_about_doc(self, question, document_text, current_topic="", current_summary=""):
        if not question or not question.strip():
            return "Please type a question about your lecture notes."

        # Real-time Groq LLM Generation
        if self.client:
            try:
                prompt_context = f"""You are an expert academic tutor and teaching assistant.
Answer the student's question accurately using their uploaded lecture content and topic summary below.

LECTURE DOCUMENT (First 4000 characters):
{document_text[:4000] if document_text else "No raw text available."}

ACTIVE TOPIC: {current_topic}
VERIFIED TOPIC SUMMARY: {current_summary[:1500] if current_summary else "N/A"}

STUDENT QUESTION: {question}

Provide a well-structured, clear explanation with bullet points if helpful:"""

                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful, clear academic tutor answering questions about lecture notes."},
                        {"role": "user", "content": prompt_context}
                    ],
                    model="openai/gpt-oss-120b",
                    temperature=0.3,
                    max_tokens=600
                )
                return chat_completion.choices[0].message.content

            except Exception as e:
                print(f"Groq API call warning: {e}. Falling back to internal semantic extractor.")

        # Fallback Semantic Extractor
        q_clean = question.lower().strip()
        paragraphs = [p.strip() for p in document_text.split('\n') if len(p.strip()) > 35]
        if not paragraphs:
            paragraphs = [s.strip() for s in re.split(r'(?<=[.!?])\s+', document_text) if len(s.strip()) > 25]

        q_words = set(re.findall(r'\w+', q_clean))
        common = {'what', 'is', 'how', 'why', 'the', 'and', 'are', 'for', 'about', 'in', 'of', 'to', 'can', 'you'}
        keywords = q_words - common

        matches = []
        for p in paragraphs:
            p_words = set(re.findall(r'\w+', p.lower()))
            overlap = len(keywords & p_words)
            if overlap > 0:
                matches.append((overlap, p))

        matches.sort(key=lambda x: x[0], reverse=True)

        if matches:
            top_excerpts = [m[1] for m in matches[:3]]
            response = "### 💡 Answer from your Lecture Notes:\n\n"
            for idx, text in enumerate(top_excerpts, 1):
                response += f"**Point {idx}:** {text}\n\n"
            if current_summary:
                response += f"---\n*Curated Concept Context ({current_topic}):*\n{current_summary[:280]}..."
            return response
        else:
            if current_summary:
                return (
                    f"### 💡 Concept Overview:\n"
                    f"While that exact phrasing wasn't matched in the raw slides, here is the verified background for **{current_topic}**:\n\n"
                    f"{current_summary}"
                )
            return "I couldn't locate a direct match in the document text. Try asking about one of the extracted topics."

if __name__ == "__main__":
    pass
