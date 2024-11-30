import psutil
import os
import subprocess
import signal


def get_top_cpu_processes(sort_by='cpu', limit=5):
    processes = [(process.info['pid'], process.info['name'], process.info['cpu_percent']) 
                 for process in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
    processes = [p for p in processes if p[2] is not None]
    sorted_processes = sorted(processes, key=lambda x: x[2], reverse=True)[:limit]
    print(f"\nTop {limit} processes by {sort_by} usage:")
    for pid, name, cpu in sorted_processes:
        print(f"PID: {pid}, Name: {name}, CPU%: {cpu}")


def get_top_mem_processes(sort_by='mem', limit=5):
    processes = [(process.info['pid'], process.info['name'], process.info['memory_percent']) 
                 for process in psutil.process_iter(['pid', 'name', 'memory_percent'])]
    processes = [p for p in processes if p[2] is not None]
    sorted_processes = sorted(processes, key=lambda x: x[2], reverse=True)[:limit]
    print(f"\nTop {limit} processes by {sort_by} usage:")
    for pid, name, mem in sorted_processes:
        print(f"PID: {pid}, Name: {name}, MEM%: {mem}")


def get_process_info(pid):
    try:
        process = psutil.Process(pid)
        info = {
            "PID": pid,
            "Name": process.name(),
            "Status": process.status(),
            "uid": process.uids().real,
            "CPU%": process.cpu_percent(interval=0.1),
            "Memory%": process.memory_percent()
        }
        print("\nProcess Information:")
        for key, value in info.items():
            print(f"{key}: {value}")
    except psutil.NoSuchProcess:
        print(f"No process found with PID: {pid}")


def search_process(name=None, pid=None):
    try:
        if pid:
            get_process_info(pid)
        elif name:
            found = False
            for process in psutil.process_iter(['pid', 'name']):
                if name.lower() in process.info['name'].lower():
                    found = True
                    print(f"Found Process - PID: {process.info['pid']}, Name: {process.info['name']}")
            if not found:
                print(f"No process found with name containing: {name}")
        else:
            print("Please provide either a name or a PID.")
    except Exception as e:
        print(f"Error searching for process: {e}")


def kill_process(pid=None, name=None):
    try:
        if pid:
            os.kill(pid, signal.SIGTERM)
            print(f"Process with PID {pid} has been terminated.")
        elif name:
            for process in psutil.process_iter(['pid', 'name']):
                if name.lower() in process.info['name'].lower():
                    os.kill(process.info['pid'], signal.SIGTERM)
                    print(f"Process {process.info['name']} (PID: {process.info['pid']}) has been terminated.")
        else:
            print("Please provide either a name or a PID.")
    except psutil.NoSuchProcess:
        print("Process not found.")
    except Exception as e: 
        print(f"Error killing process: {e}")


def monitor_process(pid=None, name=None):
    try:
        target_process = None
        if pid:
            target_process = psutil.Process(pid)
        elif name:
            for process in psutil.process_iter(['pid', 'name']):
                if name.lower() in process.info['name'].lower():
                    target_process = process
                    break
        if not target_process:
            print("Process not found.")
            return

        print(f"Monitoring process: PID={target_process.pid}, Name={target_process.name()}")
        print("Press Ctrl+C to stop monitoring.")
        while True:
            print(f"CPU%: {target_process.cpu_percent()}, Memory%: {target_process.memory_percent()}")
            subprocess.run(["sleep", "1"])

    except psutil.NoSuchProcess:
        print("Process ended.")


def main():
    while True:
        print("\n--- Process Manager ---")
        print("1. Get top CPU processes")
        print("2. Get top memory processes")
        print("3. Get process info by PID")
        print("4. Search process by name or PID")
        print("5. Kill process by PID or name")
        print("6. Monitor a process")
        print("7. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            get_top_cpu_processes()
        elif choice == '2':
            get_top_mem_processes()
        elif choice == '3':
            pid = int(input("Enter PID: "))
            get_process_info(pid)
        elif choice == '4':
            search_type = input("Search by (name/pid): ").strip().lower()
            if search_type == 'name':
                name = input("Enter process name: ")
                search_process(name=name)
            elif search_type == 'pid':
                pid = int(input("Enter PID: "))
                search_process(pid=pid)
            else:
                print("Invalid choice.")
        elif choice == '5':
            kill_type = input("Kill by (name/pid): ").strip().lower()
            if kill_type == 'name':
                name = input("Enter process name: ")
                kill_process(name=name)
            elif kill_type == 'pid':
                pid = int(input("Enter PID: "))
                kill_process(pid=pid)
            else:
                print("Invalid choice.")
        elif choice == '6':
            monitor_type = input("Monitor by (name/pid): ").strip().lower()
            if monitor_type == 'name':
                name = input("Enter process name: ")
                monitor_process(name=name)
            elif monitor_type == 'pid':
                pid = int(input("Enter PID: "))
                monitor_process(pid=pid)
            else:
                print("Invalid choice.")
        elif choice == '7':
            print("Exiting Process Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
