from prompt_toolkit import prompt
import sys
import math
from controller.datamanager import DataManager
from enum import Enum
from model.task_status import TaskStatus
from config.config import clear, storage_path
from model.task import Task
import datetime
from termcolor import colored

TASKS_ON_PAGE = 10


class TaskMenuType(Enum):
    ALL = 0
    UNCOMPLETED = 1
    COMPLETED = 3


class ConsoleInterface:
    def __init__(self):
        self.data_manager = DataManager.load_from_file(storage_path)

    def console_init(self):
        input_is_correct = True
        while True:
            clear()
            if input_is_correct:
                print("Main menu:\n1.All tasks\n2.Not completed tasks\n3.Completed tasks\n4.New task\n5.Exit")
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
            self.__change_or_add_task()
        elif value == '5':
            self.__exit()
        else:
            return False
        return True

    def __tasks_menu(self, task_menu_type, search_query=None, page=1):
        clear()
        response = self.__get_tasks(task_menu_type, search_query, page)
        all_pages = ConsoleInterface.__get_all_pages(response.count_all)
        ConsoleInterface.__print_tasks(response.tasks, page, all_pages)
        print("Tasks menu:\n1.Select page\n2.Search by name\n3.Select by id\n4.Exit to main menu")
        input_is_correct = False
        while not input_is_correct:
            answer = prompt('Enter your variant: ')
            input_is_correct = self.__tasks_menu_redirect(answer, task_menu_type, all_pages, search_query)
            if not input_is_correct:
                print("Your input was not correct, try again")

    @staticmethod
    def __get_all_pages(count_all):
        all_pages = math.ceil(count_all / TASKS_ON_PAGE)
        if all_pages == 0:
            return 1
        else:
            return all_pages

    @staticmethod
    def __number_is_valid(number):
        try:
            int(number)
            return True
        except ValueError:
            return False

    @staticmethod
    def __print_tasks(tasks, page, all_pages):
        if len(tasks) == 0:
            print("No tasks that match your query")
        else:
            for task in tasks:
                color = ConsoleInterface.__choose_color(task)
                print(colored("%d. %s | %s | %s | %s" %
                              (task.task_id, task.name, task.date_start, task.date_end, task.is_completed), color))
            print("Page %d of %d" % (page, all_pages))

    @staticmethod
    def __choose_color(task: Task):
        if task.is_running():
            return "green"
        elif task.is_finished():
            return "red"
        else:
            return "yellow"

    def __get_tasks(self, task_menu_type, search_query, page):
        offset = (page - 1) * TASKS_ON_PAGE
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
        page = None
        while not input_is_correct:
            page = prompt("Enter your page: ")
            input_is_correct = ConsoleInterface.__number_is_valid(page) and all_pages >= int(page) > 0
            if not input_is_correct:
                print("Your page is not correct, try again")
        self.__tasks_menu(menu_type, search_query, int(page))

    def __tasks_menu_change_query(self, menu_type):
        query = prompt("Enter your query: ")
        if len(query) > 0:
            self.__tasks_menu(menu_type, query)

    def __task_id_redirect(self):
        input_is_correct = False
        task_id = None
        while not input_is_correct:
            task_id = prompt("Enter id: ")
            input_is_correct = ConsoleInterface.__number_is_valid(task_id)
            if not input_is_correct:
                print("Your id is not correct, try again")
        task = self.data_manager.get_by_id(int(task_id))
        if task:
            self.__task_menu(task)

    def __task_menu(self, task):
        clear()
        ConsoleInterface.__print_task(task)
        print("Task menu:\n1.Change task\n2.Set completed/uncompleted\n3.Delete task\n4.Exit to main menu")
        input_is_correct = False
        while not input_is_correct:
            answer = prompt('Enter your variant: ')
            input_is_correct = self.__task_menu_redirect(answer, task)
            if not input_is_correct:
                print("Your input was not correct, try again")

    def __task_menu_redirect(self, value: int, task) -> bool:
        if value == '1':
            self.__change_or_add_task(task)
        elif value == '2':
            self.__set_task_completeness(task)
        elif value == '3':
            self.__delete_task(task)
        elif value == '4':
            pass
        else:
            return False
        return True

    def __change_or_add_task(self, task=None):
        input_is_correct = False
        while not input_is_correct:
            print("Enter values for task:")
            name = prompt('Enter the name: ')
            description = prompt('Enter the description: ')
            date = prompt('Enter the date of beginning: ')
            duration = prompt('Enter the duration (hh:mm:ss): ')
            input_is_correct = self.__try_to_add_or_change_task(name, description, date, duration, task)
            if not input_is_correct:
                print("Your input was not valid, try again")

    def __set_task_completeness(self, task: Task):
        self.data_manager.change_task_status(task.task_id, not task.is_completed)

    def __delete_task(self, task: Task):
        self.data_manager.delete_task(task.task_id)

    @staticmethod
    def __print_task(task: Task):
        print("Id: %d" % task.task_id)
        print("Name: %s" % task.name)
        print("Description: %s" % task.description)
        print("Start date: %s" % task.date_start)
        print("End date: %s" % task.date_end)
        print("Is completed: %s" % task.is_completed)

    def __try_to_add_or_change_task(self, name, description, date, duration, task):
        h, m, s = duration.split(':')
        if(not ConsoleInterface.__number_is_valid(h) or
            not ConsoleInterface.__number_is_valid(m) or
                not ConsoleInterface.__number_is_valid(s)):
            return False
        seconds_duration = (int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds()))
        if task is not None:
            self.data_manager.update_task_info(task.task_id, name, description, date, seconds_duration)
        else:
            self.data_manager.create_task(name, description, date, seconds_duration)
        return True

    @staticmethod
    def __exit():
        sys.exit()
