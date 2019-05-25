from prompt_toolkit import prompt


def console_init():
    answer = prompt('Give me some input: ')
    print('You said: %s' % answer)
