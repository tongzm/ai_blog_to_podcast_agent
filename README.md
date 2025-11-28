## 📰 ➡️ 🎙️ Blog to Podcast Agent

This is a Streamlit-based application that allows users to convert any blog post into a podcast. The app uses a configurable LLM (e.g., GPT, GLM) for content extraction, Firecrawl for scraping blog content, and Microsoft Edge's Text-to-Speech (TTS) service for generating audio. Users simply input a blog URL, and the app will generate a podcast episode based on the blog's main article.

## Features

- **Blog Scraping**: Scrapes the full content of any public blog URL using the Firecrawl API.

- **Content Extraction**: Uses a Large Language Model (LLM) to intelligently extract the title and main article from the scraped content, filtering out boilerplate like headers, footers, and ads.

- **Podcast Generation**: Converts the extracted text into an audio podcast using Microsoft Edge's **free** and high-quality TTS service.

- **Configurable APIs**: Allows users to configure their own LLM API key and endpoint, as well as their Firecrawl API key.

- **Voice Selection**: Provides a dropdown menu to select from a wide variety of voices and languages available through Edge TTS.

## Setup

### Requirements 

1. **API Keys**:
    - **LLM API Key**: An API key for an OpenAI-compatible service (e.g., [iFlow/Zhipu AI](https://platform.iflow.cn/) or OpenAI).

    - **Firecrawl API Key**: Get your Firecrawl API key from [firecrawl.dev](https://firecrawl.dev/).

2. **Python 3.8+**: Ensure you have Python 3.8 or higher installed.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Shubhamsaboo/awesome-llm-apps
   cd awesome-llm-apps/starter_ai_agents/ai_blog_to_podcast_agent
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
### Running the App

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. In the app interface:
    - Enter your LLM API Key, Base URL (optional), and Model ID in the sidebar.
    - Enter your Firecrawl API key in the sidebar.
    - Choose a voice for the narration.
    - Input the blog URL you want to convert.
    - Click "🎙️ Generate Podcast".
    - Listen to the generated podcast or download it.
