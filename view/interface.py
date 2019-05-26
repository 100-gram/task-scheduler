from prompt_toolkit import prompt
import sys
from controller.datamanager import DataManager

data_manager = DataManager.load_from_file()


class ConsoleInterface:
    @staticmethod
    def console_init():
        input_is_correct = True
        while True:
            if input_is_correct:
                print("Main menu: ")
                print("1. All tasks\n2.Current tasks\n3.Finished tasks\n4.New task\n5.Exit")
            else:
                print("Your input was not correct, try again")
            answer = prompt('Enter your variant: ')
            input_is_correct = ConsoleInterface.__main_menu_redirect(answer)

    @staticmethod
    def __main_menu_redirect(value: int) -> bool:
        if value == '1':
            ConsoleInterface.__all_tasks()
        elif value == '2':
            ConsoleInterface.__current_tasks()
        elif value == '3':
            ConsoleInterface.__finished_tasks()
        elif value == '4':
            ConsoleInterface.__new_task()
        elif value == '5':
            ConsoleInterface.__exit()
        else:
            return False
        return True

    @staticmethod
    def __all_tasks():
        for task in data_manager.get_all():
            print("%d. %s, %s, %s, %s" % (task.task_id, task.name, task.date_start, task.date_end, task.is_completed))
        print("Select one task by typing its number of press 0 to exit back: ");
        answer = prompt('Enter your variant: ');

    @staticmethod
    def __current_tasks():
        print("2")

    @staticmethod
    def __finished_tasks():
        print("3")

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
