# Project by:   Arellano, Von Michael
#               Lacson, John Russel
#               Punzalan, Kurt Brian Daine
# Description: This file contains the main loop which calls other functions from functions.py.

import os

import functions

os.system("clear")  # clears the terminal everytime user runs

while 1:
    functions.menuFunction()
    try:
        choice = int(input("Enter a number: "))
        if choice == 1:
            functions.addTask()
        elif choice == 2:
            functions.editTask()
        elif choice == 3:
            functions.deleteTask()
        elif choice == 4:
            functions.viewAllTask()
        elif choice == 5:
            functions.taskDone()
        elif choice == 6:
            functions.addCategory()
        elif choice == 7:
            functions.editCategory()
        elif choice == 8:
            functions.deleteCategory()
        elif choice == 9:
            functions.viewCategoryWithTasks()
        elif choice == 10:
            functions.addTaskToCategory()
        elif choice == 11:
            functions.viewTaskFromDay()
        elif choice == 12:
            functions.viewTaskFromMonth()
        elif choice == 0:
            print("Good bye!")
            break
        else:
            print("Invalid choice!")

    except ValueError:
        print("Invalid choice!")
