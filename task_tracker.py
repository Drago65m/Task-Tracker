import os
import json
from datetime import datetime
from pprint import pprint
import argparse

def create_task_file():
    file_name = 'tasks.json'
    if not os.path.isfile(file_name):
        with open('tasks.json', 'w') as file:
            json.dump([], file)

    else:
        # Check if the file is empty
        with open(file_name, 'r+') as file:
            content = file.read().strip()
            if not content:
                file.seek(0)
                json.dump([], file)
                file.truncate()

            # Check if file the is a list
            else:
                file.seek(0)
                try:
                    data = json.load(file)
                    if not isinstance(data, list):
                        print('Something is wrong with your file')
                except:
                    file.seek(0)
                    json.dump([], file)
                    file.truncate()


def add_task(task_description):
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)

        # Check if there are any tasks in the .json fil
        # If there are no tasks, new task ID should be 1
        new_task_id = 0
        if not tasks:
            new_task_id = 1
        
        # Else get the last id of the current tasks, 
        # and plus +1 for the new ID
        else:
            highest_id = 0
            for task in tasks:
                if task['id'] > highest_id:
                    highest_id = task['id']
            new_task_id += highest_id + 1

    # Create the new task
    new_task = {
        'id': new_task_id,
        'description': task_description,
        'status': 'todo',
        'createdAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'updatedAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Add the new task to the json file
    tasks.append(new_task)

    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4, separators=(',',': '))
    
    print(f'Successfully created a new task with description: {task_description}')

def delete_task(task_id):
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)
        
        # Check if there are any tasks in the .json file
        if not tasks:
            print('You do not have any tasks')
        else:
            for task in tasks:
                if task['id'] == task_id:
                    tasks.remove(task)
                    print(f'Successfully deleted the Task ID: {task_id}')
                    break
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

def update_task(task_id, new_desc=None, new_status=None):
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)

        for task in tasks:
            if task['id'] == task_id:
                if new_desc:
                    task['description'] = new_desc
                    print(f'Changing description of the task')
                if new_status:
                    task['status'] = new_status
                    print(f'Changing status of the task')
                task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f'Successfully updated task id: {task_id}')
                break

    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

def display_task(task_desc=None, task_status=None):
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)

        # if task_status and task_desc are not provided, display all tasks
        if not task_status and not task_desc:
            pprint(tasks)

        elif task_desc and task_status:
            n_found = 0
            for task in tasks:
                if task['status'] == task_status and task['description'] == task_desc:
                    n_found += 1
                    print(task)
            print(f'{n_found} tasks found with description: {task_desc}; and status: {task_status}')
            
        elif task_desc:
            n_found = 0
            for task in tasks:
                if task['description'] == task_desc:
                    n_found += 1
                    print(task)
            print(f'{n_found} tasks found with description: {task_desc}')

        elif task_status:
            n_found = 0
            for task in tasks:
                if task['status'] == task_status:
                    n_found += 1
                    print(task)
            print(f'{n_found} tasks found with status: {task_status}')


        else:
            print(f'No tasks with\n\tTask Description: {task_desc}; Task Status: {task_status}; exist')

def main():

    parser = argparse.ArgumentParser(description='Task Tracker CLI')
    subparsers = parser.add_subparsers(dest='command')

    add_task_parser = subparsers.add_parser('add', help='Add a new task')
    add_task_parser.add_argument('description', nargs='*', type=str, help='Description of the new task')

    delete_task_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_task_parser.add_argument('task_id', type=int, help='ID of the task')
    
    update_task_parser = subparsers.add_parser('update', help='Update a task')
    update_task_parser.add_argument('task_id', type=int, help='ID of the task')
    update_task_parser.add_argument('--new_desc', nargs='+', type=str, help='New description for the task')
    update_task_parser.add_argument('--new_status', type=str, choices=['todo', 'in-progress', 'done'], help='New status for the task')

    status_in_progress = subparsers.add_parser('mark-in-progress', help='Mark task as in-progress')
    status_in_progress.add_argument('task_id', type=int, help='ID of the task')

    status_done_parser = subparsers.add_parser('mark-done', help='Mark task as done')
    status_done_parser.add_argument('task_id', type=int, help='ID of the task')

    list_tasks_parser = subparsers.add_parser('list', help='List tasks')
    list_tasks_parser.add_argument('--status', nargs='?', type=str, help='Status of the task')
    list_tasks_parser.add_argument('--desc', nargs='+', type=str, help='Description of the task')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(' '.join(args.description))
    elif args.command == 'delete':
        delete_task(args.task_id)
    elif args.command == 'update':
        new_desc = ' '.join(args.new_desc) if args.new_desc else None
        new_status = args.new_status if args.new_status else None
        
        update_task(args.task_id, new_desc=new_desc, new_status=new_status)
    elif args.command == 'list':
        desc = ' '.join(args.desc) if args.desc else None
        status = args.status if args.status else None

        display_task(task_desc=desc, task_status=status)

if __name__ == '__main__':
    main()