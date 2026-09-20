import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

def get_llm():
    """Factory function to return the configured LLM provider."""
    provider = os.getenv("LLM_PROVIDER", "huggingface").lower()
    
    if provider == "huggingface":
        from langchain_huggingface import HuggingFaceEndpoint
        # We use a fast, free Llama 3 model hosted by HuggingFace
        return HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
            task="text-generation",
            max_new_tokens=1024,
            temperature=0.1
        )
        
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4o", temperature=0.1)
        
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.1)
        
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")