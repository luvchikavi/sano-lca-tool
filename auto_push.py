import os
import time
import subprocess

# Path to your local Git repository
repo_path = "/Users/aviluvchik/Python Projects/Sano"

# Branch to push changes to
branch_name = "main"

def watch_files():
    """Watch for file changes and auto-commit/push to GitHub."""
    print("Watching for file changes in:", repo_path)
    last_modified_time = {}

    while True:
        # Walk through all files in the repository
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):  # Only monitor Python files
                    file_path = os.path.join(root, file)
                    modified_time = os.path.getmtime(file_path)

                    # If file is new or modified, commit and push
                    if file_path not in last_modified_time or last_modified_time[file_path] != modified_time:
                        last_modified_time[file_path] = modified_time
                        print(f"Detected change in {file_path}. Committing...")
                        commit_and_push(file_path)

        time.sleep(5)  # Check for changes every 5 seconds

def commit_and_push(file_path):
    """Commit and push changes to GitHub."""
    try:
        # Stage the file
        subprocess.run(["git", "add", file_path], check=True)
        # Commit with a message
        subprocess.run(["git", "commit", "-m", f"Auto-commit for {file_path}"], check=True)
        # Push to the specified branch
        subprocess.run(["git", "push", "origin", branch_name], check=True)
        print(f"Committed and pushed changes for {file_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Error committing or pushing changes: {e}")

if __name__ == "__main__":
    # Ensure we're in the correct directory
    os.chdir(repo_path)
    watch_files()
