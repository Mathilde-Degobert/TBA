""" Define the Quest class"""

class Quest:
    """
    This class represents a quest in the game. A quest has a title, description,
    objectives, completion status, and optional rewards.
    """

    def __init__(self, title, description, objectives=None, character=None, dialogue=None, choices=None, correct_choices=None, reward=None):
        """
        Initialize a new quest.
        """
        self.title = title
        self.description = description
        self.objectives = objectives if objectives is not None else []
        self.character = character
        self.completed_objectives = []
        self.is_completed = False
        self.reward = reward
        self.selected_rewards = []  # For dialogue-based reward selection (list to track all chosen tools)
        self.reward_given = False
        
        # Create a DialogueStep if dialogue data is provided
        if dialogue or choices or correct_choices:
            self.dialogue_step = DialogueStep(
                description=description,
                dialogue=dialogue if dialogue is not None else [],
                choices=choices if choices is not None else [],
                correct_choices=correct_choices if correct_choices is not None else []
            )
        else:
            self.dialogue_step = None

    def get_current_step(self):
        return self.dialogue_step

    def advance(self):
        if self.dialogue_step:
            self.dialogue_step.advance_step()

    def is_complete(self):
        return self.is_completed

    def complete_objective(self, objective, player=None):
        if objective in self.objectives and objective not in self.completed_objectives:
            self.completed_objectives.append(objective)
            print(f"Objectif accompli: {objective}")
            if len(self.completed_objectives) == len(self.objectives):
                self.complete_quest(player)
            return True
        return False

    def complete_quest(self, player=None):
        if not self.is_completed:
            self.is_completed = True
            print(f"\nQuête {self.title} terminée !\n")
            if player:
                # Donner le reward principal
                if self.reward and not self.reward_given:
                    player.add_reward(self.reward)
                    self.reward_given = True
                # Donner tous les rewards issus du choix de dialogue s'ils existent
                for reward in self.selected_rewards:
                    player.add_reward(reward)
            print()

    def grant_reward(self, player=None):
        """Give the quest reward once and mark any matching reward objective."""
        if not self.reward or self.reward_given:
            return
        if player:
            player.add_reward(self.reward)
        self.reward_given = True
        self._mark_reward_objective(self.reward.name, player)

    def _mark_reward_objective(self, reward_name, player=None):
        reward_name = reward_name.lower()
        for objective in self.objectives:
            if reward_name in objective.lower() and objective not in self.completed_objectives:
                self.complete_objective(objective, player)
                break

    def get_status(self):
        if self.is_completed:
            return f"{self.title} (Terminée)"
        completed_count = len(self.completed_objectives)
        total_count = len(self.objectives)
        return f"{self.title} ({completed_count}/{total_count} objectifs)"

    def get_details(self, current_counts=None):
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
        if not current_counts:
            return objective
        for counter_name, current_count in current_counts.items():
            if counter_name not in objective:
                continue
            required = self._extract_number_from_text(objective)
            if required is not None:
                return f"{objective} (Progression: {current_count}/{required})"
        return objective

    def _extract_number_from_text(self, text):
        for word in text.split():
            if word.isdigit():
                return int(word)
        return None

    def matches_item_objective(self, item_name, objective):
        """Return True if an obtained item should satisfy the objective text.
        Works similarly to check_room_objective by checking against predefined patterns."""
        # Normaliser le nom de l'item
        item_norm = item_name.lower().replace("-", " ")
        item_orig = item_name.lower()
        
        # Créer les variations d'objectifs possibles pour cet item
        item_objectives = [
            f"Obtenir {item_name}",
            f"Obtenir le {item_name}",
            f"Obtenir la {item_name}",
            f"Obtenir les {item_name}",
            f"Obtenir l'{item_name}",
            f"Trouver {item_name}",
            f"Trouver le {item_name}",
            f"Trouver la {item_name}",
            f"Trouver les {item_name}",
            f"Trouver l'{item_name}",
            f"Récupérer {item_name}",
            f"Récupérer le {item_name}",
            f"Récupérer la {item_name}",
            f"Récupérer les {item_name}",
            f"Récupérer l'{item_name}",
            # Versions avec espaces au lieu de tirets
            f"Obtenir {item_norm}",
            f"Obtenir le {item_norm}",
            f"Obtenir la {item_norm}",
            f"Obtenir les {item_norm}",
            f"Obtenir l'{item_norm}",
            f"Trouver {item_norm}",
            f"Trouver le {item_norm}",
            f"Trouver la {item_norm}",
            f"Trouver les {item_norm}",
            f"Trouver l'{item_norm}",
            f"Récupérer {item_norm}",
            f"Récupérer le {item_norm}",
            f"Récupérer la {item_norm}",
            f"Récupérer les {item_norm}",
            f"Récupérer l'{item_norm}",
        ]
        
        # Normaliser l'objectif pour la comparaison (enlever tirets)
        objective_norm = objective.lower().replace("-", " ")
        
        # Vérifier si l'objectif correspond à l'une des variations
        for item_obj in item_objectives:
            item_obj_norm = item_obj.lower().replace("-", " ")
            if item_obj_norm == objective_norm:
                return True
        
        return False

    def check_room_objective(self, room_name, player=None):
        # Traductions des noms de pièces
        translations = {
            "forest": "forêt",
            "pont": "pont",
            "magasin": "magasin",
            "champs": "champs"
        }
        
        # Utiliser la traduction si disponible, sinon utiliser le nom original
        room_name_fr = translations.get(room_name.lower(), room_name)
        
        room_objectives = [
            f"Visiter {room_name}",
            f"Visiter le {room_name}",
            f"Visiter la {room_name}",
            f"Visiter {room_name_fr}",
            f"Visiter le {room_name_fr}",
            f"Visiter la {room_name_fr}",
            f"Explorer {room_name}",
            f"Explorer le {room_name}",
            f"Explorer la {room_name}",
            f"Explorer {room_name_fr}",
            f"Explorer le {room_name_fr}",
            f"Explorer la {room_name_fr}",
            f"Aller à {room_name}",
            f"Aller à l'{room_name}" if room_name.startswith("'") else f"Aller à l'{room_name}",
            f"Aller à {room_name_fr}",
            f"Aller à l'{room_name_fr}" if room_name_fr.startswith("'") else f"Aller à l'{room_name_fr}",
            f"Entrer dans la {room_name}",
            f"Entrer dans le {room_name}",
            f"Entrer dans la {room_name_fr}",
            f"Entrer dans le {room_name_fr}",
            f"Aller dans les {room_name}",
            f"Aller dans les {room_name_fr}",
            f"Entrer dans {room_name}",
            f"Entrer dans {room_name_fr}",
            f"Se rendre à {room_name}",
            f"Se rendre à {room_name_fr}",
        ]
        for objective in room_objectives:
            if self.complete_objective(objective, player):
                return True
        return False

    def check_action_objective(self, action, target=None, player=None):
        if target:
            # Normaliser le target pour les comparaisons (enlever tirets, etc.)
            target_normalized = target.replace("-", " ")
            objective_variations = [
                f"{action} {target}",
                f"{action} avec {target}",
                f"{action} à {target}",
                f"{action} la {target}",
                f"{action} le {target}",
                f"{action} un {target}"
            ]
            # Vérifier d'abord les variations exactes
            for objective in objective_variations:
                if self.complete_objective(objective, player):
                    return True
            # Vérifier si l'objectif contient l'action et des mots-clés du target
            for objective in self.objectives:
                if objective in self.completed_objectives:
                    continue
                obj_lower = objective.lower()
                if action.lower() in obj_lower:
                    # Vérifier si les mots du target apparaissent dans l'objectif
                    target_words = [w for w in target_normalized.lower().split() if len(w) > 2]
                    if all(word in obj_lower for word in target_words):
                        if self.complete_objective(objective, player):
                            return True
        else:
            objective_variations = [action]
            for objective in objective_variations:
                if self.complete_objective(objective, player):
                    return True
        return False

    def check_dialogue_choice_objective(self, choice_text, player=None):
        """
        Check if making a dialogue choice completes an objective.
        Matches the choice text against objectives (e.g., "Aider le" matches "Puis-je vous aider ?")
        
        Args:
            choice_text (str): The dialogue choice made by the player.
            player: The player object (optional).
            
        Returns:
            bool: True if an objective was completed, False otherwise.
        """
        # Try to find keywords from objectives in the choice text
        for objective in self.objectives:
            # Extract action keywords from objective (e.g., "Aider" from "Aider le")
            keywords = objective.lower().split()
            # Check if any keyword appears in the choice
            if any(keyword in choice_text.lower() for keyword in keywords):
                if self.complete_objective(objective, player):
                    return True
        return False

    def __str__(self):
        return self.get_status()


class QuestManager:
    """This class manages all quests in the game."""

    def __init__(self, player=None):
        self.quests = []
        self.player = player

    def add_quest(self, quest):
        self.quests.append(quest)

    def complete_objective(self, objective_text):
        for quest in self.quests:
            if quest.complete_objective(objective_text):
                # Ne pas retirer les quêtes complétées, les garder pour consultation
                return True
        return False

    def check_room_objectives(self, room_name):
        for quest in self.quests[:]:
            quest.check_room_objective(room_name, self.player)
            # Ne pas retirer les quêtes complétées

    def check_action_objectives(self, action, target=None):
        for quest in self.quests[:]:
            quest.check_action_objective(action, target, self.player)
            # Ne pas retirer les quêtes complétées

    def check_item_objectives(self, item_name):
        for quest in self.quests[:]:
            for objective in quest.objectives:
                if objective in quest.completed_objectives:
                    continue
                if quest.matches_item_objective(item_name, objective):
                    quest.complete_objective(objective, self.player)
                    # Ne pas retirer les quêtes complétées, les garder pour consultation
                    break

    def get_all_quests(self):
        return self.quests

    def get_quest_by_title(self, title):
        for quest in self.quests:
            if quest.title == title:
                return quest
        return None

    def show_quests(self):
        # Afficher toutes les quêtes (actives et complétées)
        if not self.quests:
            print("\nAucune quête disponible.\n")
            return
        print("\nListe des quêtes:")
        for quest in self.quests:
            print(f"{quest.get_status()}")
        print()

    def show_quest_details(self, quest_identifier):
        quest = None
        # D'abord essayer de chercher par titre (même pour les chiffres comme "1 - titre")
        # En cherchant les quêtes qui commencent par ce chiffre
        if quest_identifier.isdigit():
            # Chercher une quête dont le titre commence par ce chiffre
            for q in self.quests:
                if q.title.startswith(quest_identifier):
                    quest = q
                    break
            # Si pas trouvée, essayer l'ancienne méthode d'index
            if not quest:
                quest_index = int(quest_identifier) - 1
                if 0 <= quest_index < len(self.quests):
                    quest = self.quests[quest_index]
        else:
            # Chercher par titre exact ou partiel
            quest = self.get_quest_by_title(quest_identifier)
        if quest:
            print(quest.get_details())
        else:
            print(f"\nQuête '{quest_identifier}' non trouvée.\n")


class DialogueStep:
    """This class represents a step in a dialogue."""

    def __init__(self, description, dialogue=None, choices=None, correct_choices=None, item=None, reward_item=None):
        self.description = description
        self.dialogue = dialogue if dialogue is not None else []
        self.choices = choices if choices is not None else []
        self.correct_choices = correct_choices if correct_choices is not None else []
        self.item = item
        self.reward_item = reward_item
        self.current_step = 0
        self.player_choice = None  # Stocker le dernier choix du joueur

    def advance_step(self):
        if self.current_step < len(self.dialogue) - 1:
            self.current_step += 1
            return False
        return True

    def set_step(self, step):
        """Définir directement une étape spécifique (pour les branches de dialogue)."""
        if 0 <= step < len(self.dialogue):
            self.current_step = step

    def reset_step(self):
        self.current_step = 0
        self.player_choice = None

    def set_player_choice(self, choice):
        """Enregistrer le choix du joueur pour utiliser dans les conditions."""
        self.player_choice = choice

    def get_current_response(self):
        if self.current_step < len(self.dialogue):
            dialogue_item = self.dialogue[self.current_step]
            # Gérer les dialogues avec conditions (tuples) ou simples (strings)
            if isinstance(dialogue_item, tuple):
                text, condition = dialogue_item
                # Vérifier la condition
                if condition is None or self.player_choice == condition:
                    return text
                else:
                    # Condition non remplie, sauter cette étape
                    return None
            else:
                # Simple string sans condition
                return dialogue_item
        return None

    def get_current_choices(self):
        if self.current_step < len(self.choices):
            return self.choices[self.current_step]
        return None

    def get_current_correct_choices(self):
        if self.current_step < len(self.correct_choices):
            return self.correct_choices[self.current_step]
        return None
