import sql
from art import *
from termcolor import colored
import inquirer
from prettytable import PrettyTable

def notify_user(message, color):
    message = text2art(message)
    print(colored(message, color))

# Function to simplify getting input
def get_info(entity):
    if entity == 'user':
        try:
            return int(input("Enter User ID: "))
        except ValueError:
            return -1
    elif entity == 'task':
        try:
            return int(input("Enter Task ID: "))
        except ValueError:
            return -1
    elif entity == 'tag':
        try:
            return int(input("Enter Tag ID: "))
        except ValueError:
            return -1
    elif entity == 'name':
        return input("Enter name: ")
    elif entity == 'email':
        return input("Enter the new user email: ")
    elif entity == 'phone':
        return input("Enter user phone number: ")
    elif entity == 'desc':
        return input("Enter new task description: ")
    elif entity == 'preference':
        return input("Any preference you would like to add? ")
    elif entity == 'address':
        return input("Enter user address: ")
    elif entity == 'date':
        return input("Enter due date (YYYY-MM-DD) for task: ")
    elif entity == 'status':
        return input("Enter task status: ")

# Function to create a pretty tables with different structures
def my_pretty_table(records ,structure):
    table = PrettyTable(structure)
    for record in records:
        table.add_row(record)
    print(table)



def main():
    ascii_banner = text2art("Task Manager")
    print(colored(ascii_banner, 'green'))

    print("This is a task manager to manage your daily tasks\n")
    print("Please choose what do you want to do: ")

    actions = [
        "Create User", "View User", "Update User", "Delete User", "Fetch All Users", # 5 operations
        "Create User Details", "View User Details","Update User Details",  # 3 operations 
        "View user tasks", "Set Task As Complete", "Create Task", "Update Task", "Delete Task",   # 6 operations
        "Create Tag", "Assign Tag to Task", "View Tags for a Task", "View Tasks for a Tag", "View All Tags", "Update Tag", "Delete Tag",  # 6 operations
        "Exit"
    ]

    while True:
        action = inquirer.prompt([
            inquirer.List("action", message="what do you want to do?",
                        choices=actions,
            )])['action']
        

        if action == 'Exit':
            notify_user("BYE!", 'green')
            break


        # User operations


        elif action == 'Create User':
            sql.add_user(get_info('name'), get_info('email'))
            notify_user("User created successfully!", 'blue')

        elif action == 'View User':
            user = sql.read_user(get_info('user'))
            if user == False:
                continue
            my_pretty_table([user], ["ID", "Name", "Email"])

        elif action == 'Update User':
            updated = sql.update_user(get_info('user'), get_info('name'), get_info('email'))
            if updated == False:
                continue
            notify_user("User updated successfully!", 'blue')
    
        elif action == 'Delete User':
                user_id = get_info('user')
                deleted = sql.delete_user(user_id)
                if deleted == False:
                    continue
                notify_user("User deleted!", 'blue')
    

        elif action == 'Fetch All Users':
            users = sql.read_users()
            my_pretty_table(users, ["ID", "Name", "Email"])


        # UserDetails operations


        elif action == 'Create User Details':
            created = sql.add_user_details(get_info('user'), get_info('phone') ,get_info('address') , get_info('preference'))
            if created == False:     
                continue
            notify_user("User details added successfully!", 'blue')
            
        elif action == 'View User Details':
                details = sql.read_user_details(get_info('user'))
                if details == False:
                    continue
                elif details == None:
                    print("No details for this user.")
                    continue
                my_pretty_table([details], ["User Details ID","User ID", "Phone", "Address", "Preference"])
            
            
        elif action == 'Update User Details':
            updated = sql.update_user_details(get_info('user'), get_info('phone'), get_info('address'), get_info('preference'))
            if updated == False:
                continue
            notify_user("User Details updated successfully!", 'blue')


        # Tasks operations


        elif action == 'View user tasks':
            tasks = sql.read_tasks_for_user(get_info('user'))
            if tasks == False:
                continue
            my_pretty_table(tasks, ["Task ID", "User ID", "Description", "Due Date", "Status"])

        elif action == 'Set Task As Complete':
            returned = sql.check_task(get_info('task'))
            if returned == False:
                continue
            notify_user("Task Completed!", 'green')

        elif action == 'Create Task':
            returned = sql.add_task(get_info('user'), get_info('desc'), get_info('date'), get_info('status'))
            if returned == False:
                continue
            notify_user("Task added successfully!", 'blue')

        elif action == 'Update Task':
            returned = sql.update_task(get_info('task'), get_info('desc'), get_info('date'), get_info('status'))
            if returned == False:
                continue
            notify_user("Task updated successfully!", 'blue')

        elif action == 'Delete Task':
                returned = sql.delete_task( get_info('task'))
                if returned == False:
                    print("This task does not exist or has been deleted before.")
                    continue
                notify_user("Task deleted successfully!", 'blue')
    

        # Tags operations
        

        elif action == 'Create Tag': 
            sql.add_tag(get_info('name'))
            notify_user("Tag added successfully!", 'blue')

        elif action == 'Update Tag':
            returned = sql.update_tag(get_info('tag'), get_info('name'))
            if returned == False:
                continue
            notify_user("Tag Updated Successfully!", 'blue')

        elif action == 'Assign Tag to Task': 
            returned = sql.add_task_tag(get_info('task'), get_info('tag'))
            if returned == False:
                continue
            notify_user("Tag assigned to task!", 'blue')


        elif action == 'View Tags for a Task': 
            tags = sql.read_tags_for_task(get_info('task'))
            if tags == False:
                continue
            my_pretty_table(tags, ["Tag ID"])
            
        elif action == 'View Tasks for a Tag': 
            tasks = sql.read_tasks_for_tags(get_info('tag'))
            if tasks == False:
                continue
            elif tasks == None: 
                print("There are no tasks tagged with this tag.")
                continue
            my_pretty_table(tasks, ["Task ID"])
            

        elif action == 'View All Tags': 
            tags = sql.read_tags()
            my_pretty_table(tags, ["Tag ID", "Name"])

        elif action == 'Update Tag': 
            returned = sql.update_tag(get_info('tag'), get_info('name'))
            if returned == False:
                continue
            notify_user("Tag updated successfully!", 'blue')
        

        elif action == 'Delete Tag':
            returned = sql.delete_tag(get_info('tag'))
            if returned == False:
                print("This tag does not exist or has been deleted before.")
                continue
            notify_user("Tag deleted successfully!", 'blue')   
               
        elif action == 'Delete Tag from Task':
            returned = sql.delete_task_tag(get_info('task'), get_info('tag'))
            if returned == False:
                continue
            notify_user("Tag removed successfully!", 'blue')
            

             

if __name__ == '__main__':
    main()