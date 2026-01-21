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


    def __init__(self, title, description, objectives=None, reward=None):
        """
        Initialize a new quest.
        
        Args:
            title (str): The title of the quest.
            description (str): The description of the quest.
            objectives (list): List of objectives (default: empty list).
            reward (str): Optional reward description.
        """
        self.title = title
        self.description = description
        self.objectives = objectives if objectives is not None else []
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
            print(f"\nQuête terminée: {self.title}")
            if self.reward:
                print(f"Récompense: {self.reward}")
                if player:
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
            details += f"\nRécompense: {self.reward}\n"

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
            
        Examples:
        
        >>> quest = Quest("Explore", "Explore the castle", ["Visiter Castle"])
        >>> quest.check_room_objective("Castle")
        ✅ Objectif accompli: Visiter Castle
        <BLANKLINE>
        🏆 Quête terminée: Explore
        <BLANKLINE>
        True
        >>> quest.check_room_objective("Tower")
        False
        """
        room_objectives = [
            f"Visiter {room_name}",
            f"Explorer {room_name}",
            f"Aller à {room_name}",
            f"Entrer dans {room_name}"
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
            
        Examples:
        
        >>> quest = Quest("Talk", "Have a conversation", ["parler avec garde"])
        >>> quest.check_action_objective("parler", "garde") # doctest: +NORMALIZE_WHITESPACE
        ✅ Objectif accompli: parler avec garde
        <BLANKLINE>
        🏆 Quête terminée: Talk
        <BLANKLINE>
        True
        >>> quest.check_action_objective("courir", "vite")
        False
        """
        if target:
            objective_variations = [
                f"{action} {target}",
                f"{action} avec {target}",
                f"{action} à {target}",
                f"{action} la {target}"
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


    def show_quest_details(self, quest_title, current_counts=None):
        """
        Show detailed information about a specific quest.
        
        Args:
            quest_title (str): The title of the quest.
            current_counts (dict): Optional dictionary with current counter values.
        """
        quest = self.get_quest_by_title(quest_title)
        if quest:
            print(quest.get_details(current_counts))
        else:
            print(f"\nQuête '{quest_title}' non trouvée.\n")
