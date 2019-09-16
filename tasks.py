#!/usr/bin/env python

import json
import os
import re
from time import sleep

import crayons

dir_path = os.path.dirname(os.path.realpath(__file__))
js_name = "my_todolist.js"
path_to_js = os.path.join(dir_path, js_name)


def dump_todo_list_to_json():
    with open(path_to_js, "w") as f:
        json.dump(todos, f, indent=4)
    print(crayons.yellow("\n[INFO] saved", bold=True))


if not os.path.isfile(path_to_js):
    print("not os.path.isfile(path_to_js)")
    open(js_name, "a").close()
    todos = {}
    todos["id"] = 0
    todos["tasks"] = {}
    dump_todo_list_to_json()
else:
    with open(path_to_js, "r") as f:
        todos = json.load(f)


def get_id():
    new_id = todos["id"] + 1
    todos["id"] = new_id
    return str(new_id)


def list_all_tasks():
    print("id:", todos["id"])
    for id_key, task in todos["tasks"].items():
        print("-" * 40)
        print(crayons.blue(id_key), task["status"], task["text"])
        print(crayons.yellow(task["tags"]))


def list_open_tasks():
    # print('id:', todos['id'])
    for id_key, task in todos["tasks"].items():
        if task["status"] == "open":
            # print("-" * 40)
            print(crayons.blue(id_key), crayons.green(task["status"]), task["text"])

            if len(task["comment"][0]) > 0:
                for c in task["comment"]:
                    print(' ' * 6, crayons.blue(c))

            if len(task["tags"][0]) > 0:
                print(' ' * 6, '- ', end='')
                for t in task["tags"]:
                    print(crayons.yellow(t), '- ', end='')
                print('')


def list_finished_tasks():
    # print('id:', todos['id'])
    for id_key, task in todos["tasks"].items():
        if task["status"] == "finished":
            # print("-" * 40)
            print(crayons.blue(id_key), crayons.blue(task["status"]), task["text"])

            if len(task["comment"][0]) > 0:
                for c in task["comment"]:
                    print(' ' * 10, crayons.yellow(c))

            if len(task["tags"][0]) > 0:
                print(' ' * 10, '- ', end='')
                for t in task["tags"]:
                    print(crayons.yellow(t), '- ', end='')
                print('')


actions = {
    "Add task": "n",
    "Edit task": "e",
    "Add comment task": "c",
    "Remove task": "r",
    "Finish task": "f",
    "Reopen task": "o",
    "List task": "t",
    "Cancel": "y",
    "Reset ALL": "resetall",
}


def list_actions():
    length = 23
    print('-' * length)
    for action, key in actions.items():
        x = length - len(action) - 12
        print('|', crayons.yellow(action), ' ' * x, '[', crayons.yellow(key.upper()), ']', ' |')
    print('-' * length)


def extract_data(inp: str):
    # print('extract_data', inp)
    # ACTION
    if inp == "resetall":
        action = "resetall"
    else:
        action = inp[:1].lower()
        if action not in actions.values():
            # print("ERROR action")
            action = None

    # TAGS
    tags = inp.split("*")[1:]

    # input ohne TAGS
    inp = inp.split("*")[0]
    # TASK ID
    try:
        task_id = re.search(r"\d+", inp).group()
    except AttributeError:
        # print("ERROR task_id")
        task_id = None

    if task_id:
        if task_id not in todos["tasks"].keys():
            # print("ERROR task_id 2")
            task_id = None

    # TEXT
    try:
        text = inp.partition(task_id)[2].lstrip()
    except TypeError:
        # print("ERROR text")
        try:
            text = inp.partition('n')[2].lstrip()
        except TypeError:
            # print("ERROR text")
            text = None
    

    # print(action, task_id, text)
    return action, task_id, text, tags


def _main():
    go = True
    while go:
        # clear screen
        os.system('cls')

        print("\n", "#" * 10, " FINISHED ", "#" * 60, "\n", sep='')
        list_finished_tasks()
        print("\n", "#" * 10, " OPEN ", "#" * 64, "\n", sep='')
        list_open_tasks()
        print("\n", "#" * 80, "\n", sep='')

        # list_actions()
        print("EXIT Y")
        action_input = input("Input:\t") or 0
        # print('action_input', action_input)

        if action_input:
            action, task_id, text, tags = extract_data(action_input)

            if action == "resetall":
                todos["id"] = 0
                todos["tasks"] = {}
                dump_todo_list_to_json()
                continue

            if action == "n":                                               # New entry
                task_id = get_id()
                todos["tasks"][task_id] = {"text": text, "status": "open", "comment": "", "tags": tags}
            elif action == "y":                                             # Cancel program
                go = False
            elif action == "t":                                             # List all tasks
                print("list tasks")
                sleep(3)
            elif action == "f":                                             # Set status to FINISH
                todos["tasks"][task_id]["status"] = "finished"
            elif action == "o":                                             # Set status to OPEN
                # todos["tasks"][task_id]["tags"].insert(0, "reopen")
                todos["tasks"][task_id]["status"] = "open"
            elif action == "r":                                             # Remove existing task
                todos["tasks"].pop(task_id, None)
            elif action == "e":                                             # Edit existing task
                todos["tasks"][task_id]["text"] = text
                todos["tasks"][task_id]["tags"] = tags
            elif action == "c":  # Edit comment
                comment_old = todos["tasks"][task_id]["comment"]
                todos["tasks"][task_id]["comment"] = '\n'.join([comment_old, text])

            dump_todo_list_to_json()


if __name__ == "__main__":
    _main()
