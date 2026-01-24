# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """

        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
            
            """
            Handle quests in the game.
            Args:
                game (Game): The game object.
                list_of_words (list): The list of words in the command.
                number_of_parameters (int): The number of parameters expected by the command.
            Returns:
                bool: True if the command was executed successfully, False otherwise.
            """
            ...
        directions = {"NORD": "N" , "N":"N" , "SUD":"S" , "S": "S" , "OUEST":"O" , "O":"O",
                       "EST":"E" , "E":"E" , "UP": "U" , "U":"U" , "DOWN":"D" , "D":"D"}

        # Get the direction from the list of words.
        direction = list_of_words[1].upper()
        if direction in directions:
            direction = directions[direction]
            # Move the player in the direction specified by the parameter.
            player.move(direction)
        else:
            print("\nDirection", direction,"non reconnue")
        return True

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    def history(game, list_of_words, number_of_parameters):
        """
        gets the history of rooms visited by the player.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            str: The list of places visited by the player.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        player = game.player
        player.get_history()
        return True

    def go_back(game, list_of_words, number_of_parameters):
        """
        goes back to the last place visited by the player.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            str: The list of places visited by the player.
        """

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        player = game.player

        # If there is no history, print an error message and return False.
        if not player.history:
            print("\nVous n'avez pas de pièce précédente à laquelle revenir !\n")
            return False
        
        # Set the current room to the last room in the history.
        player.current_room = player.history.pop()
        print(player.current_room.get_long_description())
        player.get_history()
        return True

    def look(game, list_of_words, number_of_parameters):
        """
        looks around the current room.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            str: The description of the current room.
        """

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        player = game.player
        print(player.current_room.get_long_description())
        # Show items in the room
        player.current_room.get_inventory()
        # Show characters (PNJ) present in the same room
        if player.current_room.characters:
            print("\nPersonnes présentes :")
            for character_name, character in player.current_room.characters.items():
                print(f"- {character.name} : {character.description}")
        return True

    def take(game, list_of_words, number_of_parameters):
        """
        takes an item from the current room and adds it to the player's inventory.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the item was taken successfully, False otherwise.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        player = game.player
        item_name = list_of_words[1].lower()

        # Check if the item is in the current room.
        if item_name not in player.current_room.items:
            print(f"\nL'objet '{item_name}' n'est pas dans la pièce.\n")
            return False
        
        # Chercher une quête liée à cet item
        quest_for_item = None
        for quest in game.quests:
            if not quest.is_complete():
                current_step = quest.get_current_step()
                if current_step and current_step.reward and current_step.reward.name == item_name:
                    quest_for_item = quest
                    break
        
        # Si une quête est liée à cet item, afficher l'étape de quête
        if quest_for_item:
            current_step = quest_for_item.get_current_step()
            print(f"\n{current_step.description}\n")
            
            # Afficher les réponses de la quête
            response = current_step.get_current_response()
            if response:
                print(response)
            
            # Gérer les choix
            if current_step.get_current_choices():
                if Actions.handle_choices(current_step, quest_for_item, game):
                    # Si tous les choix sont corrects, on peut prendre l'item
                    quest_for_item.advance()
                else:
                    # Mauvais choix, on ne prend pas l'item
                    print(f"\nVous n'avez pas pris '{item_name}'.\n")
                    return False
            else:
                # Pas de choix, juste avancer l'étape
                quest_for_item.advance()
        
        # Prendre l'item
        if player.get_weight() + player.current_room.items[item_name].weight > player.max_weight:
            print(f"\nVous ne pouvez pas prendre '{item_name}' car cela dépasse votre limite de poids.\n")
            return False
        else :
            item = player.current_room.items.pop(item_name)
            player.inventory[item_name] = item
            print(f"\nVous avez pris '{item_name}'.\n")
            
            # Vérifier les objectifs d'action pour la quête (ex: "Trouver le pied de biche")
            game.player.quest_manager.check_action_objectives("Trouver", item_name)
            
            return True 

    def drop(game, list_of_words, number_of_parameters):
        """
        drops an item from the player's inventory and adds it to the current room.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the item was dropped successfully, False otherwise
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        player = game.player
        item_name = list_of_words[1].lower()

        # Check if the item is in the player's inventory.
        if item_name not in player.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans votre inventaire.\n")
            return False
        
        # Drop the item from the player's inventory and add it to the current room.
        item = player.inventory.pop(item_name)
        player.current_room.items[item_name] = item
        print(f"\nVous avez déposé '{item_name}'.\n")
        return True

    def check(game, list_of_words, number_of_parameters):
        """
        checks the player's inventory.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the inventory was checked successfully, False otherwise.
        """

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        player = game.player
        player.get_inventory()
        return True

    def move_pnj(game, list_of_words, number_of_parameters):
        for character in game.character:
            character.move()
        return True

    def talk(game, list_of_words, number_of_parameters):
        """
        Talk to a character in the current room.
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        if len(game.player.current_room.characters) >= 1:
            character_name = list_of_words[1].lower()
            # Chercher le personnage en comparant les noms en minuscules
            character = None
            for char_name, char_obj in game.player.current_room.characters.items():
                # Chercher si le nom commence par le terme ou si c'est une correspondance partielle
                if char_name.lower().startswith(character_name) or character_name in char_name.lower():
                    character = char_obj
                    break
            if character is not None:
                # Marquer l'objectif "Parler à [character]" comme complété
                game.player.quest_manager.check_action_objectives("Parler", character.name)
                if not Actions.check_pnj_quest(game, character):
                    print(character.get_msg())
                    # Gestion générique des outils proposés par un personnage
                    if getattr(character, "tool_choices", None):
                        Actions.handle_tool_gift(game, character)
            else:
                print(f"Il n'y a pas de personnage nommé {character_name} dans cette pièce.")
        else:
            print("Il n'y a aucun PNJ dans cette pièce")
        return True

#####

    @staticmethod
    def use(game, list_of_words: list, number_of_parameters: int) -> bool:
        """
        Utilise l'outil et accorde la récompense de quête si applicable.
        Vérifie toutes les conditions d'utilisation, affiche les messages d'erreur, et gère l'ajout de la récompense à l'inventaire ou à la pièce.
        Args:
            game (Game): L'instance du jeu.
            list_of_words (list): Commande utilisateur.
            number_of_parameters (int): Nombre de paramètres attendus.
        Returns:
            bool: True si l'outil a été utilisé avec succès, False sinon
        """
        player = game.player
        current_room = player.current_room
        inventaire_lower = {k.lower(): v for k, v in player.inventory.items()}

        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1].lower()

        # Vérifie la présence de l'item dans l'inventaire
        if item_name not in player.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans votre inventaire.\n")
            return False

        # Prépare les conditions dynamiques
        localisation = player.current_room.name.lower()
        objets_piece = list(current_room.items.keys())
        inventaire_items = list(inventaire_lower.keys())

        # Vérifie les conditions d'utilisation
        success = Actions.check_condition_outils(game, item_name, localisation, objets_piece, inventaire_items)
        if not success:
            print(f"\n{item_name} ne vous est pas utile.\n")
            return False

        print(f"\nVous avez utilisé {item_name} avec succès.\n")
        del player.inventory[item_name]

        # Vérifier les objectifs d'action pour la quête (ex: "Utiliser la clé-étage")
        game.player.quest_manager.check_action_objectives("Utiliser", item_name)
        return True

    @staticmethod
    def check_condition_outils(game, outil: str, localisation: str, objets_piece: list, inventaire: list):
        """
        Vérifie si toutes les conditions d'utilisation de l'outil sont remplies.
        Affiche des messages d'erreur précis si une condition n'est pas satisfaite.
        Retourne un tuple (bool, Item): (True/False si utilisable, récompense ou None).
        """
        # Clé à l'étage
        if outil == "clé-étage":
            if "étage" in localisation:
                print("\nVous avez réussi à ouvrir la porte de l'étage et trouvez un microphone par terre !\n")
                return True
            print("\nVous devez être à l'étage pour utiliser la clé.\n")
            return False
        # Pied-de-biche dans la voiture
        if outil == "pied-de-biche":
            if localisation == "voiture":
                return True
            print("\nVous devez être dans la voiture pour utiliser le pied-de-biche.\n")
            return False
        # Tournevis au sous-sol avec table et matériaux
        if outil == "tournevis":
            if localisation == "sous_sol":
                if "table" in [x.lower() for x in objets_piece]:
                    materiaux_requis = ["modulateur", "batterie", "piles", "câbles", "microphone", "appareil-auditif", "carte-mère"]
                    manquants = [mat for mat in materiaux_requis if mat not in inventaire]
                    if not manquants:
                        print("\nVous avez fabriqué le dispositif d'ultrasons avec succès !\n")
                        return True
                    print("\nIl vous manque les matériaux suivants :")
                    for mat in manquants:
                        print(f" - {mat}")
                    return False
                print("\nVous devez avoir une table dans la pièce pour utiliser le tournevis au sous-sol.\n")
                return False
            print("\nVous devez être au sous-sol pour utiliser le tournevis.\n")
            return False
        return False


    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title)
        return True

    @staticmethod
    def check_pnj_quest(game, character_found):
        """
        Vérifier si le personnage avec lequel le joueur parle est lié à une quête en cours.
        Args:
            game (Game): L'objet du jeu.
            character (Character): Le personnage avec lequel le joueur parle.
        Returns:
            bool: True si la quête a avancé, False sinon.
        """
        if character_found is None:
            return False
        
        for quest in game.player.quest_manager.quests:
            if quest.character == character_found.name and not quest.is_complete():
                if game.player.current_room == character_found.current_room:
                    current_step = quest.get_current_step()
                    if current_step:
                        # Réinitialiser le dialogue au début à chaque nouvelle interaction
                        current_step.reset_step()
                        Actions.handle_dialogue(current_step)
                        if Actions.handle_choices(current_step, quest, game):
                            Actions.advance_dialogue(game, quest)
                    return True
                l="Vous devez être dans la salle "
                v = " pour parler à "
                print(l + character_found.current_room.name + v + character_found.name)
                return False
        return False

    @staticmethod
    def handle_dialogue(current_step):
        """
        Gérer les réponses pour une étape du dialogue.
        Args:
            current_step (DialogueStep): L'étape de dialogue actuelle.
        """
        response = current_step.get_current_response()
        if response:
            print(f"\n{response}\n")
        else:
            # Si le dialogue est None (condition non remplie), avancer à la prochaine étape
            if current_step.advance_step():
                return
            # Récursivement chercher le prochain dialogue valide
            Actions.handle_dialogue(current_step)

    @staticmethod
    def handle_choices(current_step, quest, game=None):
        """
        Gérer les choix pour une étape de quête donnée.
        Args:
            current_step (QuestStep): L'étape de quête actuelle.
            quest (Quest): La quête actuelle.
            game (Game): L'objet du jeu (optionnel, pour les récompenses).
        Returns:
            bool: True si le joueur a fait un choix valide, False sinon.
        """
        # Si le dialogue courant est conditionnel et non satisfait, sauter cette étape
        if current_step.current_step < len(current_step.dialogue):
            dlg_item = current_step.dialogue[current_step.current_step]
            if isinstance(dlg_item, tuple):
                _, condition = dlg_item
                if condition is not None and current_step.player_choice != condition:
                    # Avancer au prochain dialogue/choix valide
                    if current_step.advance_step():
                        return True
                    Actions.handle_dialogue(current_step)
                    return Actions.handle_choices(current_step, quest, game)

        choices = current_step.get_current_choices()

        if not choices:
            # Étape sans choix : on considère cette étape validée
            return True

        # Si c'est la question des outils, filtrer pour enlever les outils déjà choisis
        displayed_choices = list(choices)
        if hasattr(quest, 'tool_choices') and any(tool in choices for tool in quest.tool_choices.keys()):
            if quest.selected_rewards:
                # Créer une liste des noms d'outils déjà choisis
                selected_tool_names = [reward.name for reward in quest.selected_rewards]
                displayed_choices = [tool for tool in choices if quest.tool_choices.get(tool, None) and quest.tool_choices[tool].name not in selected_tool_names]
                # Si tous les outils ont été choisis, skip cette étape
                if not displayed_choices:
                    return True

        print("─" * 40)
        for i, choice in enumerate(displayed_choices, 1):
            print(f" {i}. {choice}")
        print("─" * 40)
        user_choice = input("\nChoisissez une option: ")
        try:
            user_choice = int(user_choice)
            if 1 <= user_choice <= len(displayed_choices):
                chosen_option = displayed_choices[user_choice - 1]
                print(f"Vous avez choisi: {chosen_option}")
                correct_choices = current_step.get_current_correct_choices()
                if chosen_option in correct_choices:
                    # Enregistrer le choix du joueur pour les conditions de dialogue
                    current_step.set_player_choice(chosen_option)
                    
                    # Marquer les objectifs liés au choix comme complétés
                    quest.check_dialogue_choice_objective(chosen_option, player=None)
                    
                    # Si c'est un choix d'outil, l'ajouter à la liste des récompenses et le donner au joueur
                    if hasattr(quest, 'tool_choices') and chosen_option in quest.tool_choices:
                        tool_item = quest.tool_choices[chosen_option]
                        quest.selected_rewards.append(tool_item)  # Ajouter à la liste au lieu de remplacer
                        # Donner l'outil au joueur immédiatement
                        if game and game.player:
                            game.player.inventory[tool_item.name] = tool_item
                            print(f"Vous avez obtenu: {tool_item.description}")
                    
                    if current_step.advance_step():
                        return True
                    Actions.handle_dialogue(current_step)
                    return Actions.handle_choices(current_step, quest, game)
                print("Choix incorrect. Vous devez recommencer l'étape.")
                current_step.reset_step()  # Réinitialisation de la sous-étape
                return False
            print("Choix invalide.")
            return False
        except ValueError:
            print("Choix invalide.")
            return False

    @staticmethod
    def advance_dialogue(game, quest):
        """
        Faire avancer le dialogue.
        Args:
            game (Game): L'objet du jeu.
            quest (Quest): La quête actuelle.
        """
        current_step = quest.get_current_step()
        if current_step.advance_step():
            # Si on arrive à la fin du dialogue, donner la récompense principale si définie
            if game and game.player:
                quest.grant_reward(game.player)
            # Étape finale atteinte
            if current_step.reward_item:
                game.player.inventory[current_step.reward_item.name] = current_step.reward_item
                print(f"Vous avez reçu {current_step.reward_item.name} comme récompense.")
            if quest.is_complete() and not getattr(quest, 'title', None) == "La quête principale":
                print(f"Félicitations, vous avez complété la quête: {quest.title}")
            return

        # Sinon, afficher le dialogue et gérer les choix, puis continuer
        Actions.handle_dialogue(current_step)
        if Actions.handle_choices(current_step, quest, game):
            return Actions.advance_dialogue(game, quest)
        print("Vous avez échoué cette étape de la quête. Veuillez réessayer.")

    @staticmethod
    def handle_tool_gift(game, character):
        """Allow a character to give selectable tools once each."""
        # Outils déjà donnés
        given = set(getattr(character, "given_tools", []))
        available = {
            name: item for name, item in character.tool_choices.items()
            if name not in given and name not in game.player.inventory
        }
        if not available:
            return
        print("─" * 40)
        tool_names = list(available.keys())
        for i, name in enumerate(tool_names, 1):
            print(f" {i}. {name}")
        print("─" * 40)
        choice = input("\nChoisissez un outil: ")
        try:
            idx = int(choice)
            if 1 <= idx <= len(tool_names):
                chosen_name = tool_names[idx - 1]
                item = available[chosen_name]
                if game.player.add_reward(item):
                    character.given_tools.append(chosen_name)
                return
            print("Choix invalide.")
        except ValueError:
            print("Choix invalide.")
