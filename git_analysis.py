import git
import os

# Repository URL and local directory
repo_url = "https://github.com/Nagaan/auto-report-writer"
repo_dir = "./auto-report-writer"

# Clone the repository if it doesn't exist locally
if not os.path.exists(repo_dir):
    git.Repo.clone_from(repo_url, repo_dir)

# List the files and directories in the cloned repository
repo_contents = os.listdir(repo_dir)
print("Repository Contents:", repo_contents)


# Function to analyze the structure of the repository
def analyze_structure(path, level=0):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        print("  " * level + "|-- " + item)
        if os.path.isdir(item_path):
            analyze_structure(item_path, level + 1)


# Analyze the structure of the cloned repository
analyze_structure(repo_dir)
