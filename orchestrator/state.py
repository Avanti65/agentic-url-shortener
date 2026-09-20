from typing import TypedDict, Annotated, List, Dict, Any
import operator

class AgentState(TypedDict):
    # Core Request Context
    user_request: str
    
    # Execution & Code State
    plan: List[str]
    target_files: List[str]
    generated_code: Dict[str, str]
    
    # Validation & Metrics
    test_results: Dict[str, Any]
    retry_count: int

    human_approved: bool