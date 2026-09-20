from graph import app

def main():
    """Entry point for the Agentic SDLC Orchestrator."""
    print("Starting Agentic SDLC Orchestrator...\n")
    
    # The initial input to pass into the state machine
    initial_state = {
        "user_request": "Implement a custom alias feature for short URLs.",
        "retry_count": 0
    }
    
    # Invoke the LangGraph
    result = app.invoke(initial_state)
    
    print("\nWorkflow Complete. Final State Keys:")
    
    # Print out the keys available in our final state to verify data passed through
    for key, value in result.items():
        if key in ["plan", "retry_count"]:
            print(f"- {key}: {value}")
        else:
            print(f"- {key}: (Data present)")

if __name__ == "__main__":
    main()