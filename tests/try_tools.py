import sys
sys.path.append(".")

from agent.tools import RepoTools

tools = RepoTools("sandbox/toy_repo")

print("--- list_files ---")
print(tools.list_files())

print("--- read_file ---")
print(tools.read_file("calculator.py"))

print("--- search ---")
print(tools.search("average"))

print("--- edit_file (fix the bug) ---")
print(tools.edit_file("calculator.py", "(len(numbers) + 1)", "len(numbers)"))

print("--- run_tests ---")
print(tools.run_tests())