""" Define the Quest class"""

class Quest:
    """
    This class represents a quest in the game. A quest has a title, description,
    objectives, completion status, and optional rewards.
    
    Attributes:
        title (str): The title of the quest.
        description (str): The description of the quest.
        objectives (list): List of objectives to complete.
        is_completed (bool): Whether the quest is completed.
        is_active (bool): Whether the quest is currently active.
        reward (str): Optional reward for completing the quest.
    """


    def __init__(self, title, description, objectives=None, reward=None, character=None, dialogue_step=None):
        """
        Initialize a new quest.
        
        Args:
            title (str): The title of the quest.
            description (str): The description of the quest.
            objectives (list): List of objectives (default: empty list).
            reward (Item): The reward item (default: None).
            character (str): The character associated with this quest (default: None).
            dialogue (list): List of dialogue strings (default: empty list).
            choices (list): List of available choices (default: empty list).
            correct_choices (list): List of correct choices (default: empty list).
        """
        self.title = title
        self.description = description
        self.objectives = objectives if objectives is not None else []
        self.character = character
        self.dialogue_step = dialogue_step
        self.completed_objectives = []
        self.is_completed = False
        self.reward = reward

    def complete_objective(self, objective, player=None):
        """
        Mark an objective as completed.
        
        Args:
            objective (str): The objective to mark as completed.
            player: The player object (optional).
            
        Returns:
            bool: True if objective was found and completed, False otherwise.
        """
        if objective in self.objectives and objective not in self.completed_objectives:
            self.completed_objectives.append(objective)
            print(f"Objectif accompli: {objective}")

            # Check if all objectives are completed
            if len(self.completed_objectives) == len(self.objectives):
                self.complete_quest(player)

            return True
        return False


    def complete_quest(self, player=None):
        """
        Mark the quest as completed and give reward to player.
        
        Args:
            player: The player object to give the reward to (optional).
        """
        if not self.is_completed:
            self.is_completed = True
            print(f"\nQuête {self.title} terminée !\n")
            if self.reward:
                if self.reward:
                    player.add_reward(self.reward)
            print()


    def get_status(self):
        """
        Get the current status of the quest.
        
        Returns:
            str: A formatted string showing the quest status.
        """
        if self.is_completed:
            return f"{self.title} (Terminée)"
        completed_count = len(self.completed_objectives)
        total_count = len(self.objectives)
        return f"{self.title} ({completed_count}/{total_count} objectifs)"


    def get_details(self, current_counts=None):
        """
        Get detailed information about the quest.
        
        Args:
            current_counts (dict): Optional dictionary with current counter values 
                                   (e.g., {"Se déplacer": 5})
        
        Returns:
            str: A formatted string with quest details.
        """
        details = f"\nQuête: {self.title}\n"
        details += f"{self.description}\n"

        if self.objectives:
            details += "\nObjectifs:\n"
            for objective in self.objectives:
                status = "✅" if objective in self.completed_objectives else "⬜"
                objective_text = self._format_objective_with_progress(objective, current_counts)
                details += f"  {status} {objective_text}\n"

        if self.reward:
            details += f"\nRécompense = {self.reward}\n"

        return details

    def _format_objective_with_progress(self, objective, current_counts):
        """
        Format an objective with progress information if available.
        
        Args:
            objective (str): The objective text.
            current_counts (dict): Dictionary with current counter values.
            
        Returns:
            str: Formatted objective text with progress if applicable.
        """
        if not current_counts:
            return objective

        for counter_name, current_count in current_counts.items():
            if counter_name not in objective:
                continue

            # Extract required count from objective
            required = self._extract_number_from_text(objective)
            if required is not None:
                return f"{objective} (Progression: {current_count}/{required})"

        return objective

    def _extract_number_from_text(self, text):
        """
        Extract the first number from a text string.
        
        Args:
            text (str): The text to search.
            
        Returns:
            int: The first number found, or None if no number exists.
        """
        for word in text.split():
            if word.isdigit():
                return int(word)
        return None


    def check_room_objective(self, room_name, player=None):
        """
        Check if visiting a specific room completes an objective.
        
        Args:
            room_name (str): The name of the room visited.
            player: The player object (optional).
            
        Returns:
            bool: True if an objective was completed, False otherwise.
        """
        room_objectives = [
            f"Visiter {room_name}",
            f"Explorer {room_name}",
            f"Aller à {room_name}",
            f"Entrer dans la {room_name}",
            f"Entrer dans {room_name}",
            f"Se rendre à {room_name}"
        ]

        for objective in room_objectives:
            if self.complete_objective(objective, player):
                return True
        return False


    def check_action_objective(self, action, target=None, player=None):
        """
        Check if performing an action completes an objective.
        
        Args:
            action (str): The action performed (e.g., "parler", "prendre", "utiliser").
            target (str): Optional target of the action.
            player: The player object (optional).
            
        Returns:
            bool: True if an objective was completed, False otherwise.
        """
        if target:
            objective_variations = [
                f"{action} {target}",
                f"{action} avec {target}",
                f"{action} à {target}",
                f"{action} la {target}",
                f"{action} le {target}",
                f"{action} un {target}"
            ]
        else:
            objective_variations = [action]

        for objective in objective_variations:
            if self.complete_objective(objective, player):
                return True
        return False

    def __str__(self):
        """
        Return a string representation of the quest.
        """
        return self.get_status()


class QuestManager:
    """
    This class manages all quests in the game.
    
    Attributes:
        quests (list): List of all quests in the game.
        active_quests (list): List of currently active quests.
        player: Reference to the player object.
    """

    def __init__(self, player=None):
        """
        Initialize the quest manager.
        
        Args:
            player: The player object (optional, can be set later).
            
        Examples:
        
        >>> manager = QuestManager()
        >>> len(manager.quests)
        0
        >>> len(manager.active_quests)
        0
        """
        self.quests = []
        self.player = player

    def add_quest(self, quest):
        """
        Add a quest to the game.
        
        Args:
            quest (Quest): The quest to add.
        """
        self.quests.append(quest)

    def complete_objective(self, objective_text):
        """
        Complete an objective in any active quest.
        
        Args:
            objective_text (str): The objective to complete.
            
        Returns:
            bool: True if objective was found and completed, False otherwise.
        """
        for quest in self.quests:
            if quest.complete_objective(objective_text):
                # Remove completed quests
                if quest.is_completed:
                    self.quests.remove(quest)
                return True
        return False

    def check_room_objectives(self, room_name):
        """
        Check all active quests for room-related objectives.
        
        Args:
            room_name (str): The name of the room visited.
        """
        for quest in self.quests[:]:  # Use slice to avoid modification during iteration
            quest.check_room_objective(room_name, self.player)
            if quest.is_completed:
                self.quests.remove(quest)

    def check_action_objectives(self, action, target=None):
        """
        Check all active quests for action-related objectives.
        
        Args:
            action (str): The action performed.
            target (str): Optional target of the action.
        """
        for quest in self.quests[:]:
            quest.check_action_objective(action, target, self.player)
            if quest.is_completed:
                self.quests.remove(quest)

    def get_all_quests(self):
        """
        Get all quests.
        
        Returns:
            list: List of all quests.
        """
        return self.quests

    def get_quest_by_title(self, title):
        """
        Get a quest by its title.
        
        Args:
            title (str): The title of the quest.
            
        Returns:
            Quest: The quest if found, None otherwise.
        """
        for quest in self.quests:
            if quest.title == title:
                return quest
        return None

    def show_quests(self):
        """
        Display all quests and their status.
        """
        if not self.quests:
            print("\nAucune quête disponible.\n")
            return

        print("\nListe des quêtes:")
        for quest in self.quests:
            print(f"{quest.get_status()}")
        print()

    def show_quest_details(self, quest_identifier):
        """
        Show detailed information about a specific quest.
        
        Args:
            quest_identifier (str): The number of the quest.
        """
        quest = None
        # Check if identifier is a number
        if quest_identifier.isdigit():
            quest_index = int(quest_identifier) - 1  # Convert to 0-based index
            if 0 <= quest_index < len(self.quests):
                quest = self.quests[quest_index]
        else:
            # Otherwise, search by title
            quest = self.get_quest_by_title(quest_identifier)

        if quest:
            print(quest.get_details())
        else:
            print(f"\nQuête '{quest_identifier}' non trouvée.\n")

class DialogueStep:
    """ This class represents a step in a dialogue. """
    def __init__(self, description, dialogue=None, choices=None, correct_choices=None, item=None, reward_item=None):
        
        self.description = description
        self.dialogue = dialogue if dialogue is not None else []
        self.choices = choices if choices is not None else []
        self.correct_choices = correct_choices if correct_choices is not None else []
        self.item = item
        self.reward_item = reward_item
        self.current_step = 0

    def advance_step(self):
        """ Advance to the next substep. """
        if self.current_step < len(self.dialogue) - 1:
            self.current_step += 1
            return False
        return True

    def reset_step(self):
        """ Reset the substep to the beginning. """
        self.current_step = 0

    def get_current_response(self):
        """ 
        Get the current special response for this substep.
        Returns:
            str: The special response for this substep.
        """
        if self.current_step < len(self.dialogue):
            return self.dialogue[self.current_step]
        return None

    def get_current_choices(self):
        """
        Get the current choices for this substep.
        Returns:
            list: The choices for this substep.
        """
        if self.current_step < len(self.choices):
            return self.choices[self.current_step]
        return None

    def get_current_correct_choices(self):
        """
        Get the current correct choices for this substep.
        Returns:
            list: The correct choices for this substep.
        """
        if self.current_step < len(self.correct_choices):
            return self.correct_choices[self.current_step]
        return None