from langgraph.graph import StateGraph, END
from state import AgentState

# Define the Nodes (Agentic Steps)

def planner_node(state: AgentState):
    """
    Analyzes the user request and formulates a step-by-step execution plan.
    Updates the state with the generated plan.
    """
    print("\n[Node: Planner] Analyzing request and creating an execution plan...")
    return {"plan": ["Step 1: Understand task", "Step 2: Write code", "Step 3: Test"]}

def coder_node(state: AgentState):
    """
    Reads the execution plan and generates the required C# code.
    Updates the state with a dictionary of target files and their code.
    """
    print("\n[Node: Coder] Writing C# code based on the plan...")
    return {"generated_code": {"Program.cs": "// Dummy generated C# Code"}}

def validator_node(state: AgentState):
    """
    Executes the .NET test suite against the generated code.
    Simulates a failure on the first attempt and success on subsequent attempts.
    Updates test results and increments the retry counter.
    """
    print("\n[Node: Validator] Running 'dotnet test' against the codebase...")
    
    current_retries = state.get("retry_count", 0)
    passed = current_retries > 0 
    
    if passed:
        print(" -> Output: Tests Passed!")
    else:
        print(" -> Output: Tests Failed! (Simulated)")
        
    return {
        "test_results": {"passed": passed}, 
        "retry_count": current_retries + 1
    }

def human_gate_node(state: AgentState):
    """
    Acts as an approval checkpoint before code is considered finalized.
    """
    print("\n[Node: Human Gate] Feature ready. Pausing for human review...")
    return {}

# Conditional Logic

def route_after_validation(state: AgentState):
    """
    Evaluates the test results to determine the next node.
    Routes to the human gate if tests pass, loops back to the coder if they fail,
    or terminates the graph if the maximum retry limit is reached.
    """
    passed = state.get("test_results", {}).get("passed", False)
    retries = state.get("retry_count", 0)
    
    if passed:
        return "human_gate"
    elif retries < 3:
        print(f" -> Retrying... (Attempt {retries} of 3)")
        return "coder"
    else:
        print(" -> Max retries reached. Triggering rollback/abort.")
        return END

# Build Graph

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("planner", planner_node)
workflow.add_node("coder", coder_node)
workflow.add_node("validator", validator_node)
workflow.add_node("human_gate", human_gate_node)

# set start
workflow.set_entry_point("planner")

# Connect nodes
workflow.add_edge("planner", "coder")
workflow.add_edge("coder", "validator")

# Add conditional edge
workflow.add_conditional_edges(
    "validator",
    route_after_validation,
    {
        "human_gate": "human_gate",
        "coder": "coder",
        END: END
    }
)

# Set End, End human review
workflow.add_edge("human_gate", END)

# Compile
app = workflow.compile()