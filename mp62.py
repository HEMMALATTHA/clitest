import json
import os
from datetime import datetime

DATA_FILE = "availability.json"

# Helper: Convert time string to datetime.time object
def to_time(tstr):
    return datetime.strptime(tstr, "%H:%M").time()

# Helper: Convert time object to string
def time_str(t):
    return t.strftime("%H:%M")

# Helper: Overlapping logic
def get_overlap(range1, range2):
    start1, end1 = range1
    start2, end2 = range2
    start = max(start1, start2)
    end = min(end1, end2)
    if start < end:
        return (start, end)
    return None

# Load availability from file
def load_availability():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            raw_data = json.load(f)
            loaded = {}
            for name, slots in raw_data.items():
                loaded[name] = [(to_time(start), to_time(end)) for start, end in slots]
            return loaded
    return {}

# Save availability to file
def save_availability(data):
    serializable = {
        name: [(time_str(start), time_str(end)) for start, end in slots]
        for name, slots in data.items()
    }
    with open(DATA_FILE, "w") as f:
        json.dump(serializable, f, indent=2)

# Show common free time slots
def find_common_slots(availability):
    if not availability:
        print("No availability data yet.")
        return

    people = list(availability.keys())
    common = availability[people[0]]

    for person in people[1:]:
        next_common = []
        for cslot in common:
            for pslot in availability[person]:
                overlap = get_overlap(cslot, pslot)
                if overlap:
                    next_common.append(overlap)
        common = next_common
        if not common:
            break

    print("\n🟢 Common Free Time Slots:")
    if not common:
        print("No common time slots available.")
    else:
        for start, end in common:
            print(f"- {time_str(start)} to {time_str(end)}")
    print()

# Add availability
def add_availability(availability):
    name = input("Enter person’s name: ").strip()
    slots = []
    print("Enter availability time slots (e.g., 09:00-11:00). Type 'done' when finished.")
    while True:
        line = input("Time slot: ").strip()
        if line.lower() == 'done':
            break
        try:
            start_str, end_str = line.split('-')
            start = to_time(start_str.strip())
            end = to_time(end_str.strip())
            if start >= end:
                print("⚠️ End time must be after start time.")
                continue
            slots.append((start, end))
        except Exception:
            print("⚠️ Invalid input format. Use HH:MM-HH:MM.")

    if name in availability:
        availability[name].extend(slots)
    else:
        availability[name] = slots

    save_availability(availability)
    print(f"✅ Availability added for {name}.\n")

# View availability
def view_availability(availability):
    if not availability:
        print("No availability added yet.\n")
        return
    print("\n🗓️ Current Availability:")
    for name, slots in availability.items():
        print(f"{name}:")
        for start, end in slots:
            print(f"  - {time_str(start)} to {time_str(end)}")
    print()

# Menu
def menu():
    availability = load_availability()

    while True:
        print("=== Meeting Scheduler ===")
        print("1. Add Availability")
        print("2. View Availability")
        print("3. Find Common Time Slots")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_availability(availability)
        elif choice == '2':
            view_availability(availability)
        elif choice == '3':
            find_common_slots(availability)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.\n")

# Run
if __name__ == "__main__":
    menu()
