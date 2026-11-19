import os
import tempfile
from dotenv import load_dotenv
import gradio as gr

from src.extractor import TopicExtractor
from src.file_loader import load_file
from src.preprocessor import TextPreprocessor
from src.study_assistant import StudyAssistant
from src.summarizer import ContentSummarizer
from src.web_fetcher import WebResourceFetcher

load_dotenv()

serp_key = os.getenv("SERPAPI_API_KEY", "").strip()
API_KEYS = [serp_key] if serp_key else ["677e23d7f857350e19d6628d09c2f7e56650487d45c51f804060b630810d4dbe"]
DOMAIN_KEYWORDS_PATH = "data/domain_keywords.csv"

print("Initializing AI Lecture Engine & Study Hub...")
preprocessor = TextPreprocessor()
extractor = TopicExtractor(domain_keywords_path=DOMAIN_KEYWORDS_PATH)
fetcher = WebResourceFetcher(api_keys=API_KEYS)
summarizer = ContentSummarizer()
assistant = StudyAssistant()

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Global Smooth Background & Typography */
body, .gradio-container {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    background: radial-gradient(circle at 15% 15%, #131b2e 0%, #0a0d14 100%) !important;
    max-width: 1300px !important;
    margin: 0 auto !important;
    color: #e2e8f0 !important;
}

/* Header Glassmorphism */
.header-banner {
    text-align: center;
    padding: 24px 20px;
    background: rgba(30, 41, 59, 0.45);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 16px;
    margin-bottom: 22px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.header-banner:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 35px -8px rgba(56, 189, 248, 0.15);
}
.header-banner h1 {
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}
.header-banner p {
    font-size: 14.5px;
    color: #94a3b8;
    margin: 0;
}

/* Interactive Card Panels */
.card-panel {
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.4);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.card-panel:hover {
    border-color: rgba(56, 189, 248, 0.25);
    box-shadow: 0 12px 30px -5px rgba(0, 0, 0, 0.6);
}

/* Animated Interactive Tag Chips */
.tag-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}
.tag-chip {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.8) 100%);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 12.5px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    animation: fadeInTag 0.4s ease-out forwards;
    transition: all 0.25s ease;
    cursor: default;
}
.tag-chip:hover {
    background: #0284c7;
    color: #ffffff;
    border-color: #38bdf8;
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
}

@keyframes fadeInTag {
    from {
        opacity: 0;
        transform: translateY(6px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Video Card Hover Effects */
.video-card {
    display: flex;
    align-items: center;
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
}
.video-card:hover {
    transform: translateX(4px);
    border-color: rgba(239, 68, 68, 0.4);
    box-shadow: 0 6px 18px rgba(239, 68, 68, 0.15);
    background: rgba(30, 41, 59, 0.7);
}
.video-card img {
    width: 108px;
    height: 64px;
    object-fit: cover;
    border-radius: 8px;
    margin-right: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.video-card a {
    color: #60a5fa;
    text-decoration: none;
    font-weight: 600;
    font-size: 14.5px;
    transition: color 0.2s ease;
}
.video-card a:hover {
    color: #93c5fd;
    text-decoration: underline;
}

/* Flashcards & Active Recall Cards */
.flashcard {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.7) 0%, rgba(30, 41, 59, 0.5) 100%);
    border-left: 4px solid #38bdf8;
    border-top: 1px solid rgba(255,255,255,0.05);
    border-right: 1px solid rgba(255,255,255,0.05);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding: 14px 18px;
    margin-bottom: 12px;
    border-radius: 0 12px 12px 0;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.flashcard:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
}
.flashcard h4 {
    margin: 0 0 6px 0;
    color: #38bdf8;
    font-size: 15px;
    font-weight: 700;
}
.flashcard p {
    margin: 0;
    color: #cbd5e1;
    font-size: 14px;
    line-height: 1.5;
}

/* Tab Bar Refinements */
.tab-nav {
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}
.tab-nav button {
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
}
.tab-nav button.selected {
    color: #38bdf8 !important;
    border-bottom: 2px solid #38bdf8 !important;
}

/* Buttons Glow */
.primary-btn {
    background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3) !important;
}
.primary-btn:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(37, 99, 235, 0.45) !important;
}
"""

def render_videos_html(videos):
    if not videos:
        return "<p style='color: #94a3b8; padding: 12px;'>No video tutorials found for this topic.</p>"
    html = "<div style='margin-top: 6px;'>"
    for v in videos:
        thumb = v.get('thumbnail') or 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=100'
        title = v.get('title', 'Video Tutorial')
        link = v.get('link', '#')
        channel = v.get('channel', 'YouTube')
        html += f"""
        <div class='video-card'>
            <img src='{thumb}' alt='thumb' />
            <div>
                <a href='{link}' target='_blank'>▶ {title}</a>
                <div style='color: #94a3b8; font-size: 12px; margin-top: 5px;'>Channel: <span style='color: #cbd5e1;'>{channel}</span></div>
            </div>
        </div>
        """
    html += "</div>"
    return html

def render_flashcards_html(flashcards, quiz_items):
    html = ""
    if flashcards:
        html += "<h4 style='color: #38bdf8; margin: 10px 0 10px 0; font-weight: 700;'>🗂️ Active Recall Flashcards</h4>"
        for fc in flashcards:
            html += f"""
            <div class='flashcard'>
                <h4>🏷️ {fc['term']}</h4>
                <p>{fc['definition']}</p>
            </div>
            """
    if quiz_items:
        html += "<h4 style='color: #c084fc; margin: 20px 0 10px 0; font-weight: 700;'>❓ Self-Test Quiz Questions</h4>"
        for i, q in enumerate(quiz_items, 1):
            html += f"""
            <div class='flashcard' style='border-left-color: #a855f7;'>
                <h4 style='color: #c084fc;'>Question {i}: {q['question']}</h4>
                <details style='margin-top: 6px; color: #94a3b8; font-size: 13.5px;'>
                    <summary style='cursor: pointer; color: #c084fc; font-weight: 600;'>🔍 Show Answer</summary>
                    <p style='margin-top: 8px; color: #e2e8f0; background: rgba(0,0,0,0.25); padding: 8px 12px; border-radius: 6px;'>{q['answer']}</p>
                </details>
            </div>
            """
    return html or "<p style='color: #94a3b8; padding: 12px;'>No flashcards available for this section.</p>"

def process_upload_event(file_obj, top_k):
    if file_obj is None:
        return (
            "Please upload a lecture file (.pdf or .pptx) above.",
            gr.update(choices=[], value=None),
            "",
            gr.update(choices=[], value=None),
            "",
            "",
            "",
            "<p style='color: #94a3b8;'>Upload notes to see recommended video tutorials.</p>",
            "<p style='color: #94a3b8;'>Flashcards and active-recall test questions will appear here.</p>",
            {},
            "",
            [],
            ""
        )

    try:
        raw_text = load_file(file_obj.name)
        if not raw_text or len(raw_text.strip()) == 0:
            return (
                "Could not extract readable text from this file.",
                gr.update(choices=[], value=None),
                "",
                gr.update(choices=[], value=None),
                "",
                "",
                "",
                "<p style='color: #94a3b8;'>No videos available.</p>",
                "<p style='color: #94a3b8;'>No flashcards available.</p>",
                {},
                "",
                [],
                ""
            )

        clean_text = preprocessor.clean_and_process(raw_text)
        topics_data = extractor.hybrid_extraction(clean_text, top_n=int(top_k))
        topic_names = [t[0] for t in topics_data]

        if not topic_names:
            return (
                "No distinct topics identified in this file.",
                gr.update(choices=[], value=None),
                "",
                gr.update(choices=[], value=None),
                "",
                "",
                "",
                "<p style='color: #94a3b8;'>No videos available.</p>",
                "<p style='color: #94a3b8;'>No flashcards available.</p>",
                {},
                "",
                [],
                ""
            )

        fname = os.path.basename(file_obj.name)
        words_count = len(raw_text.split())
        status_msg = f"✨ Ready! Extracted {len(topic_names)} key concepts from '{fname}' ({words_count:,} words)."

        tags_html = "<div class='tag-container'>" + "".join(
            [f"<span class='tag-chip'>🏷️ {t}</span>" for t in topic_names]
        ) + "</div>"

        # Pre-fetch resources for top topic
        top_topic = topic_names[0]
        links_data = fetcher.fetch_links(top_topic, num_results=5)
        link_choices = []
        meta_store = {}

        for item in links_data:
            title = item.get('title', 'Resource')
            link = item.get('link', '')
            clean_title = (title[:55] + '...') if len(title) > 55 else title
            link_choices.append((clean_title, link))
            meta_store[link] = item

        first_link = link_choices[0][1] if link_choices else None

        summary_title = ""
        summary_text = ""
        source_html = ""

        if first_link:
            meta = meta_store.get(first_link, {})
            res = summarizer.get_summary(first_link, fallback_topic=top_topic, snippet=meta.get("snippet", ""))
            summary_title = res.get('title', 'Learning Resource')
            summary_text = res.get('summary', '')
            source_html = f"<div style='margin-top: 10px;'><a href='{first_link}' target='_blank' style='display: inline-block; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; padding: 7px 16px; border-radius: 8px; text-decoration: none; font-size: 13.5px; font-weight: 600; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);'>🌐 Open Original Article ↗</a></div>"

        videos = fetcher.fetch_youtube_videos(top_topic, max_results=3)
        video_html = render_videos_html(videos)

        flashcards, quiz_items = assistant.generate_quiz_and_flashcards(top_topic, summary_text)
        study_cards_html = render_flashcards_html(flashcards, quiz_items)

        return (
            status_msg,
            gr.update(choices=topic_names, value=top_topic),
            tags_html,
            gr.update(choices=link_choices, value=first_link),
            summary_title,
            summary_text,
            source_html,
            video_html,
            study_cards_html,
            meta_store,
            raw_text,
            topic_names,
            fname
        )

    except Exception as e:
        print(f"Process upload error: {e}")
        return (
            f"Error processing file: {str(e)}",
            gr.update(choices=[], value=None),
            "",
            gr.update(choices=[], value=None),
            "",
            "",
            "",
            "<p style='color: #94a3b8;'>Error loading videos.</p>",
            "<p style='color: #94a3b8;'>Error generating flashcards.</p>",
            {},
            "",
            [],
            ""
        )

def topic_changed_event(topic, meta_store, all_topics, doc_name):
    if not topic:
        return (
            gr.update(choices=[], value=None),
            "",
            "",
            "",
            "",
            "",
            {}
        )

    links_data = fetcher.fetch_links(topic, num_results=5)
    link_choices = []
    new_meta_store = dict(meta_store) if isinstance(meta_store, dict) else {}

    for item in links_data:
        title = item.get('title', 'Resource')
        link = item.get('link', '')
        clean_title = (title[:55] + '...') if len(title) > 55 else title
        link_choices.append((clean_title, link))
        new_meta_store[link] = item

    first_link = link_choices[0][1] if link_choices else None

    summary_title = ""
    summary_text = ""
    source_html = ""

    if first_link:
        meta = new_meta_store.get(first_link, {})
        res = summarizer.get_summary(first_link, fallback_topic=topic, snippet=meta.get("snippet", ""))
        summary_title = res.get('title', 'Learning Resource')
        summary_text = res.get('summary', '')
        source_html = f"<div style='margin-top: 10px;'><a href='{first_link}' target='_blank' style='display: inline-block; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; padding: 7px 16px; border-radius: 8px; text-decoration: none; font-size: 13.5px; font-weight: 600; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);'>🌐 Open Original Article ↗</a></div>"

    videos = fetcher.fetch_youtube_videos(topic, max_results=3)
    video_html = render_videos_html(videos)

    flashcards, quiz_items = assistant.generate_quiz_and_flashcards(topic, summary_text)
    study_cards_html = render_flashcards_html(flashcards, quiz_items)

    return (
        gr.update(choices=link_choices, value=first_link),
        summary_title,
        summary_text,
        source_html,
        video_html,
        study_cards_html,
        new_meta_store
    )

def link_changed_event(url, meta_store, topic, all_topics, doc_name):
    if not url:
        return "", "", "", ""

    meta = meta_store.get(url, {}) if isinstance(meta_store, dict) else {}
    snippet = meta.get("snippet", "")

    res = summarizer.get_summary(url, fallback_topic=topic, snippet=snippet)
    title = res.get('title', 'Learning Resource')
    summary_text = res.get('summary', '')
    source_html = f"<div style='margin-top: 10px;'><a href='{url}' target='_blank' style='display: inline-block; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; padding: 7px 16px; border-radius: 8px; text-decoration: none; font-size: 13.5px; font-weight: 600; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);'>🌐 Open Original Article ↗</a></div>"

    flashcards, quiz_items = assistant.generate_quiz_and_flashcards(topic or "Study Concept", summary_text)
    study_cards_html = render_flashcards_html(flashcards, quiz_items)

    return title, summary_text, source_html, study_cards_html

def submit_question(user_question, chat_history_list, raw_doc, current_topic, current_summary):
    if not user_question or not user_question.strip():
        return "", chat_history_list
    
    current_list = list(chat_history_list) if isinstance(chat_history_list, list) else []
    bot_answer = assistant.answer_question_about_doc(
        user_question,
        raw_doc or "",
        current_topic or "",
        current_summary or ""
    )
    current_list.append({"role": "user", "content": user_question})
    current_list.append({"role": "assistant", "content": bot_answer})
    return "", current_list

with gr.Blocks(title="AI Lecture Assistant") as demo:
    resource_meta_state = gr.State({})
    raw_document_state = gr.State("")
    all_topics_state = gr.State([])
    doc_name_state = gr.State("")

    with gr.Column(elem_classes=["header-banner"]):
        gr.Markdown(
            """
            # 📚 Next-Level AI Lecture Assistant & Study Hub
            Transform slides and notes into structured topics, verified reading summaries, YouTube tutorials, and active-recall quizzes.
            """
        )

    with gr.Row():
        # LEFT COLUMN: Input & Topic Navigator
        with gr.Column(scale=1, elem_classes=["card-panel"]):
            gr.Markdown("### 📂 1. Document Upload")
            file_input = gr.File(
                label="Lecture Slide / Note (.pdf or .pptx)",
                file_types=[".pdf", ".pptx"],
                type="filepath"
            )
            top_k_slider = gr.Slider(
                minimum=4,
                maximum=12,
                value=8,
                step=1,
                label="Topics to Extract"
            )
            status_box = gr.Textbox(
                label="System Status",
                value="Upload a file to begin.",
                interactive=False,
                lines=1
            )

            gr.Markdown("### 🎯 2. Extracted Topics")
            topic_tags_display = gr.HTML()

            topic_dropdown = gr.Dropdown(
                label="Select Topic to Explore",
                choices=[],
                allow_custom_value=True,
                interactive=True
            )

            link_dropdown = gr.Dropdown(
                label="Curated Learning Sources",
                choices=[],
                allow_custom_value=True,
                interactive=True
            )

        # RIGHT COLUMN: Multi-Tab Study Hub
        with gr.Column(scale=1, elem_classes=["card-panel"]):
            with gr.Tabs():
                with gr.TabItem("📖 Concept Summary"):
                    summary_title = gr.Textbox(
                        label="Source / Concept Title",
                        interactive=False
                    )
                    summary_content = gr.TextArea(
                        label="Educational Summary & Key Takeaways",
                        lines=14,
                        interactive=False
                    )
                    source_link_html = gr.HTML()

                with gr.TabItem("▶️ YouTube Tutorials"):
                    youtube_container = gr.HTML("<p style='color: #94a3b8; padding: 12px;'>Upload notes to see recommended video tutorials.</p>")

                with gr.TabItem("🗂️ Quizzes & Flashcards"):
                    study_cards_container = gr.HTML("<p style='color: #94a3b8; padding: 12px;'>Flashcards and active-recall test questions will appear here.</p>")

                with gr.TabItem("💬 Ask AI About This Lecture"):
                    chat_window = gr.Chatbot(
                        label="Lecture Q&A Assistant",
                        height=350
                    )
                    with gr.Row():
                        chat_text_input = gr.Textbox(
                            show_label=False,
                            placeholder="Ask any question about this lecture (e.g. 'Summarize key points')...",
                            scale=4
                        )
                        ask_button = gr.Button("Ask", scale=1, elem_classes=["primary-btn"])

    # Connect Events cleanly
    file_input.upload(
        fn=process_upload_event,
        inputs=[file_input, top_k_slider],
        outputs=[
            status_box,
            topic_dropdown,
            topic_tags_display,
            link_dropdown,
            summary_title,
            summary_content,
            source_link_html,
            youtube_container,
            study_cards_container,
            resource_meta_state,
            raw_document_state,
            all_topics_state,
            doc_name_state
        ],
        show_progress="minimal"
    )

    topic_dropdown.change(
        fn=topic_changed_event,
        inputs=[topic_dropdown, resource_meta_state, all_topics_state, doc_name_state],
        outputs=[
            link_dropdown,
            summary_title,
            summary_content,
            source_link_html,
            youtube_container,
            study_cards_container,
            resource_meta_state
        ],
        show_progress="minimal"
    )

    link_dropdown.change(
        fn=link_changed_event,
        inputs=[link_dropdown, resource_meta_state, topic_dropdown, all_topics_state, doc_name_state],
        outputs=[
            summary_title,
            summary_content,
            source_link_html,
            study_cards_container
        ],
        show_progress="minimal"
    )

    ask_button.click(
        fn=submit_question,
        inputs=[chat_text_input, chat_window, raw_document_state, topic_dropdown, summary_content],
        outputs=[chat_text_input, chat_window]
    )
    chat_text_input.submit(
        fn=submit_question,
        inputs=[chat_text_input, chat_window, raw_document_state, topic_dropdown, summary_content],
        outputs=[chat_text_input, chat_window]
    )

if __name__ == "__main__":
    demo.launch(share=False, css=custom_css)
