def multiple_choice_menu(prompt: str, options):
    print(prompt)
    if type(options) in (list, tuple):
        choices = options
    elif type(options) == dict:
        choices = tuple(options.keys())
    else:
        raise ValueError("Options should be tuple, list or dict")
    for i in range(len(choices)):
        print(f"{i + 1}. {choices[i]}")
    valid = False
    while not valid:
        choice = input()
        try:
            choice = int(choice)
            if len(choices) >= choice > 0:
                choice -= 1
                valid = True
                if type(options) == dict:
                    result = tuple(options.values())[choice]
                    if callable(result):
                        result()
                    else:
                        return result
                else:
                    return options[choice]
            else:
                raise ValueError()
        except ValueError:
            print("Please enter a valid number!")


def user_confirmation_dialog(prompt: str, automation: str = None) -> bool:
    choice = None
    while choice is None:
        if automation is None:
            user_input = input(prompt).strip().lower()
        else:
            user_input = automation
            automation = None
        if user_input.startswith("y"):
            choice = True
        elif user_input.startswith("n"):
            choice = False
    return choice

