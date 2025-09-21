#!/usr/bin/env python3
"""
Git Difference Tool - Compare commits using Python
Supports multiple methods: subprocess, GitPython library, and command-line interface
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


# ========================================
# METHOD 1: Using subprocess (No dependencies)
# ========================================

class GitDiffSubprocess:
    def __init__(self, repo_path='.'):
        self.repo_path = Path(repo_path).resolve()

    def get_commit_info(self, commit_hash):
        """Get basic info about a commit"""
        try:
            cmd = [
                'git', '-C', str(self.repo_path), 'show',
                '--no-patch', '--format=%H|%an|%ae|%ad|%s', commit_hash
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            parts = result.stdout.strip().split('|')
            return {
                'hash': parts[0],
                'author': parts[1],
                'email': parts[2],
                'date': parts[3],
                'message': parts[4]
            }
        except subprocess.CalledProcessError as e:
            print(f"Error getting commit info: {e.stderr}")
            return None

    def get_diff_stats(self, commit1, commit2):
        """Get diff statistics between two commits"""
        try:
            cmd = ['git', '-C', str(self.repo_path), 'diff', '--stat', f"{commit1}..{commit2}"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error getting diff stats: {e.stderr}")
            return None

    def get_diff_summary(self, commit1, commit2):
        """Get summary of changes between commits"""
        try:
            cmd = ['git', '-C', str(self.repo_path), 'diff', '--name-status', f"{commit1}..{commit2}"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            changes = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('\t')
                    status = parts[0]
                    filename = parts[1]

                    status_map = {
                        'A': 'Added',
                        'M': 'Modified',
                        'D': 'Deleted',
                        'R': 'Renamed',
                        'C': 'Copied'
                    }

                    changes.append({
                        'status': status_map.get(status, status),
                        'file': filename
                    })

            return changes
        except subprocess.CalledProcessError as e:
            print(f"Error getting diff summary: {e.stderr}")
            return []

    def get_full_diff(self, commit1, commit2, context_lines=3):
        """Get full diff between two commits"""
        try:
            cmd = [
                'git', '-C', str(self.repo_path), 'diff',
                f'--unified={context_lines}', f"{commit1}..{commit2}"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error getting full diff: {e.stderr}")
            return None

    def get_diff_for_file(self, commit1, commit2, filepath):
        """Get diff for a specific file"""
        try:
            cmd = [
                'git', '-C', str(self.repo_path), 'diff',
                f"{commit1}..{commit2}", '--', filepath
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error getting file diff: {e.stderr}")
            return None


# ========================================
# METHOD 2: Using GitPython library
# ========================================

class GitDiffPython:
    def __init__(self, repo_path='.'):
        try:
            import git
            self.repo = git.Repo(repo_path)
            self.git_available = True
        except ImportError:
            print("GitPython not installed. Install with: pip install GitPython")
            self.git_available = False
        except Exception as e:
            print(f"Error initializing Git repo: {e}")
            self.git_available = False

    def get_commit_info(self, commit_hash):
        """Get commit information using GitPython"""
        if not self.git_available:
            return None

        try:
            commit = self.repo.commit(commit_hash)
            return {
                'hash': commit.hexsha,
                'author': commit.author.name,
                'email': commit.author.email,
                'date': commit.committed_datetime.isoformat(),
                'message': commit.message.strip(),
                'stats': commit.stats.total
            }
        except Exception as e:
            print(f"Error getting commit info: {e}")
            return None

    def get_diff_data(self, commit1, commit2):
        """Get comprehensive diff data using GitPython"""
        if not self.git_available:
            return None

        try:
            commit1_obj = self.repo.commit(commit1)
            commit2_obj = self.repo.commit(commit2)

            # Get diff between commits
            diff = commit1_obj.diff(commit2_obj)

            changes = []
            for item in diff:
                change_data = {
                    'file': item.a_path or item.b_path,
                    'change_type': item.change_type,
                    'old_file': item.a_path,
                    'new_file': item.b_path,
                }

                # Add diff content if available
                if hasattr(item, 'diff'):
                    try:
                        change_data['diff'] = item.diff.decode('utf-8')
                    except:
                        change_data['diff'] = "Binary file or encoding issue"

                changes.append(change_data)

            return {
                'commit1': self.get_commit_info(commit1),
                'commit2': self.get_commit_info(commit2),
                'changes': changes
            }
        except Exception as e:
            print(f"Error getting diff data: {e}")
            return None


# ========================================
# METHOD 3: Command Line Interface
# ========================================

class GitDiffCLI:
    def __init__(self):
        self.subprocess_diff = GitDiffSubprocess()
        self.python_diff = GitDiffPython()

    def display_commit_info(self, commit_info):
        """Display commit information in a formatted way"""
        if not commit_info:
            return

        print(f"📝 Commit: {commit_info['hash'][:8]}")
        print(f"👤 Author: {commit_info['author']} <{commit_info['email']}>")
        print(f"📅 Date: {commit_info['date']}")
        print(f"💬 Message: {commit_info['message']}")
        print("-" * 60)

    def display_diff_summary(self, changes):
        """Display a summary of changes"""
        if not changes:
            print("No changes found.")
            return

        print(f"\n📊 Summary: {len(changes)} file(s) changed")
        print("=" * 60)

        for change in changes:
            status_icons = {
                'Added': '✅',
                'Modified': '🔄',
                'Deleted': '❌',
                'Renamed': '📝',
                'Copied': '📋'
            }

            icon = status_icons.get(change['status'], '❓')
            print(f"{icon} {change['status']:<10} {change['file']}")

    def display_full_diff(self, diff_content):
        """Display full diff with syntax highlighting"""
        if not diff_content:
            print("No diff content available.")
            return

        print("\n🔍 Full Diff:")
        print("=" * 60)

        lines = diff_content.split('\n')
        for line in lines:
            if line.startswith('+++'):
                print(f"\033[92m{line}\033[0m")  # Green
            elif line.startswith('---'):
                print(f"\033[91m{line}\033[0m")  # Red
            elif line.startswith('+'):
                print(f"\033[92m{line}\033[0m")  # Green
            elif line.startswith('-'):
                print(f"\033[91m{line}\033[0m")  # Red
            elif line.startswith('@@'):
                print(f"\033[96m{line}\033[0m")  # Cyan
            else:
                print(line)

    def save_diff_report(self, commit1, commit2, output_file=None):
        """Save diff report to file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"git_diff_{commit1[:8]}_{commit2[:8]}_{timestamp}.md"

        try:
            with open(output_file, 'w') as f:
                f.write(f"# Git Diff Report\n\n")
                f.write(f"**Generated:** {datetime.now().isoformat()}\n")
                f.write(f"**Commits:** {commit1} → {commit2}\n\n")

                # Get commit info
                info1 = self.subprocess_diff.get_commit_info(commit1)
                info2 = self.subprocess_diff.get_commit_info(commit2)

                if info1:
                    f.write(f"## From Commit\n")
                    f.write(f"- **Hash:** {info1['hash']}\n")
                    f.write(f"- **Author:** {info1['author']}\n")
                    f.write(f"- **Message:** {info1['message']}\n\n")

                if info2:
                    f.write(f"## To Commit\n")
                    f.write(f"- **Hash:** {info2['hash']}\n")
                    f.write(f"- **Author:** {info2['author']}\n")
                    f.write(f"- **Message:** {info2['message']}\n\n")

                # Get changes summary
                changes = self.subprocess_diff.get_diff_summary(commit1, commit2)
                if changes:
                    f.write(f"## Changes Summary\n\n")
                    for change in changes:
                        f.write(f"- **{change['status']}:** {change['file']}\n")
                    f.write("\n")

                # Get stats
                stats = self.subprocess_diff.get_diff_stats(commit1, commit2)
                if stats:
                    f.write(f"## Statistics\n\n```\n{stats}\n```\n\n")

                # Get full diff
                full_diff = self.subprocess_diff.get_full_diff(commit1, commit2)
                if full_diff:
                    f.write(f"## Full Diff\n\n```diff\n{full_diff}\n```\n")

            print(f"✅ Diff report saved to: {output_file}")
            return output_file

        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return None

    def interactive_mode(self):
        """Interactive CLI mode"""
        print("🔄 Git Diff Tool - Interactive Mode")
        print("=" * 50)

        # Get repository path
        repo_path = input("Repository path (press Enter for current directory): ").strip()
        if not repo_path:
            repo_path = "."

        self.subprocess_diff = GitDiffSubprocess(repo_path)

        # Get commit hashes
        commit1 = input("Enter first commit hash (older): ").strip()
        commit2 = input("Enter second commit hash (newer): ").strip()

        if not commit1 or not commit2:
            print("❌ Both commit hashes are required!")
            return

        print(f"\n🔍 Analyzing commits {commit1[:8]}..{commit2[:8]}")

        # Display commit information
        print("\n" + "=" * 60)
        print("FROM COMMIT:")
        self.display_commit_info(self.subprocess_diff.get_commit_info(commit1))

        print("TO COMMIT:")
        self.display_commit_info(self.subprocess_diff.get_commit_info(commit2))

        # Display changes summary
        changes = self.subprocess_diff.get_diff_summary(commit1, commit2)
        self.display_diff_summary(changes)

        # Display stats
        stats = self.subprocess_diff.get_diff_stats(commit1, commit2)
        if stats:
            print(f"\n📈 Statistics:")
            print("=" * 60)
            print(stats)

        # Ask if user wants full diff
        show_full = input("\nShow full diff? (y/N): ").strip().lower()
        if show_full == 'y':
            full_diff = self.subprocess_diff.get_full_diff(commit1, commit2)
            self.display_full_diff(full_diff)

        # Ask if user wants to save report
        save_report = input("\nSave diff report to file? (y/N): ").strip().lower()
        if save_report == 'y':
            self.save_diff_report(commit1, commit2)


# ========================================
# UTILITY FUNCTIONS
# ========================================

def get_recent_commits(repo_path='.', count=10):
    """Get list of recent commits"""
    try:
        cmd = [
            'git', '-C', repo_path, 'log',
            '--oneline', f'-{count}', '--format=%H|%s'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|', 1)
                commits.append({
                    'hash': parts[0],
                    'message': parts[1] if len(parts) > 1 else ''
                })

        return commits
    except subprocess.CalledProcessError as e:
        print(f"Error getting recent commits: {e.stderr}")
        return []


def compare_commits_quick(commit1, commit2, repo_path='.'):
    """Quick comparison function"""
    diff_tool = GitDiffSubprocess(repo_path)

    print(f"🔍 Quick Comparison: {commit1[:8]} → {commit2[:8]}")
    print("=" * 50)

    # Get basic info
    info1 = diff_tool.get_commit_info(commit1)
    info2 = diff_tool.get_commit_info(commit2)

    if info1:
        print(f"From: {info1['message']} ({info1['author']})")
    if info2:
        print(f"To:   {info2['message']} ({info2['author']})")

    # Get changes
    changes = diff_tool.get_diff_summary(commit1, commit2)
    print(f"\nFiles changed: {len(changes)}")

    for change in changes[:10]:  # Show first 10 changes
        print(f"  {change['status']:<10} {change['file']}")

    if len(changes) > 10:
        print(f"  ... and {len(changes) - 10} more files")


# ========================================
# MAIN FUNCTION
# ========================================

def main():
    """Main function with command-line argument support"""
    if len(sys.argv) == 1:
        # Interactive mode
        cli = GitDiffCLI()
        cli.interactive_mode()

    elif len(sys.argv) == 3:
        # Quick mode with two commit hashes
        commit1, commit2 = sys.argv[1], sys.argv[2]
        compare_commits_quick(commit1, commit2)

    elif len(sys.argv) == 4 and sys.argv[1] == '--repo':
        # Quick mode with repository path
        repo_path = sys.argv[2]
        commits = get_recent_commits(repo_path, 5)

        print(f"📋 Recent commits in {repo_path}:")
        for i, commit in enumerate(commits):
            print(f"{i + 1}. {commit['hash'][:8]} - {commit['message']}")

    else:
        print("Git Diff Tool Usage:")
        print("  python git_diff.py                    # Interactive mode")
        print("  python git_diff.py <commit1> <commit2>  # Quick comparison")
        print("  python git_diff.py --repo <path>      # Show recent commits")
        print("\nExamples:")
        print("  python git_diff.py HEAD~2 HEAD")
        print("  python git_diff.py abc1234 def5678")
        print("  python git_diff.py --repo /path/to/repo")


if __name__ == "__main__":
    main()
