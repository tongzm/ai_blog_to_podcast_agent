import os
import asyncio
import re
import streamlit as st
from uuid import uuid4

# Third-party imports
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.models.openai import OpenAIChat
from agno.tools.firecrawl import FirecrawlTools
import edge_tts
from edge_tts import VoicesManager
from langdetect import detect, LangDetectException

# -- Helper Functions --

def run_async(coro):
    """Runs an async coroutine in a sync context."""
    return asyncio.run(coro)

@st.cache_data
def get_edge_tts_voices_cached():
    """Fetches and caches available voices from edge-tts."""
    async def get_voices():
        try:
            voices = await VoicesManager.create()
            return voices.find()
        except Exception:
            return []
    return run_async(get_voices())

async def generate_edge_tts_audio(text, voice):
    """Generates audio using edge-tts and returns bytes."""
    communicate = edge_tts.Communicate(text, voice)
    audio_chunks = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])
    return b"".join(audio_chunks)

# -- Streamlit UI --
st.set_page_config(page_title="📰 ➡️ 🎙️ Blog to Podcast", page_icon="🎙️")
st.title("📰 ➡️ 🎙️ Blog to Podcast Agent")

# -- Sidebar Configuration --
st.sidebar.header("⚙️ Configuration")

with st.sidebar.expander("🤖 LLM Configuration", expanded=True):
    llm_api_key = st.text_input("API Key", type="password", help="Your API key for the LLM.")
    llm_base_url = st.text_input("Base URL", help="The base URL of the OpenAI-compatible API.", value="https://apis.iflow.cn/v1")
    llm_model_id = st.text_input("Model ID", help="The model name, e.g., glm-4.6, gpt-4o.", value="glm-4.6")
    firecrawl_key = st.text_input("Firecrawl API Key", type="password", help="Needed for scraping the blog content.")

with st.sidebar.expander("🗣️ TTS Configuration", expanded=True):
    st.info("Microsoft Edge TTS (Free) is used for audio generation.")
    
    ms_voice = None
    voices_list = get_edge_tts_voices_cached()
    
    if voices_list:
        voice_options = {f'{v["ShortName"]} ({v["Gender"]}) - {v["Locale"]}': v["ShortName"] for v in voices_list}
        default_voice_name = "zh-CN-XiaoxiaoNeural"
        default_index = 0
        if default_voice_name in voice_options.values():
            for i, key in enumerate(voice_options.keys()):
                if voice_options[key] == default_voice_name:
                    default_index = i
                    break
        
        selected_voice_label = st.selectbox(
            "Choose a Voice",
            options=list(voice_options.keys()),
            index=default_index,
            help="Select the voice for the podcast narration."
        )
        ms_voice = voice_options[selected_voice_label]
    else:
        st.warning("Could not fetch voice list. A default will be used.")
        ms_voice = "zh-CN-XiaoxiaoNeural"

st.sidebar.markdown("""
---
**Registration Links:**
- [Get your iFlow (智谱AI) API Key](https://platform.iflow.cn/)
- [Get your Firecrawl API Key](https://firecrawl.dev/)
""")

# -- Main App Logic --
url = st.text_input("Enter Blog URL:", "")

required_keys = [llm_api_key, firecrawl_key]
is_disabled = not all(required_keys)

if st.button("🎙️ Generate Podcast", disabled=is_disabled):
    if not url.strip():
        st.warning("Please enter a blog URL")
    else:
        with st.spinner("Processing..."):
            try:
                # 1. Setup Agent
                os.environ["OPENAI_API_KEY"] = llm_api_key
                os.environ["FIRECRAWL_API_KEY"] = firecrawl_key
                agent_model = OpenAIChat(id=llm_model_id, api_key=llm_api_key, base_url=llm_base_url or None)
                agent = Agent(name="BlogExtractor", model=agent_model, tools=[FirecrawlTools()], instructions=[])

                # 2. Run agent to extract plain text content
                st.info("Step 1/2: Scraping and extracting content...")
                prompt = (
                    "You are a content extraction engine. Your primary task is to extract the main article from the provided scraped content, including its title. "
                    "Follow these rules strictly: "
                    "1. Your output MUST BEGIN with the main title of the article. "
                    "2. After the title, extract ONLY the main body text of the article. "
                    "3. EXCLUDE all other elements, such as site-wide headers, navigation bars, footers, advertisements, author bios, and comment sections. "
                    "4. Your output MUST be plain text. Do NOT use any Markdown formatting. "
                    "5. Do NOT summarize, paraphrase, or change the original text. Output the extracted title and text verbatim. "
                    "6. Do NOT include any introductory phrases, explanations, or any text other than the extracted article content. "
                    f"Now, process the scraped content from this URL and extract its main title and body text: {url}"
                )
                response: RunOutput = agent.run(prompt)
                extracted_text = response.content if hasattr(response, 'content') else str(response)

                if not extracted_text:
                    st.error("Failed to extract content. The blog might be inaccessible or the LLM failed to process it.")
                else:
                    # 3. Generate Audio using the extracted plain text
                    st.info("Step 2/2: Generating audio...")
                    
                    if not ms_voice:
                        st.error("No TTS voice selected or available. Cannot generate audio.")
                    else:
                        st.write(f"Using voice: **{ms_voice}**")
                        audio_bytes = run_async(generate_edge_tts_audio(extracted_text, ms_voice))
                        
                        # 4. Display results
                        if audio_bytes:
                            st.success("Podcast generated! 🎧")
                            st.audio(audio_bytes, format="audio/mp3")
                            st.download_button("Download Podcast", audio_bytes, "podcast.mp3", "audio/mp3")
                            
                            with st.expander("📄 Extracted Text"):
                                st.text(extracted_text)
                        else:
                            st.error("Failed to generate audio.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
else:
    if is_disabled:
        st.info("Please fill in all required configuration in the sidebar to enable podcast generation.")
