import time
import sys
from graph import app

def main():
    print("========================================")
    print("🚀 Agentic SDLC: URL Shortener Assistant")
    print("========================================")
    print("Choose a task category:")
    print("  1. 🛠️ Add a new feature or endpoint")
    print("  2. 🧪 Generate unit tests")
    print("  3. 🧹 Refactor or optimize existing code")
    print("  4. 💬 Custom prompt")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice not in ["1", "2", "3", "4"]:
        print("Invalid choice. Exiting.")
        sys.exit(1)
        
    print("\nDescribe exactly what you want the agent to do:")
    user_input = input("-> ").strip()
    
    # Silently enrich the prompt based on the user's category selection
    if choice == "1":
        final_prompt = f"Feature Request for URL Shortener: {user_input}. Ensure no existing endpoints are broken."
    elif choice == "2":
        final_prompt = f"Test Generation: Write tests for the following URL Shortener logic: {user_input}"
    elif choice == "3":
        final_prompt = f"Refactoring Request: Improve the URL Shortener codebase by doing the following: {user_input}"
    else:
        final_prompt = user_input

    initial_state = {
        "user_request": final_prompt,
        "retry_count": 0
    }
    
    print(f"\n[Invoking Agentic Workflow]...\n")
    
    start_time = time.time()
    result = app.invoke(initial_state)
    end_time = time.time()
    
    latency_seconds = round(end_time - start_time, 2)
    total_retries = result.get("retry_count", 0)
    
    # Check if the Planner rejected the prompt
    plan_output = "\n".join(result.get("plan", []))
    if "REJECTED" in plan_output:
        success_status = "BLOCKED (Irrelevant Prompt)"
    else:
        success_status = "SUCCESS" if result.get("human_approved") is not False else "FAILED/REJECTED"
    
    print("\n" + "="*50)
    print("📈 AGENTIC TELEMETRY & RELIABILITY METRICS")
    print("="*50)
    print(f"Outcome Status       : {success_status}")
    print(f"End-to-End Latency   : {latency_seconds} seconds")
    print(f"Retry/Error Frequency: {total_retries} compiler errors caught & fixed")
    
    if total_retries > 0:
        approx_mttr = round(latency_seconds / (total_retries + 1), 2)
        print(f"Approximate MTTR     : {approx_mttr} seconds per autonomous fix")
    else:
        print("Approximate MTTR     : 0 seconds (Zero build failures)")
    print("="*50)

if __name__ == "__main__":
    main()