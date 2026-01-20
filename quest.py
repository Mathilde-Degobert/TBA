
class Quest:

    """ This class represents a quest in the game. """

    def __init__(self, title, description, steps, is_main_quest=True, depends_on=None):
        self.title = title
        self.description = description
        self.steps = steps
        self.current_step = 0
        self.is_main_quest = is_main_quest
        self.depends_on = depends_on or []  # Liste des quêtes dont cette quête dépend
        self.completed_paths = []  # Track choix/chemins déjà complétés

    def advance(self):
        """ Advance to the next step in the quest. """
        if self.current_step < len(self.steps):
            self.current_step += 1

    def reset_to_step(self, step_num):
        """Reset quest to a specific step."""
        self.current_step = step_num

    def is_complete(self):
        """
        Check if the quest is complete.
        Returns:
            bool: True if the quest is complete, False otherwise.
        """
        # Si la quête a des dépendances, vérifier qu'elles sont toutes complétées
        if self.depends_on:
            return all(quest.is_complete() for quest in self.depends_on)
        # Sinon, vérifier les étapes
        return self.current_step >= len(self.steps)

    def get_current_step(self):
        """
        Get the current step of the quest.
        Returns:
            QuestStep: The current step of the quest.
        """
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None

class QuestStep:

    """ This class represents a step in a quest. """

    def __init__(self, description, character=None, item=None,
                 quest_responses=None, choices=None, correct_choices=None, reward_item=None):
        self.description = description
        self.character = character
        self.item = item
        self.quest_responses = quest_responses or []
        self.choices = choices or []
        self.correct_choices = correct_choices or []
        self.reward = reward_item
        self.current_substep = 0

    def reset_substep(self):
        """ Reset the substep to the beginning. """
        self.current_substep = 0

    def advance_substep(self):
        """ Advance to the next substep. """
        if self.current_substep < len(self.quest_responses) - 1:
            self.current_substep += 1
            return False
        return True

    def get_current_response(self):
        """ 
        Get the current quest response for this substep.
        Returns:
            str: The quest response for this substep.
        """
        if self.current_substep < len(self.quest_responses):
            return self.quest_responses[self.current_substep]
        return None

    def get_current_choices(self):
        """
        Get the current choices for this substep.
        Returns:
            list: The choices for this substep.
        """
        if self.current_substep < len(self.choices):
            return self.choices[self.current_substep]
        return None

    def get_current_correct_choices(self):
        """
        Get the current correct choices for this substep.
        Returns:
            list: The correct choices for this substep.
        """
        if self.current_substep < len(self.correct_choices):
            return self.correct_choices[self.current_substep]
        return None

