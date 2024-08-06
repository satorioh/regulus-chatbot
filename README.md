# Regulus Chatbot

## Tech Stack
- Python
- LangChain

## Project Overview
This project aims to demonstrate typical application scenarios of large models on the client side. It currently includes features such as chat, translation, legal assistant, and YouTube video summarization.

## Key Features
- Implemented chat and translation features using components like agent, tool, memory, and promptTemplate based on LLM and LangChain.
- Developed a legal assistant by integrating zilliz vector library and RetriveQA.
- Created a video summarization feature using youtube-transcript-api and load_summarize_chain.

## Installation and Running
1. Clone the project to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the project:
    ```bash
    python main.py
    ```

## Usage Instructions
- **Chat Feature**: Implemented using LLM and LangChain, supports multi-turn conversations.
- **Translation Feature**: Supports translation in multiple languages. See `config/global_config.py` for supported languages.
- **Legal Assistant**: Provides legal consultation services by integrating zilliz vector library and RetriveQA.
- **YouTube Video Summarization**: Provides video content summarization using youtube-transcript-api and load_summarize_chain.


## License
This project is licensed under the MIT License. See the LICENSE file for details.