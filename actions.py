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
                if Actions.handle_choices(current_step, quest_for_item):
                    # Si tous les choix sont corrects, on peut prendre l'item
                    quest_for_item.advance()
                else:
                    # Les mauvais choix, on ne prend pas l'item
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
        
        player = game.player
        character_name = list_of_words[1].lower()
        
        # Find the character in the current room
        character_found = None
        for character in game.character:
            character_first_name = character.name.split()[0].lower()
            if character.name.lower() == character_name or character_first_name == character_name:
                # Check if character is in the same room as the player
                if character.current_room is player.current_room:
                    character_found = character
                    break      
        if character_found is None:
            print(f"\n'{character_name}' n'est pas dans la pièce.\n")
            return False
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
        success, quest_reward = Actions.check_condition_outils(game, item_name, localisation, objets_piece, inventaire_items)
        if not success:
            print(f"\n{item_name} ne vous est pas utile.\n")
            return False

        print(f"\nVous avez utilisé {item_name} avec succès.\n")

        # Ajoute la récompense à l'inventaire ou à la pièce
        if quest_reward:
            if player.check_inventory_space(quest_reward.weight):
                player.inventory[quest_reward.name] = quest_reward
                print(f"Vous avez obtenu : {quest_reward.name}\n")
                del player.inventory[item_name]
                # Si c'est le dispositif d'ultrasons, retire les matériaux utilisés
                if quest_reward.name == "dispositif d'ultrasons":
                    materiaux_requis = ["modulateur", "batterie", "piles", "câbles", "microphone", "appareil-auditif", "carte-mère"]
                    for mat in materiaux_requis:
                        if mat in player.inventory:
                            del player.inventory[mat]
            else:
                current_room.items[quest_reward.name] = quest_reward
                print(f"\nVotre inventaire est trop plein pour {quest_reward.name}. L'objet a été déposé dans la pièce.\n")
                return False
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
            if localisation == "etage":
                from item import Item
                quest_reward = Item("Microphone", "Microphone trouvé à l'étage", 1.0)
                print("\nVous avez réussi à ouvrir la porte de l'étage et trouvez un microphone par terre !\n")
                return True, quest_reward
            print("\nVous devez être à l'étage pour utiliser la clé.\n")
            return False, None
        # Pied-de-biche dans la voiture
        if outil == "pied-de-biche":
            if localisation == "voiture":
                from item import Item
                quest_reward = Item("câbles", "Câbles récupérés du tableau de bord", 1.0)
                print("\nVous avez réussi à ouvrir le tableau de bord et récupérer les câbles !\n")
                return True, quest_reward
            print("\nVous devez être dans la voiture pour utiliser le pied-de-biche.\n")
            return False, None
        # Tournevis au sous-sol avec table et matériaux
        if outil == "tournevis":
            if localisation == "sous_sol":
                if "table" in [x.lower() for x in objets_piece]:
                    materiaux_requis = ["modulateur", "batterie", "piles", "câbles", "microphone", "appareil-auditif", "carte-mère"]
                    manquants = [mat for mat in materiaux_requis if mat not in inventaire]
                    if not manquants:
                        from item import Item
                        quest_reward = Item("dispositif d'ultrasons", "Dispositif d'ultrasons assemblé", 1.0)
                        print("\nVous avez fabriqué le dispositif d'ultrasons avec succès !\n")
                        return True, quest_reward
                    print("\nIl vous manque les matériaux suivants :")
                    for mat in manquants:
                        print(f" - {mat}")
                    return False, None
                print("\nVous devez avoir une table dans la pièce pour utiliser le tournevis au sous-sol.\n")
                return False, None
            print("\nVous devez être au sous-sol pour utiliser le tournevis.\n")
            return False, None
        return False, None


    @staticmethod
    def check_quest_talk(game, character):
        """
        Vérifier si le personnage avec lequel le joueur parle est lié à une quête en cours.
        Args:
            game (Game): L'objet du jeu.
            character (Character): Le personnage avec lequel le joueur parle.
        Returns:
            bool: True si la quête a avancé, False sinon.
        """
        if character is None:
            return False
        for quest in game.quests:
            current_step = quest.get_current_step()
            if current_step and current_step.character == character:
                if game.player.current_room == character.current_room:
                    Actions.handle_special_responses(current_step)
                    if Actions.handle_choices(current_step, quest):
                        Actions.advance_quest(game, quest)
                    return True
                l="Vous devez être dans la salle "
                v = " pour parler à "
                print(l + character.current_room.name + v + character.name)
                return False
        return False


        # Cas spécial pour Lee Abbott: vérifier si la quête continue
        if character_found.name == "Lee Abbot":
            lee_quest = None
            for quest in game.quests:
                if quest.title == "Interagir avec Lee Abbott":
                    lee_quest = quest
                    break
            
            # Vérifier si le joueur a déjà les clés ET le tournevis
            has_keys = "clé-étage" in player.inventory
            has_screwdriver = "tournevis" in player.inventory
            
            # Si quête complétée ET a tous les items, terminer
            if has_keys and has_screwdriver:
                print(f"\nLee Abbott: Bravo ! Tu as tout ce qu'il te faut. Bonne chance !\n")
                if lee_quest:
                    lee_quest.reset_to_step(len(lee_quest.steps))
                return True
            
            # Sinon, proposer les choix restants
            if lee_quest:
                current_step = lee_quest.get_current_step()
                if current_step:
                    print(f"\n{current_step.description}\n")
                    response = current_step.get_current_response()
                    if response:
                        print(response)
                    
                    # Afficher les choix non encore effectués avec leurs numéros originaux
                    if current_step.get_current_choices():
                        choices = current_step.get_current_choices()
                        
                        print("\nChoix disponibles:")
                        choice_mapping = {}  # Mapper les numéros affichés aux choix
                        displayed_num = 1
                        
                        for original_idx, choice in enumerate(choices):
                            # Masquer le choix "Pouvez-vous me prêter un outil ?" si le tournevis n'a pas été obtenu
                            if choice == "Pouvez-vous me prêter un outil ?" and "tournevis" not in player.inventory:
                                continue
                            if choice not in lee_quest.completed_paths:
                                print(f"{original_idx + 1}. {choice}")
                                choice_mapping[original_idx + 1] = choice
                        
                        if choice_mapping:
                            user_input = input("Votre choix: ")
                            try:
                                choice_num = int(user_input)
                                if choice_num in choice_mapping:
                                    chosen_option = choice_mapping[choice_num]
                                    print(f"\nVous avez choisi: {chosen_option}\n")
                                    
                                    # Marquer ce choix comme complété
                                    lee_quest.completed_paths.append(chosen_option)
                                    
                                    # Avancer et afficher la réaction
                                    lee_quest.advance()
                                    next_step = lee_quest.get_current_step()
                                    
                                    if next_step:
                                        # Adapter le message en fonction du choix
                                        if chosen_option == "Puis-je vous aider ?":
                                            print(f"\n{next_step.description}\n")
                                            response = next_step.get_current_response()
                                            if response:
                                                print(response)
                                            # Ajouter la récompense
                                            if next_step.reward:
                                                if player.check_inventory_space(next_step.reward.weight):
                                                    player.inventory[next_step.reward.name] = next_step.reward
                                                    print(f"\nVous avez obtenu: {next_step.reward.name}\n")
                                                else:
                                                    print(f"\n⚠️ Votre inventaire est trop plein pour {next_step.reward.name}.\n")
                                        elif chosen_option == "Pouvez-vous me prêter un outil ?":
                                            print(f"\nLee Abbott réfléchit un moment et dit : 'Je pourrais te prêter un outil. Lequel te serait utile ?'\n")
                                            print("Voici les outils disponibles:")
                                            print("1. Marteau")
                                            print("2. Tournevis")
                                            print("3. Clé à molette\n")
                                            
                                            tool_input = input("Quel outil voulez-vous ? ")
                                            try:
                                                tool_choice = int(tool_input)
                                                from item import Item
                                                tools = {
                                                    1: Item("marteau", "Un marteau robuste (outil)", 2.5),
                                                    2: Item("tournevis", "Un tournevis multifonction (outil)", 1.5),
                                                    3: Item("clé-molette", "Une clé à molette (outil)", 3.0)
                                                }
                                                tool_names = {1: "marteau", 2: "tournevis", 3: "clé-molette"}
                                                
                                                if tool_choice in tools:
                                                    tool_item = tools[tool_choice]
                                                    tool_name = tool_names[tool_choice]
                                                    if player.check_inventory_space(tool_item.weight):
                                                        player.inventory[tool_name] = tool_item
                                                        print(f"\nLee Abbott vous donne le {tool_name}.\n")
                                                        print(f"Vous avez obtenu: {tool_name}\n")
                                                    else:
                                                        print(f"\n Votre inventaire est trop plein pour le {tool_name}.\n")
                                            except ValueError:
                                                print("Choix invalide.")
                                        else:
                                            # Choix 3: "Je n'ai besoin de rien"
                                            print(f"\nLee Abbott hausse les épaules et retourne à son travail.\n")
                                        
                                        # Réinitialiser la quête à l'étape 1 pour relancer le dialogue
                                        lee_quest.reset_to_step(0)
                            except ValueError:
                                print("Choix invalide.")
                                return False
                        else:
                            print("\nLee Abbott: Tu as déjà exploré tous tes choix pour le moment...\n")
                return True
        
        # Chercher une quête liée à ce personnage (pour les autres PNJ)
        quest_for_character = None
        for quest in game.quests:
            if not quest.is_complete():
                current_step = quest.get_current_step()
                if current_step and current_step.character == character_found.name:
                    quest_for_character = quest
                    break
        
        # Si une quête est liée à ce personnage, afficher l'étape de quête
        if quest_for_character:
            current_step = quest_for_character.get_current_step()
            print(f"\n{current_step.description}\n")
            
            # Afficher les réponses de la quête
            response = current_step.get_current_response()
            if response:
                print(response)
            
            # Gérer les choix
            if current_step.get_current_choices():
                if Actions.handle_choices(current_step, quest_for_character):
                    # handle_choices a géré les choix correctement, avancer la quête
                    quest_for_character.advance()
                    next_step = quest_for_character.get_current_step()
                    
                    if next_step:
                        # Afficher l'étape suivante
                        print(f"\n{next_step.description}\n")
                        response = next_step.get_current_response()
                        if response:
                            print(response)
                        
                        # Ajouter la récompense
                        if next_step.reward:
                            if player.check_inventory_space(next_step.reward.weight):
                                player.inventory[next_step.reward.name] = next_step.reward
                                print(f"\nVous avez obtenu: {next_step.reward.name}\n")
                            else:
                                print(f"\n Votre inventaire est trop plein pour {next_step.reward.name}.\n")
            else:
                # Pas de choix, juste avancer l'étape
                quest_for_character.advance()
                if current_step.reward:
                    if player.check_inventory_space(current_step.reward.weight):
                        player.inventory[current_step.reward.name] = current_step.reward
                        print(f"\nVous avez obtenu: {current_step.reward.name}\n")
        else:
            # Pas de quête liée, juste afficher le message du personnage
            message = character_found.get_msg()
            print(f"\n{character_found.name} : {message}\n")
        
        return True

    
    

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
        if game.quests:
            print("\nListe des quêtes:")
            print("=" * 50)
            
            # Display main quests
            main_quests = [q for q in game.quests if q.is_main_quest]
            if main_quests:
                print("\n★ QUÊTES PRINCIPALES ★")
                for quest in main_quests:
                    if quest.is_complete():
                        status = "✓ Complétée"
                    elif quest.current_step > 0:
                        status = "➤ En cours"
                    else:
                        status = "○ Non démarrée"
                    print(f"  {quest.title} [{status}]")
                    print(f"    {quest.description}")
            
            # Display secondary quests
            secondary_quests = [q for q in game.quests if not q.is_main_quest]
            if secondary_quests:
                print("\n◆ QUÊTES SECONDAIRES ◆")
                for i, quest in enumerate(secondary_quests, 1):
                    if quest.is_complete():
                        status = "✓ Complétée"
                    elif quest.current_step > 0:
                        status = "➤ En cours"
                    else:
                        status = "○ Non démarrée"
                    print(f"  {i}. {quest.title} [{status}]")
                    print(f"     {quest.description}")
            
            print("\n" + "=" * 50)
        else:
            print("\nAucune quête disponible.\n")
        return True


    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest and its current step.
       
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.
        Returns:
            bool: True if the command was executed successfully, False otherwise """

        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Find and show quest details
        for quest in game.quests:
            if quest.title.lower() == quest_title.lower():
                print(f"\n=== Quête: {quest.title} ===")
                print(f"Description: {quest.description}")
                print(f"Progression: {quest.current_step + 1}/{len(quest.steps)}")
                
                current_step = quest.get_current_step()
                if current_step:
                    print(f"\nÉtape actuelle: {current_step.description}")
                else:
                    print("\nQuête complétée!")
                return True
        
        print(f"\nQuête '{quest_title}' non trouvée.\n")
        return False

    @staticmethod
    def handle_special_responses(current_step):
        """
        Gérer les réponses spéciales pour une étape de quête donnée.
        Args:
            current_step (QuestStep): L'étape de quête actuelle.
        """
        response = current_step.get_current_response()
        if response:
            print(response)

    @staticmethod
    def handle_choices(current_step, quest):
        """
        Gérer les choix pour une étape de quête donnée.
        Args:
            current_step (QuestStep): L'étape de quête actuelle.
            quest (Quest): La quête actuelle.
        Returns:
            bool: True si le joueur a fait un choix valide, False sinon.
        """
        choices = current_step.get_current_choices()
        if choices:
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice}")
            user_choice = input("Choisissez une option: ")
            try:
                user_choice = int(user_choice)
                if 1 <= user_choice <= len(choices):
                    chosen_option = choices[user_choice - 1]
                    print(f"Vous avez choisi: {chosen_option}")
                    correct_choices = current_step.get_current_correct_choices()
                    if chosen_option in correct_choices:
                        if current_step.advance_substep():
                            return True
                        Actions.handle_special_responses(current_step)
                        return Actions.handle_choices(current_step, quest)
                    print("Choix incorrect. Vous devez recommencer l'étape.")
                    current_step.reset_substep()  # Réinitialisation de la sous-étape
                    return False
                print("Choix invalide.")
                return False
            except ValueError:
                print("Choix invalide.")
                return False
        return False

    @staticmethod
    def advance_quest(game, quest):
        """
        Faire avancer la quête actuelle.
        Args:
            game (Game): L'objet du jeu.
            quest (Quest): La quête actuelle.
        """
        current_step = quest.get_current_step()
        if current_step.advance_substep():
            quest.advance()
            if current_step.reward:
                game.player.inventory[current_step.reward.name] = current_step.reward
                print(f"Vous avez reçu {current_step.reward.name} comme récompense.")
            if quest.is_complete() and not quest.title == "La quête principale":
                print(f"Félicitations, vous avez complété la quête: {quest.title}")
            else:
                next_step = quest.get_current_step()
                if next_step:
                    next_step.current_substep = 0
                    print(f"Étape suivante: {next_step.description}")
                    if game.player.current_room == next_step.character.current_room:
                        Actions.handle_special_responses(next_step)
                        Actions.handle_choices(next_step, quest)
                    else:
                        l = "Vous devez aller dans la salle "
                        v = " pour continuer la quête."
                        print(l + next_step.character.current_room.name + v)
        else:
            Actions.handle_special_responses(current_step)
            if not Actions.handle_choices(current_step, quest):
                print("Vous avez échoué cette étape de la quête. Veuillez réessayer.")

