from datetime import datetime
import csv

# Constant day when open the app
TODAY = datetime.now()

def formated_date(date) -> str:
    return datetime.strftime(date, "%d-%m-%y")

def main():
    while True:
        print_main_menu()
        user_select = input().strip()

        if user_select == "1":
            add_task(create_task())
            print("\nAdd task!")
        elif user_select == "2":
            watch_tasks()
        elif user_select == "3":
            print("\nExit succeful! Good bye.🌞")
            break
        else:
            print("\n❗Please write 1 , 2 or 3")
            continue


# Create task
def create_task() -> dict:
    """
    Prompts the user for information about a task and
    returns a dictionary containing the details.
    Returns:
        A dictionary with the following fields:
        - 'task' (str): The description of the task.
        - OPTIONAL 'date' (str): The date of the task in 'DD-MM-YY' format..
    """
    # Prompts task
    task_prompt = input("\n📝Create task: ").strip()
    # Question for set reminder
    while True:
        reminder_res = input("\n🔔Set reminder? (y/n): ").strip().lower()
        if reminder_res == "y":
            reminder_date = set_reminder()
            # User regrets setting reminder
            if reminder_date == "cancel":
                continue
            return {
                "task": task_prompt,
                "reminder": formated_date(reminder_date),
            }
        elif reminder_res == "n":
            return {"task": task_prompt, "reminder": ""}
        else:
            print('\n❗Please write "y" or "n"')
            continue
# Set reminder with obj datetime
def set_reminder():
    """
    Prompts the user to enter a date in 'dd-mm-yy' format to set a reminder.
    If the date is before the current date, the user is prompted again. The user can also cancel the operation.

    Returns:
        A `datetime.datetime` object representing the entered date with hours and minutes set to zero,
        or the string "cancel" if the user decides to cancel the operation.
    """
    while True:
        try:
            date_prompt = input(
                '\n🗓️Write date: (dd-mm-yy) or "cancel" for cancel reminder '
            ).strip()
            if date_prompt.lower() == "cancel":
                return date_prompt.lower()
            date_check = datetime.strptime(date_prompt, "%d-%m-%y")
            # Temp object date!!
            if date_check.date() < TODAY.date():
                print("\n❗Date than lower what today")
                continue
            return date_check
        except ValueError:
            print('\n❗Please write date: (dd-mm-yy) or "cancel"')
            continue
# Add task in csv
def add_task(task):
    try:
        with open("task.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["tasks", "reminder", "state"])
            writer.writerow(
                {
                    "tasks": task["task"],
                    "reminder": task["reminder"],
                    "state": "pending",
                }
            )
    except FileNotFoundError:
        print("Error add task!")
# Print main menu with 3 options
def print_main_menu():
    print("\nTODO LIST: -------------------\n")
    print("1.📋Create task")
    print("2.👀Watch tasks")
    print("3.🚪Exit")
    print("\n------------------------------")
def watch_tasks():
    while True:
        print_tasks_pending()
        print_menu_tasks()
        user_select_wtmenu = input("")
        if user_select_wtmenu == "1":
            mark_done_task()
        elif user_select_wtmenu == "2":
            print_task_done()
        elif user_select_wtmenu == "3":
            back_pending_status()
        elif user_select_wtmenu == "4":
            clean_tasks_done()
        elif user_select_wtmenu == "5":
            break
# Print list task pendings
def print_tasks_pending():
    print("TO DO: -----------------------\n")
    try:
        with open("task.csv", newline="") as file:
            reader = csv.DictReader(file)
            # Iterator for tasks pendings and after print then
            tasks_list = (
                {"task": row["tasks"], "reminder": row["reminder"]}
                for row in reader
                if row["state"] == "pending"
            )
            for i, row in enumerate(tasks_list, 1):
                if row["reminder"] == "":
                    print(f"{i}. {row['task']} -- ⭕")
                else:
                    days = days_left(row["reminder"])
                    print(f"{i}. {row['task']} | {days} days... -- ⭕")
    except FileNotFoundError:
        print("Error watch tasks!")

    print("\n------------------------------")
# Print menu task with 5 options
def print_menu_tasks():
    print("\n1.✔️ Mark task done")
    print("2.🗒️ Wath done tasks")
    print("3.⬅️ Back to pending status")
    print("4.🧹Clean done tasks")
    print("5.🚪Back main menu\n")
# How many days left o past reminder
def days_left(date_str) -> str:
    date_obj = datetime.strptime(date_str, "%d-%m-%y")
    days = (date_obj - TODAY).days
    days = int(days)
    if days == 0:
        return "🔛Today"
    elif days < 0:
        return f"🔚Past {str(days)}"
    elif days > 0:
        return f"🔜Left {str(days)}"
# Mark and update task for done
def mark_done_task():
    list_tasks = []

    with open("task.csv", newline="") as file:
        reader = csv.DictReader(file)
        list_tasks = [row for row in reader]

    # Filter task pending
    pending_tasks = [task for task in list_tasks if task["state"] == "pending"]

    if not pending_tasks:
        print("❗No pending tasks.")
        return

    while True:
        try:
            select_mark = int(input("✅Task mark done: "))
            if select_mark in range(1, len(pending_tasks) + 1):
                # Ident task
                selected_task = pending_tasks[select_mark - 1]

                # Update list_tasks
                for task in list_tasks:
                    if task == selected_task:
                        task["state"] = "done"
                        break

                print(f"✅{selected_task['tasks']} is done!")
                break
            else:
                print(f"❗Please write a number between 1 and {len(pending_tasks)}")
        except ValueError:
            print("❗Please enter a valid number.")

    # Escribir todas las tareas de nuevo en el archivo
    with open("task.csv", "w", newline="") as file:
        fieldnames = ["tasks", "reminder", "state"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(list_tasks)
# Print only tasks done
def print_task_done():
    print("DONE: ------------------------\n")
    try:
        with open("task.csv", newline="") as file:
            reader = csv.DictReader(file)
            # List for tasks done and after print then
            tasks_done_list = [
                {"task": row["tasks"], "reminder": row["reminder"]}
                for row in reader
                if row["state"] == "done"
            ]
            # tasks_done_list empty
            if not tasks_done_list:
                print("❗There are no tasks done")
                return
            
            for i, row in enumerate(tasks_done_list, 1):
                if row["reminder"] == "":
                    print(f"{i}. {row['task']} -- ✅")
                else:
                    print(f"{i}. {row['task']} {row["reminder"]} -- ✅")
    except FileNotFoundError:
        print("Error watch tasks done!")
    
    print("\n------------------------------")
# Back to pending status and update csv
def back_pending_status():
    print_task_done()
    tasks_list = []
    with open("task.csv", newline="") as file:
        reader = csv.DictReader(file)
        tasks_list = [row for row in reader]
    tasks_done = [row for row in tasks_list if row["state"] == "done"]
    
    if not tasks_done:
        print("❗No task to move back to pending")
        return

    while True:
        try:
            task_select = int(input("Select task done: "))
            if task_select in range(1, len(tasks_done) + 1):
                selected_task = tasks_done[task_select - 1]
                # Update tasks_list
                for task in tasks_list:
                    if task == selected_task:
                        task["state"] = "pending"
                        print(f'🔙Task: {task["tasks"]} is back to pending!')
                        break
                break
            else:
                print(f"❗Please write a number between 1 and {len(tasks_done)}")
        except ValueError:
            print("❗Please enter a valid number.")

    with open("task.csv", "w", newline="") as file:
        fieldnames = ["tasks", "reminder", "state"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks_list)

def clean_tasks_done():
    list_tasks = []
    with open("task.csv",newline="") as file:
        reader = csv.DictReader(file)
        list_tasks = [row for row in reader if row["state"] == "pending"]
    with open("task.csv","w",newline="") as file:
        fieldnames = ["tasks", "reminder", "state"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(list_tasks)
    print("\n🧹CLEAN TASKS DONE")
if __name__ == "__main__":
    main()
