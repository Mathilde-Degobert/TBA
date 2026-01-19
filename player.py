# Define the Player class.

from quest import QuestManager

class Player():
    """
        This class represents a player. A player is composed of a name and a current room.

        Attributes:
            name (str): The name.
            current_room (Room): The current room.
        Methods:
            __init__(self, name) : The constructor.
            move(self, direction): The move
    """
    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.max_weight = 8.0  
         self.move_count = 0
        self.quest_manager = QuestManager(self)
        self.rewards = []  # List to store earned rewards

            
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.history.append(self.current_room)
        self.current_room = next_room
        print(self.current_room.get_long_description())
        
        
        # Check room visit objectives
        self.quest_manager.check_room_objectives(self.current_room.name)


        # Increment move counter and check movement objectives
        self.move_count += 1
        self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)
        
        return True



    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
       
        Args:
            reward (str): The reward to add.
           
        Examples:
       
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")



    def show_rewards(self):
        """
        Display all rewards earned by the player.
       
        Examples:
       
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()



    # Define the history method.
    def get_history(self):
        if self.history == []:
            print("\nVous n'avez pas encore visité de pièces.\n")
            return False
        
        else :
            print("\nVous avez déjà visité les lieux suivants :")
            for room in self.history:
                print(f"- {room.name}")

    def get_inventory(self):
        """Display the player's inventory."""
        if not self.inventory :
            print("\nVotre inventaire est vide.\n")
            return False
        
        else :
            print("\nVotre inventaire contient :")
            for item_name, item in self.inventory.items():
                    print(f"- {item}")

    def get_weight(self):
        """Return the total weight of items in the player's inventory (in kg)."""
        total = 0.0
        for item in self.inventory.values():
            total += item.weight
        return total