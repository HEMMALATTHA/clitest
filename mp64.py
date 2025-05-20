import subprocess

def run_git_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode())

def git_status():
    run_git_command("git status")

def git_add():
    files = input("Enter files to add (or '.' for all): ").strip()
    run_git_command(f"git add {files}")

def git_commit():
    message = input("Enter commit message: ").strip()
    if not message:
        print("Commit message cannot be empty.")
        return
    run_git_command(f'git commit -m "{message}"')

def git_push():
    branch = input("Enter branch name to push (default: main): ").strip() or "main"
    run_git_command(f"git push origin {branch}")

def git_pull():
    branch = input("Enter branch name to pull (default: main): ").strip() or "main"
    run_git_command(f"git pull origin {branch}")

def main():
    while True:
        print("\n=== Git CLI Enhancer ===")
        print("1. git status")
        print("2. git add")
        print("3. git commit")
        print("4. git push")
        print("5. git pull")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            git_status()
        elif choice == "2":
            git_add()
        elif choice == "3":
            git_commit()
        elif choice == "4":
            git_push()
        elif choice == "5":
            git_pull()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
