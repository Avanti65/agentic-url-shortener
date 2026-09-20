from graph import app
import time

def main():
    """Entry point for the Agentic SDLC Orchestrator."""
    print("Starting Agentic SDLC Orchestrator...\n")
    
    # The initial input to pass into the state machine
    initial_state = {
        "user_request": "Add a GET /stats/{shortCode} endpoint that returns the original URL, short code, and total clicks as JSON without redirecting the user. Do not modify any database models.",
        "retry_count": 0
    }
    
    # 1. Track Start Time
    start_time = time.time()
    
    # 2. Invoke the graph
    result = app.invoke(initial_state)
    
    # 3. Track End Time
    end_time = time.time()
    
    # 4. Calculate Reliability Metrics
    latency_seconds = round(end_time - start_time, 2)
    total_retries = result.get("retry_count", 0)
    
    # Determine final outcome state
    success_status = "SUCCESS" if result.get("human_approved") is not False else "FAILED/REJECTED"
    
    print("\n" + "="*50)
    print("📈 AGENTIC TELEMETRY & RELIABILITY METRICS")
    print("="*50)
    print(f"Outcome Status       : {success_status}")
    print(f"End-to-End Latency   : {latency_seconds} seconds")
    print(f"Retry/Error Frequency: {total_retries} compiler errors caught & fixed")
    
    if total_retries > 0:
        # Approximate MTTR based on execution time divided by the number of automated fixes
        approx_mttr = round(latency_seconds / (total_retries + 1), 2)
        print(f"Approximate MTTR     : {approx_mttr} seconds per autonomous fix")
    else:
        print("Approximate MTTR     : 0 seconds (Zero build failures)")
        
    print("="*50)

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()