from prompt_toolkit import prompt
import sys
import math
from controller.datamanager import DataManager
from enum import Enum
from model.task_status import TaskStatus

data_manager = DataManager.load_from_file();
TASKS_ON_PAGE = 10;


class TaskMenuType(Enum):
    ALL = 0
    UNCOMPLETED = 1
    COMPLETED = 3


class ConsoleInterface:
    @staticmethod
    def console_init():
        input_is_correct = True
        while True:
            if input_is_correct:
                print("Main menu: ")
                print("1.All tasks\n2.Not completed tasks\n3.3.Completed tasks\n4.New task\n5.Exit")
            else:
                print("Your input was not correct, try again")
            answer = prompt('Enter your variant: ')
            input_is_correct = ConsoleInterface.__main_menu_redirect(answer)

    @staticmethod
    def __main_menu_redirect(value: int) -> bool:
        if value == '1':
            ConsoleInterface.__tasks_menu(TaskMenuType.ALL)
        elif value == '2':
            ConsoleInterface.__tasks_menu(TaskMenuType.NOT_COMPLETED)
        elif value == '3':
            ConsoleInterface.__tasks_menu(TaskMenuType.COMPLETED)
        elif value == '4':
            ConsoleInterface.__new_task()
        elif value == '5':
            ConsoleInterface.__exit()
        else:
            return False
        return True

    @staticmethod
    def __tasks_menu(task_menu_type, search_query=None, page=1):
        response = ConsoleInterface.__get_tasks(task_menu_type, search_query, page)
        all_pages = math.ceil(response.count_all/TASKS_ON_PAGE)
        ConsoleInterface.__print_tasks(response.tasks, page, all_pages)
        print("1.Select page\n2.Search by name\n3.Select by id\n4.Exit to main menu")
        input_is_correct = False
        while not input_is_correct:
            answer = prompt('Enter your variant: ')
            input_is_correct = ConsoleInterface.__tasks_redirect(answer, task_menu_type, all_pages, search_query)
            if not input_is_correct:
                print("Your input was not correct, try again")

    @staticmethod
    def __print_tasks(tasks, page, all_pages):
        if len(tasks) == 0:
            print("No tasks that match your query")
        else:
            for task in tasks:
                print("%d. %s, %s, %s, %s" %
                      (task.task_id, task.name, task.date_start, task.date_end, task.is_completed))
            print("Page %d of %d" % (page, all_pages))

    @staticmethod
    def __get_tasks(task_menu_type, search_query, page):
        offset = (page - 1) * TASKS_ON_PAGE;
        if task_menu_type == TaskMenuType.ALL:
            return data_manager.get_all(offset, TASKS_ON_PAGE, search_query)
        elif task_menu_type == TaskMenuType.UNCOMPLETED:
            return data_manager.get_with_status(TaskStatus.UNCOMPLETED, offset, TASKS_ON_PAGE, search_query)
        else:
            return data_manager.get_with_status(TaskStatus.COMPLETED, offset, TASKS_ON_PAGE, search_query)

    @staticmethod
    def __tasks_redirect(value: int, menu_type, all_pages, search_query=None) -> bool:
        if value == '1':
            ConsoleInterface.__page_redirect(search_query, menu_type, all_pages)
        elif value == '2':
            ConsoleInterface.__query_redirect(menu_type)
        elif value == '3':
            ConsoleInterface.__input_id()
        elif value == '4':
            pass
        else:
            return False
        return True

    @staticmethod
    def __page_redirect(search_query, menu_type, all_pages):
        input_is_correct = False
        while not input_is_correct:
            page = prompt("Enter your page: ")
            input_is_correct = all_pages >= page >= 0
            if not input_is_correct:
                print("Your page is not correct, try again")
        ConsoleInterface.__tasks_menu(menu_type, search_query, page)

    @staticmethod
    def __query_redirect(menu_type):
        query = prompt("Enter your query: ")
        if len(query) > 0:
            ConsoleInterface.__tasks_menu(menu_type, query)

    @staticmethod
    def __new_task():
        print("Enter values for new task:")
        name = prompt('Enter the name: ')
        description = prompt('Enter the description: ')
        date = prompt('Enter the date of beginning: ')
        duration = prompt('Enter the duration: ')

    @staticmethod
    def __try_to_add_task():
        print("try")

    @staticmethod
    def __exit():
        sys.exit()
