# Project by:   Arellano, Von Michael
#               Lacson, John Russel
#               Punzalan, Kurt Brian Daine
# Description:  This file contains the necessary functions to implement the task_app.

# IMPORTS
from cProfile import label
from zipapp import create_archive

import mysql.connector as mariadb
from mysql.connector import Error
from prettytable import PrettyTable

# Subject for change depending on the user and password.
mariadb_connection = mariadb.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",  # Enter password for your user
)

create_cursor = mariadb_connection.cursor()

# CREATE DATABASE AND USE IT
create_cursor.execute("CREATE DATABASE IF NOT EXISTS task_app")
create_cursor.execute("USE task_app")

# SHOW DATABASES
# create_cursor.execute("SHOW DATABASES")
# for x in create_cursor:
#    print(x)

# CREATE TABLES
# Create table for category
create_cursor.execute(
    "CREATE TABLE IF NOT EXISTS category (category_id INT(5) NOT NULL, category_name VARCHAR(30) NOT NULL, date_created DATETIME NOT NULL, CONSTRAINT category_category_id_pk PRIMARY KEY (category_id));"
)
# Create table for tasks
create_cursor.execute(
    "CREATE TABLE IF NOT EXISTS task (task_id INT(5) NOT NULL, title VARCHAR(40) NOT NULL, is_done BOOLEAN NOT NULL, date_created DATETIME NOT NULL, deadline DATETIME, dsc VARCHAR(60), CONSTRAINT task_task_id_pk PRIMARY KEY (task_id));"
)
# Create table for has
create_cursor.execute(
    "CREATE TABLE IF NOT EXISTS has(category_id INT(5), task_id INT(5), PRIMARY KEY (category_id, task_id), CONSTRAINT has_category_id_fk FOREIGN KEY (category_id) REFERENCES category(category_id), CONSTRAINT has_task_id_fk FOREIGN KEY (task_id) REFERENCES task(task_id));"
)

# SHOW TABLES
# create_cursor.execute("SHOW TABLES")
# for x in create_cursor:
#    print(x)

# INITIALIZE task_counter; will be used for task_id
task_statement = "SELECT MAX(task_id) FROM task;"
create_cursor.execute(task_statement)
task_counter = create_cursor.fetchone()[0]
if task_counter == None:
    task_counter = 0

# INITIALIZE category_counter; will be used for category_id
category_statement = "SELECT MAX(category_id) FROM category;"
create_cursor.execute(category_statement)
category_counter = create_cursor.fetchone()[0]
if category_counter == None:
    category_counter = 0


# FUNCTION to display menu.
def menuFunction():
    print("\n======= MENU ======")
    print("[1] Add a Task")
    print("[2] Edit a Task")
    print("[3] Delete a Task")
    print("[4] View All Task")
    print("[5] Mark Task as Done")
    print("[6] Add a category")
    print("[7] Edit category")
    print("[8] Delete category")
    print("[9] View category")
    print("[10] Add a Task to a Category")
    print("[11] View Task Due on Specific Day")
    print("[12] View Task Due on Specific Month")
    print("[0] Exit")
    print("===================\n")


# End of menuFunction


# FUNCTION to print the table depending on the desired format.
# Parameters:   view_all - the SQL query;
#               table - the PrettyTable format
#               label - the desired label of the table
def view(view_all, table, label):
    create_cursor.execute(view_all)
    tuples = create_cursor.fetchall()

    # print tuples in a table; source: https://www.geeksforgeeks.org/how-to-make-a-table-in-python/
    for x in tuples:
        table.add_row(list(x))
    print(label)
    print(table)


# End of view


# FUNCTION that accepts toExecute parameter which is the SQL query that needs to be executed.
def execute_and_commit(toExecute):
    create_cursor.execute(toExecute)
    mariadb_connection.commit()


# End of execute_and_commit


# FUNCTION to check if the given toCheck input exists in the database.
# Returns false if non-existent, else returns true.
def checkExistence(sql, toCheck):
    existing = False

    create_cursor.execute(sql)

    tuples = create_cursor.fetchall()
    for x in tuples:
        if (toCheck == x) or (toCheck == x[0]):
            existing = True

    return existing


# End of checkExistence


# FUNCTION for adding a task.
def addTask():
    global task_counter

    task_counter += 1
    task_id = task_counter

    # Print necessary prompt for a adding task.
    try:
        print("\nChoice: [1] Add a Task")
        title = input("\nEnter task title (maximum of 40 characters): ")
        deadline = input("Enter task deadline (MM-DD-YYYY HH:MM AM/PM): ")
        dsc = input("Enter task description (maximum of 60 characters): ")

        new_task = f"INSERT INTO task VALUES ({task_id}, '{title}', FALSE, NOW(), STR_TO_DATE('{deadline}', '%m-%d-%Y %h:%i %p'), '{dsc}');"
        execute_and_commit(new_task)
        print("\nAdded successfully.")
    except Error as e:
        print("\nInvalid input!")


# End of addTask


# FUNCTION for editing a task.
def editTask():
    select_empty = "SELECT COUNT(task_id) FROM task;"
    create_cursor.execute(select_empty)
    check_if_empty = create_cursor.fetchone()[0]

    print("\nChoice: [2] Edit Task")

    if check_if_empty == 0:
        print("Add tasks first!")
    else:

        viewAllTaskNoCategory()

        task_id = int(input("Enter the task id: "))
        input_exists = checkExistence("SELECT * FROM task;", task_id)

        if input_exists:

            # Print necessary prompt for editing tasks.
            print("\n====== EDIT ======")
            print("[1] Edit Task Title")
            print("[2] Edit Task Deadline")
            print("[3] Edit Task Description")
            print("[4] Delete a Task Category")
            print("==================\n")

            edit_choice = int(input("Enter choice: "))

            # Conditional statement for editing task title.
            if edit_choice == 1:
                try:
                    new_title = input("Enter a new title for your task: ")
                    edit_one = (
                        f"UPDATE task SET title='{new_title}' WHERE task_id={task_id}"
                    )
                    execute_and_commit(edit_one)
                    print("\n", new_title, "is now the new title of task id", task_id)

                except Error as e:
                    print("\n Title Edit unsuccessful.")
            # Conditional statement for editing task deadline.
            elif edit_choice == 2:
                try:
                    new_deadline = input(
                        "Enter new deadline (MM-DD-YYYY HH:MM AM/PM): "
                    )
                    edit_two = f"UPDATE task SET deadline=STR_TO_DATE('{new_deadline}', '%m-%d-%Y %h:%i %p') WHERE task_id={task_id}"
                    execute_and_commit(edit_two)
                    print(
                        "\n",
                        new_deadline,
                        "is now the new deadline of task id",
                        task_id,
                    )

                except Error as e:
                    print("\n Deadline edit unsuccessful.")
            # Conditional statement for editing task description.
            elif edit_choice == 3:
                try:
                    new_dsc = input("Enter new task description: ")
                    edit_three = (
                        f"UPDATE task SET dsc='{new_dsc}' WHERE task_id={task_id}"
                    )
                    execute_and_commit(edit_three)
                    print(
                        "\n", new_dsc, "is now the new description of task id", task_id
                    )

                except Error as e:
                    print("\n Description edit unsuccessful.")
            # Conditional statement for deleting task category.
            elif edit_choice == 4:
                try:
                    print("\nDeleting a Task from a Category...")
                    sqlCommand = f"SELECT category_id, category_name FROM has NATURAL JOIN category WHERE task_id={task_id};"
                    col_title = PrettyTable(["Category ID", "Category Name"])
                    label = f"\nCategory/ies with Task ID {task_id}"
                    view(sqlCommand, col_title, label)
                    cat_num = int(
                        input(
                            "\nChoose the category ID you want to delete this task id from: "
                        )
                    )

                    edit_four = f"DELETE FROM has WHERE task_id={task_id} AND category_id={cat_num}"
                    execute_and_commit(edit_four)
                    print(
                        "Successfully deleted task id",
                        task_id,
                        "from category id",
                        cat_num,
                    )

                except Error as e:
                    print("\nEdit unsuccessful.")
            else:
                print("\nInvalid choice!")

        else:
            print("\nChosen task id does not exist.")


# End of editTask


# FUNCTION for deleting a task
def deleteTask():
    print("\nChoice: [3] Delete a Task")

    viewAllTaskNoCategory()

    # Print and input necessary prompt for deleting a task.
    to_del = int(input("Enter task ID: "))
    input_exists = checkExistence("SELECT * FROM task;", to_del)

    if input_exists:
        # Delete task from "has" table
        del_task = f"DELETE FROM has WHERE task_id={to_del};"
        execute_and_commit(del_task)

        # Delete task from "task" table
        del_task = f"DELETE FROM task WHERE task_id={to_del};"
        execute_and_commit(del_task)

        print("\nDeleted Successfully.")
    else:
        print("\nChosen task id does not exist.")


# End of deleteTask


# FUNCTION for displaying all tasks along with their category
def viewAllTask():
    print("\nChoice: [4] View All Task")

    label = "\nTASK LIST:"
    view_all = "SELECT (SELECT category_id FROM has h WHERE h.task_id=t.task_id), (SELECT category_name FROM category c WHERE c.category_id IN (SELECT category_id FROM has h WHERE h.task_id=t.task_id)), task_id, title, is_done, date_created, deadline, dsc FROM task t;"
    task_table = PrettyTable(
        [
            "Category ID",
            "Category",
            "Task ID",
            "Task",
            "Done",
            "Date Created",
            "Deadline",
            "Description",
        ]
    )
    view(view_all, task_table, label)


# End of viewAllTask


# FUNCTION to print all tasks excluding their category
def viewAllTaskNoCategory():
    label = "\nTASK LIST"
    view_all = "SELECT * FROM task;"
    task_table = PrettyTable(
        ["Task ID", "Task", "Done", "Date Created", "Deadline", "Description"]
    )
    view(view_all, task_table, label)


# End of viewAllTaskNoCategory


# FUNCTION to mark a task as done.
def taskDone():
    print("\nChoice: [5] Mark Task as Done")
    viewAllTaskNoCategory()
    task_id = int(input("Enter task id of finished task: "))
    input_exists = checkExistence("SELECT * FROM task;", task_id)
    if input_exists:
        set_done = f"UPDATE task SET is_done=true WHERE task_id = {task_id}"
        execute_and_commit(set_done)
        print("Task id", task_id, "marked as done.")
    else:
        print("\nChosen task id does not exist.")


# End of taskDone


# FUNCTION to add a new category on the category table.
def addCategory():
    global category_counter
    category_counter += 1
    category_id = category_counter

    print("\nChoice: [6] Add a Category")
    category_name = input("\nEnter category name (maximum of 30 characters): ")

    new_category = (
        f"INSERT INTO category VALUES ({category_id}, '{category_name}', NOW());"
    )
    execute_and_commit(new_category)
    print("\nAdded Successfully.")


# End of addCategory


# FUNCTION to edit a category (category name).
def editCategory():
    print("\nChoice: [7] Edit Category")
    viewCategory()
    category_id = int(input("Enter the category id: "))
    input_exists = checkExistence("SELECT * FROM category;", category_id)
    if input_exists:

        try:
            new_name = input("Enter a new name for your category: ")
            edit_categ = f"UPDATE category SET category_name='{new_name}' WHERE category_id={category_id};"
            execute_and_commit(edit_categ)
            int("\n", new_name, "is now the new name of category id", category_id)

        except Error as e:
            print("\n Edit unsuccessful.")

    else:
        print("\nChosen category does not exist.")


# End of editCategory


# FUNCTION for deleting a category
def deleteCategory():
    print("\nChoice: [8] Delete Category")
    viewCategory()
    to_del = int(input("Enter category ID: "))
    input_exists = checkExistence("SELECT * FROM category;", to_del)
    if input_exists:
        del_task = f"DELETE FROM has WHERE category_id={to_del};"
        execute_and_commit(del_task)
        del_task = f"DELETE FROM category WHERE category_id={to_del};"
        execute_and_commit(del_task)
        print("\nDeleted Successfully.")
    else:
        print("\nChosen category does not exist.")


# End of deleteCategory


# FUNCTION to print the list of all categories (without tasks)
def viewCategory():
    label = "\nCATEGORY LIST:"
    view_all_category = "SELECT * FROM category;"
    column_label = PrettyTable(["Category ID", "Category Name", "Date Created"])
    view(view_all_category, column_label, label)


# End


# FUNCTION to print the categories including the tasks under them
def viewCategoryWithTasks():
    print("\nChoice: [9] View Category")
    # Fetch first the category id
    get_cat_ids = "SELECT * FROM category;"
    create_cursor.execute(get_cat_ids)
    # Returns array of tuples containing details of categories.
    all_cat_ids = create_cursor.fetchall()
    category_col_table = PrettyTable(["Category ID", "Category Name", "Date Created"])

    for x in all_cat_ids:
        # Print the details of category x
        category_col_table.add_row(list(x))
        print("\n\nCATEGORY: \n", category_col_table, "\n")
        category_col_table.clear_rows()

        # Fetch and print the tasks under category x
        label = f"TASK/S FOR CATEGORY {x[0]}:"
        get_tasks = f"SELECT task_id, title, is_done, date_created, deadline, dsc FROM task NATURAL JOIN has where category_id={x[0]};"
        task_col_table = PrettyTable(
            ["Task ID", "Task", "Done", "Date Created", "Deadline", "Description"]
        )
        view(get_tasks, task_col_table, label)


# End of viewCategoryWithTasks


# FUNCTION for adding a task to category
def addTaskToCategory():
    print("\nChoice: [10] Add a Task to a Category")
    viewAllTaskNoCategory()
    task_id = int(input("Select task id to add: "))
    get_task_ids = "SELECT task_id FROM task;"
    # Check first if the chosen task id is present.
    # False: meaning chosen task_id is not present, else True.
    task_existing = checkExistence(get_task_ids, task_id)

    # If task_exisiting is true
    if task_existing:

        viewCategory()
        category_id = int(input("Select category id: "))
        get_cat_ids = "SELECT category_id FROM category;"
        # Check first if the chosen category id is present.
        # False: meaning chosen category_id is not present, else True.
        cat_existing = checkExistence(get_cat_ids, category_id)

        # If cat_existing is true
        if cat_existing:

            # Check if the combination of category_id and task_id is already existing in the has table.
            insert_tuple = (category_id, task_id)
            get_tuple_comb = "SELECT * FROM has;"
            tuple_existing = checkExistence(get_tuple_comb, insert_tuple)

            if tuple_existing:
                print("\nThis task is already under this category.")
            else:
                # insert the sql statement in has table.
                print("\nAdding task id", task_id, "to category id", category_id, "...")
                insert_has = f"INSERT INTO has VALUES ({category_id}, {task_id});"
                execute_and_commit(insert_has)
                print(
                    "\nSuccessfully added task id",
                    task_id,
                    "in category id",
                    category_id,
                )

        # else if non-existent.
        else:
            print("\nChosen category id does not exit.")

    # else if non-existent.
    else:
        print("\nChosen task id does not exist.")


# End of addTaskToCategory


# BONUS FEATURES
# FUNCTION for viewing tasks due on a certain date
def viewTaskFromDay():
    print("\nChoice: [11] View Task Due on Specific Day")
    try:
        task_from_day = input("Enter date (MM-DD-YYYY): ")
        label = "\nTASK DUE ON " + task_from_day + ":"
        view_tfd = f"SELECT (SELECT category_id FROM has h WHERE h.task_id=t.task_id), (SELECT category_name FROM category c WHERE c.category_id IN (SELECT category_id FROM has h WHERE h.task_id=t.task_id)), task_id, title, is_done, date_created, deadline, dsc FROM task t WHERE DATE(deadline)=STR_TO_DATE('{task_from_day}', '%m-%d-%Y');"
        task_table = PrettyTable(
            [
                "Category ID",
                "Category",
                "Task ID",
                "Task",
                "Done",
                "Date Created",
                "Deadline",
                "Description",
            ]
        )
        view(view_tfd, task_table, label)

    except Error as e:
        print("\nInvalid input!")


# End of viewTaskFromDay


# FUNCTION for viewing tasks due on a certain month
def viewTaskFromMonth():
    print("\nChoice: [12] View Task Due on Specific Month")
    try:
        task_from_month = input("Enter month name (e.g. January): ")
        label = "\nTASK DUE ON " + task_from_month + ":"
        view_tfm = f"SELECT (SELECT category_id FROM has h WHERE h.task_id=t.task_id), (SELECT category_name FROM category c WHERE c.category_id IN (SELECT category_id FROM has h WHERE h.task_id=t.task_id)), task_id, title, is_done, date_created, deadline, dsc FROM task t WHERE MONTHNAME(deadline)=MONTHNAME(STR_TO_DATE('{task_from_month}', '%M'));"
        task_table = PrettyTable(
            [
                "Category ID",
                "Category",
                "Task ID",
                "Task",
                "Done",
                "Date Created",
                "Deadline",
                "Description",
            ]
        )
        view(view_tfm, task_table, label)

    except Error as e:
        print("\nInvalid input!")


# End of viewTaskFromMonth
