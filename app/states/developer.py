from aiogram.fsm.state import State, StatesGroup


class DeveloperProjectState(StatesGroup):

    waiting_for_action = State()

    waiting_for_github = State()

    waiting_for_comment = State()

    waiting_for_archive = State()

    waiting_for_message = State()

    waiting_for_deadline = State()

    waiting_for_priority = State()

    waiting_for_estimate = State()



class SubmitProjectStates(StatesGroup):

    waiting_for_project = State()

    waiting_for_github = State()

    waiting_for_file = State()

    waiting_for_zip = State()

    waiting_for_comment = State()

    waiting_for_description = State()

    waiting_for_link = State()