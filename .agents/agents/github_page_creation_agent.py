#!/usr/bin/env python3
"""
GitHub Page Creation Agent
Purpose: Automates the creation of a GitHub Pages site for a given repository and branch.
"""

import os
import subprocess
import sys

def run(cmd):
    """Run a command and raise on error."""
    subprocess.run(cmd, check=True)

def create_pages(repo, branch="gh-pages"):
    """
    Create or update the gh-pages branch for the specified repository.
    - repo: GitHub repository identifier (e.g., 'owner/repo' or full HTTPS URL).
    - branch: Target branch name (default: 'gh-pages').
    """
    # Verify that a GitHub token is available
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("[REDACTED] GITHUB_TOKEN not set. Define it in the environment or Hermes memory.", file=sys.stderr)
        sys.exit(1)

    # Use a temporary directory for the worktree
    temp_dir = "tmp_gh_pages_worktree"
    if os.path.exists(temp_dir):
        subprocess.run(["rm", "-rf", temp_dir], check=True)

    # Clone the repository (supports HTTPS or SSH URLs)
    run(["git", "clone", repo, temp_dir])

    # Enter the cloned directory
    run(["git", "checkout", "-B", branch, "origin/" + branch], cwd=temp_dir)

    # Ensure there is at least a placeholder index.html
    index_path = os.path.join(temp_dir, "index.html")
    if not os.path.exists(index_path):
        with open(index_path, "w") as f:
            f.write("<h1>Hello from GitHub Pages!</h1>")
        run(["git", "add", "index.html"], cwd=temp_dir)
        run(["git", "commit", "-m", "Add placeholder index.html"], cwd=temp_dir)

    # Push the branch (creates it on the remote if it doesn't exist)
    run(["git", "push", "-u", "origin", branch, "--force"], cwd=temp_dir)

    # Cleanup temporary directory
    subprocess.run(["rm", "-rf", temp_dir], check=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: github_page_creation_agent.py <repository> [branch]", file=sys.stderr)
        sys.exit(1)

    repo_arg = sys.argv[1]
    branch_arg = sys.argv[2] if len(sys.argv) > 2 else "gh-pages"
    create_pages(repo_arg, branch_arg)