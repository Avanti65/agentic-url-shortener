import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

def get_llm():
    """Factory function to return the configured LLM provider."""
    provider = os.getenv("LLM_PROVIDER", "huggingface").lower()
    
    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        # Updated to the latest supported generation: Gemini 3.5 Flash
        return ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            temperature=0.1
        )
        
    elif provider == "huggingface":
        from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
        endpoint = HuggingFaceEndpoint(
            repo_id="HuggingFaceH4/zephyr-7b-beta", 
            max_new_tokens=1024,
            temperature=0.1
        )
        return ChatHuggingFace(llm=endpoint)
        
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4o", temperature=0.1)
        
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.1)
        
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")