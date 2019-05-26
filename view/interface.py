from prompt_toolkit import prompt
import sys
import math
from controller.datamanager import DataManager
from enum import Enum
from model.task_status import TaskStatus

TASKS_ON_PAGE = 10


class TaskMenuType(Enum):
    ALL = 0
    UNCOMPLETED = 1
    COMPLETED = 3


class ConsoleInterface:
    def __init__(self):
        self.data_manager = DataManager.load_from_file()

    def console_init(self):
        input_is_correct = True
        while True:
            if input_is_correct:
                print("Main menu: ")
                print("1.All tasks\n2.Not completed tasks\n3.Completed tasks\n4.New task\n5.Exit")
            else:
                print("Your input was not correct, try again")
            answer = prompt('Enter your variant: ')
            input_is_correct = self.__main_menu_redirect(answer)

    def __main_menu_redirect(self, value: int) -> bool:
        if value == '1':
            self.__tasks_menu(TaskMenuType.ALL)
        elif value == '2':
            self.__tasks_menu(TaskMenuType.UNCOMPLETED)
        elif value == '3':
            self.__tasks_menu(TaskMenuType.COMPLETED)
        elif value == '4':
            self.__new_task()
        elif value == '5':
            self.__exit()
        else:
            return False
        return True

    def __tasks_menu(self, task_menu_type, search_query=None, page=1):
        response = self.__get_tasks(task_menu_type, search_query, page)
        all_pages = math.ceil(response.count_all/TASKS_ON_PAGE)
        ConsoleInterface.__print_tasks(response.tasks, page, all_pages)
        print("1.Select page\n2.Search by name\n3.Select by id\n4.Exit to main menu")
        input_is_correct = False
        while not input_is_correct:
            answer = prompt('Enter your variant: ')
            input_is_correct = self.__tasks_menu_redirect(answer, task_menu_type, all_pages, search_query)
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

    def __get_tasks(self, task_menu_type, search_query, page):
        offset = (page - 1) * TASKS_ON_PAGE;
        if task_menu_type == TaskMenuType.ALL:
            return self.data_manager.get_all(offset, TASKS_ON_PAGE, search_query)
        elif task_menu_type == TaskMenuType.UNCOMPLETED:
            return self.data_manager.get_with_status(TaskStatus.UNCOMPLETED, offset, TASKS_ON_PAGE, search_query)
        else:
            return self.data_manager.get_with_status(TaskStatus.COMPLETED, offset, TASKS_ON_PAGE, search_query)

    def __tasks_menu_redirect(self, value: int, menu_type, all_pages, search_query=None) -> bool:
        if value == '1':
            self.__tasks_menu_change_page(search_query, menu_type, all_pages)
        elif value == '2':
            self.__tasks_menu_change_query(menu_type)
        elif value == '3':
            self.__task_id_redirect()
        elif value == '4':
            pass
        else:
            return False
        return True

    def __tasks_menu_change_page(self, search_query, menu_type, all_pages):
        input_is_correct = False
        while not input_is_correct:
            page = prompt("Enter your page: ")
            try:
                input_is_correct = all_pages >= int(page) >= 0
            except ValueError:
                input_is_correct = False
            if not input_is_correct:
                print("Your page is not correct, try again")
        self.__tasks_menu(menu_type, search_query, int(page))

    def __tasks_menu_change_query(self, menu_type):
        query = prompt("Enter your query: ")
        if len(query) > 0:
            self.__tasks_menu(menu_type, query)

    def __task_id_redirect(self, menu_type):
        print("not yet done");

    def __new_task(self):
        print("Enter values for new task:")
        name = prompt('Enter the name: ')
        description = prompt('Enter the description: ')
        date = prompt('Enter the date of beginning: ')
        duration = prompt('Enter the duration: ')

    def __try_to_add_task(self):
        print("try")

    @staticmethod
    def __exit():
        sys.exit()
