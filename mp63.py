import subprocess

def run_command(command):
    """Run a shell command and print its output."""
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode())

def list_containers(all_containers=False):
    """List containers."""
    cmd = "docker ps -a" if all_containers else "docker ps"
    run_command(cmd)

def start_container():
    container_id = input("Enter container name or ID to start: ").strip()
    run_command(f"docker start {container_id}")

def stop_container():
    container_id = input("Enter container name or ID to stop: ").strip()
    run_command(f"docker stop {container_id}")

def exec_into_container():
    container_id = input("Enter container name or ID to exec into: ").strip()
    shell = input("Shell to use (default: /bin/bash): ").strip() or "/bin/bash"
    run_command(f"docker exec -it {container_id} {shell}")

def main():
    while True:
        print("\n=== Docker CLI Wrapper ===")
        print("1. List running containers")
        print("2. List all containers")
        print("3. Start a container")
        print("4. Stop a container")
        print("5. Exec into a container")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            list_containers()
        elif choice == '2':
            list_containers(all_containers=True)
        elif choice == '3':
            start_container()
        elif choice == '4':
            stop_container()
        elif choice == '5':
            exec_into_container()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
