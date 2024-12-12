import os
import git

def manage_git_repo(repo_url: str, repo_dir: str):
    """
    Checks if a directory is a git repository with the specified remote.
    If it is, the script fetches and pulls the latest changes.
    If the directory does not exist or is not a repository, it creates the directory and clones the repo.
    
    Args:
        repo_url (str): The URL of the remote git repository.
        repo_dir (str): The local directory where the repo should be located.
    """
    try:
        if os.path.exists(repo_dir):
            if os.path.isdir(repo_dir):
                try:
                    # Try to open the existing repo
                    repo = git.Repo(repo_dir)
                    # Check if it has the correct remote URL
                    remotes = [remote.url for remote in repo.remotes]
                    if repo_url in remotes:
                        print(f"Directory '{repo_dir}' is a git repository with the correct remote URL.")
                        print("Fetching and pulling the latest changes...")
                        repo.git.fetch()
                        repo.git.pull()
                    else:
                        print(f"The directory '{repo_dir}' exists but does not have the specified remote URL.")
                except git.exc.InvalidGitRepositoryError:
                    print(f"The directory '{repo_dir}' exists but is not a valid git repository.")
                    print("Cloning the repository...")
                    clone_repo(repo_url, repo_dir)
            else:
                print(f"The path '{repo_dir}' exists but is not a directory.")
        else:
            print(f"The directory '{repo_dir}' does not exist. Creating it and cloning the repository...")
            clone_repo(repo_url, repo_dir)
    except Exception as e:
        print(f"An error occurred: {e}")

def clone_repo(repo_url: str, repo_dir: str):
    """Clones the git repository to the specified directory."""
    try:
        os.makedirs(repo_dir, exist_ok=True)
        git.Repo.clone_from(repo_url, repo_dir)
        print(f"Successfully cloned the repository from {repo_url} to {repo_dir}.")
    except Exception as e:
        print(f"Failed to clone repository: {e}")

if __name__ == "__main__":
    repo_url = "https://github.com/EU-ECDC/Respiratory_viruses_weekly_data.git"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.join(script_dir,"../raw_data/Respiratory_viruses_weekly_data")
    manage_git_repo(repo_url, repo_dir)
