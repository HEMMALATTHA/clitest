from jira import JIRA
import getpass

# Step 1: Connect to JIRA
def connect_to_jira():
    server = input("JIRA URL (e.g., https://your-domain.atlassian.net): ").strip()
    email = input("Your JIRA Email: ").strip()
    api_token = getpass.getpass("Enter your API token (hidden): ")

    try:
        jira = JIRA(server=server, basic_auth=(email, api_token))
        print("✅ Connected to JIRA!")
        return jira
    except Exception as e:
        print("❌ Failed to connect to JIRA:", e)
        return None

# Step 2: Create Issue
def create_issue(jira):
    project_key = input("Enter Project Key (e.g., PROJ): ").strip()
    summary = input("Enter Issue Summary: ").strip()
    description = input("Enter Issue Description: ").strip()
    issue_type = input("Enter Issue Type (e.g., Task, Bug, Story): ").strip()

    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': description,
        'issuetype': {'name': issue_type},
    }

    try:
        new_issue = jira.create_issue(fields=issue_dict)
        print(f"✅ Issue created: {new_issue.key}")
        return new_issue
    except Exception as e:
        print("❌ Error creating issue:", e)

# Step 3: Assign Issue
def assign_issue(jira, issue):
    assignee = input("Enter assignee username (Atlassian ID): ").strip()
    try:
        jira.assign_issue(issue, assignee)
        print(f"✅ Assigned to {assignee}")
    except Exception as e:
        print("❌ Could not assign issue:", e)

# Main CLI Menu
def main():
    jira = connect_to_jira()
    if not jira:
        return

    while True:
        print("\n--- JIRA CLI Menu ---")
        print("1. Create Issue")
        print("2. Create & Assign Issue")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_issue(jira)
        elif choice == "2":
            issue = create_issue(jira)
            if issue:
                assign_issue(jira, issue)
        elif choice == "3":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
