[English](README.md)

## 📰 ➡️ 🎙️ 博客转播客代理

这是一个基于 Streamlit 的应用程序，允许用户将任何博客文章转换为播客。该应用使用可配置的 LLM（例如 GPT、GLM）进行内容提取，使用 Firecrawl 抓取博客内容，并使用微软 Edge 的文本转语音（TTS）服务生成音频。用户只需输入博客 URL，应用即可根据博客的主要文章生成一集播客。

## 功能

- **博客抓取**: 使用 Firecrawl API 抓取任何公共博客 URL 的全部内容。

- **内容提取**: 使用大型语言模型（LLM）智能地从抓取的内容中提取标题和主要文章，过滤掉页眉、页脚和广告等样板内容。

- **播客生成**: 使用微软 Edge **免费**且高质量的 TTS 服务将提取的文本转换为音频播客。

- **可配置的 API**: 允许用户配置自己的 LLM API 密钥和端点，以及他们的 Firecrawl API 密钥。

- **语音选择**: 提供一个下拉菜单，可以从 Edge TTS 提供的多种语音和语言中进行选择。

## 设置

### 要求

1. **API 密钥**:
    - **LLM API 密钥**: 一个与 OpenAI 兼容的服务的 API 密钥（例如，[智谱AI](https://platform.iflow.cn/) 或 OpenAI）。

    - **Firecrawl API 密钥**: 从 [firecrawl.dev](https://firecrawl.dev/) 获取您的 Firecrawl API 密钥。

2. **Python 3.8+**: 确保您已安装 Python 3.8 或更高版本。

### 安装
1. 克隆此存储库：
   ```bash
   git clone https://github.com/Shubhamsaboo/awesome-llm-apps
   cd awesome-llm-apps/starter_ai_agents/ai_blog_to_podcast_agent
   ```

2. 安装所需的 Python 包：
   ```bash
   pip install -r requirements.txt
   ```
### 运行应用

1. 启动 Streamlit 应用：
   ```bash
   streamlit run app.py
   ```

2. 在应用界面中：
    - 在侧边栏中输入您的 LLM API 密钥、基础 URL（可选）和模型 ID。
    - 在侧边栏中输入您的 Firecrawl API 密钥。
    - 为旁白选择一种语音。
    - 输入您想要转换的博客 URL。
    - 点击“🎙️ 生成播客”。
    - 收听生成的播客或下载它。
