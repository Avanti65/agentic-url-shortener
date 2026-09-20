from graph import app

def main():
    """Entry point for the Agentic SDLC Orchestrator."""
    print("Starting Agentic SDLC Orchestrator...\n")
    
    # The initial input to pass into the state machine
    # Update the request to build the Click Tracking feature
    initial_state = {
        "user_request": """Add a 'Clicks' integer property to the short URL database model with a default value of 0. 
Update the GET redirect endpoint so that every time a short URL is accessed, the Clicks counter is incremented by 1 and saved to the database. 
Make sure the new Clicks property is returned in the response when creating a new short URL.""",
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