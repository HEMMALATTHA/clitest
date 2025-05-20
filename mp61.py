import calendar
import datetime
import json
import os

EVENT_FILE = "events.json"

# Load events from JSON file
def load_events():
    if os.path.exists(EVENT_FILE):
        with open(EVENT_FILE, "r") as f:
            return json.load(f)
    return {}

# Save events to JSON file
def save_events(events):
    with open(EVENT_FILE, "w") as f:
        json.dump(events, f, indent=4)

# Show calendar with year/month validation
def show_calendar():
    while True:
        try:
            year = int(input("Enter year (2000–2080): "))
            if 2000 <= year <= 2080:
                break
            else:
                print("Year must be between 2000 and 2080.")
        except ValueError:
            print("Invalid year. Please enter a number.")

    while True:
        try:
            month = int(input("Enter month (1-12): "))
            if 1 <= month <= 12:
                break
            else:
                print("Month must be between 1 and 12.")
        except ValueError:
            print("Invalid month. Please enter a number.")

    print("\n" + calendar.month(year, month))

# Add an event
def add_event(events):
    while True:
        date_str = input("Enter event date (YYYY-MM-DD): ").strip()
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_obj < datetime.date.today():
                print("Date cannot be in the past.")
            elif date_obj.year > 2080:
                print("Year must not exceed 2080.")
            else:
                break
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")

    while True:
        event_name = input("Enter event name: ").strip()
        if event_name:
            break
        else:
            print("Event name cannot be empty.")

    events.setdefault(date_str, []).append(event_name)
    save_events(events)
    print("✅ Event added.")

# Check for upcoming events (within 7 days)
def check_upcoming_events(events):
    today = datetime.date.today()
    upcoming_days = 7
    found = False

    print("\n📅 Upcoming Events (next 7 days):")
    for date_str, event_list in events.items():
        try:
            event_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            delta = (event_date - today).days
            if 0 <= delta <= upcoming_days:
                found = True
                for event in event_list:
                    print(f"  - {event} on {event_date.strftime('%b %d, %Y')} (in {delta} days)")
        except:
            continue

    if not found:
        print("  No upcoming events.")

# Delete an event by date and index
def delete_event(events):
    date_str = input("Enter the event date to delete from (YYYY-MM-DD): ").strip()
    if date_str not in events:
        print("No events found on this date.")
        return

    print(f"\nEvents on {date_str}:")
    for idx, event in enumerate(events[date_str], start=1):
        print(f"{idx}. {event}")

    try:
        index = int(input("Enter the number of the event to delete: "))
        if 1 <= index <= len(events[date_str]):
            removed = events[date_str].pop(index - 1)
            if not events[date_str]:
                del events[date_str]
            save_events(events)
            print(f"✅ Deleted: {removed}")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")

# Edit event name
def edit_event(events):
    date_str = input("Enter the event date to edit (YYYY-MM-DD): ").strip()
    if date_str not in events:
        print("No events found on this date.")
        return

    print(f"\nEvents on {date_str}:")
    for idx, event in enumerate(events[date_str], start=1):
        print(f"{idx}. {event}")

    try:
        index = int(input("Enter the number of the event to edit: "))
        if 1 <= index <= len(events[date_str]):
            new_event = input("Enter the new event name: ").strip()
            if new_event:
                old = events[date_str][index - 1]
                events[date_str][index - 1] = new_event
                save_events(events)
                print(f"✅ Updated: '{old}' → '{new_event}'")
            else:
                print("Event name cannot be empty.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")

# Show all events sorted by date
def show_all_events(events):
    if not events:
        print("📭 No events found.")
        return

    print("\n📆 All Events Sorted by Date:")
    for date_str in sorted(events.keys()):
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            formatted_date = date_obj.strftime("%b %d, %Y")
        except:
            formatted_date = date_str

        print(f"\n{formatted_date}:")
        for event in events[date_str]:
            print(f"  - {event}")

# Main loop
def main():
    events = load_events()

    while True:
        print("\n=== CLI Calendar Menu ===")
        print("1. Show Calendar")
        print("2. Add Event")
        print("3. Show Upcoming Events")
        print("4. Exit")
        print("5. Delete Event")
        print("6. Edit Event")
        print("7. Show All Events")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            show_calendar()
        elif choice == "2":
            add_event(events)
        elif choice == "3":
            check_upcoming_events(events)
        elif choice == "4":
            print("👋 Goodbye!")
            break
        elif choice == "5":
            delete_event(events)
        elif choice == "6":
            edit_event(events)
        elif choice == "7":
            show_all_events(events)
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
