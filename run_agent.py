from agent.loop import run_agent

issue = "The average() function in calculator.py returns wrong values. average([2, 4, 6]) should be 4."

result = run_agent("sandbox/toy_repo", issue)
print("\n=== RESULT ===")
print(result["summary"])
print("Steps used:", result["steps"])
