from prompt_toolkit import prompt
import sys
from controller.datamanager import DataManager
from enum import Enum

data_manager = DataManager.load_from_file();
ITEMS_PER_PAGE = 10;


class TaskMenuType(Enum):
    ALL = 0
    RUNNING = 1
    FINISHED = 2
    COMPLETED = 3


class ConsoleInterface:
    @staticmethod
    def console_init():
        input_is_correct = True
        while True:
            if input_is_correct:
                print("Main menu: ")
                print("1.All tasks\n2.Running tasks\n3.Finished tasks\n4.Completed tasks\n5.New task\n6.Exit")
            else:
                print("Your input was not correct, try again")
            answer = prompt('Enter your variant: ')
            input_is_correct = ConsoleInterface.__main_menu_redirect(answer)

    @staticmethod
    def __main_menu_redirect(value: int) -> bool:
        if value == '1':
            ConsoleInterface.__tasks_menu(TaskMenuType.ALL)
        elif value == '2':
            ConsoleInterface.__tasks_menu(TaskMenuType.RUNNING)
        elif value == '3':
            ConsoleInterface.__tasks_menu(TaskMenuType.FINISHED)
        elif value == '4':
            ConsoleInterface.__tasks_menu(TaskMenuType.COMPLETED)
        elif value == '5':
            ConsoleInterface.__new_task()
        elif value == '6':
            ConsoleInterface.__exit()
        else:
            return False
        return True

    @staticmethod
    def __tasks_menu(task_menu_type, search_query = "", page = 1):
        tasks = ConsoleInterface.__get_tasks(task_menu_type, search_query, page);
        ConsoleInterface.__print_tasks(tasks)
        print("1.Select page\n2.Search by name\n3.Select by id\n4.Exit to main menu");
        input_is_correct = True
        while not input_is_correct:
            answer = prompt('Enter your variant: ')
            input_is_correct = ConsoleInterface.__tasks_redirect(answer)
            print("Your input was not correct, try again")

    @staticmethod
    def __print_tasks(tasks):
        if tasks.length == 0:
            print("No tasks that match your query");
        for task in tasks:
            print("%d. %s, %s, %s, %s" % (task.task_id, task.name, task.date_start, task.date_end, task.is_completed))

    @staticmethod
    def __get_tasks(task_menu_type, search_query, page):
        if task_menu_type == TaskMenuType.ALL:
            return data_manager.get_all((page - 1) * ITEMS_PER_PAGE, ITEMS_PER_PAGE, search_query)

    @staticmethod
    def __tasks_redirect(value: int) -> bool:
        if value == '1':
            ConsoleInterface.__get_page()
        elif value == '2':
            ConsoleInterface.__get_query()
        elif value == '3':
            ConsoleInterface.__get_id()
        elif value == '4':
            pass
        else:
            return False
        return True


    @staticmethod
    def __new_task():
        print("Enter values for new task:")
        name = prompt('Enter the name: ');
        description = prompt('Enter the description: ');
        date = prompt('Enter the date of beginning: ');
        duration = prompt('Enter the duration: ');

    @staticmethod
    def __try_to_add_task():
        print("try")

    @staticmethod
    def __exit():
        sys.exit()
