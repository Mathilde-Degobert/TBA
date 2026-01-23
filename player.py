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
        self.max_weight = 8000.0  # en grammes
        self.move_count = 0
        self.quest_manager = QuestManager(self)

            
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

        # Increment move counter
        self.move_count += 1
        
        return True



    def add_reward(self, reward):
        """
        Add a reward to the player's inventory.
       
        Args:
            reward (str): The reward to add.
        """
        if reward:
            if self.check_inventory_space(reward.weight):
                self.inventory[reward.name] = reward
                print(f"Vous avez obtenu : {reward.name}\n")
                # Si c'est le dispositif d'ultrasons, retire les matériaux utilisés
                if reward.name == "dispositif d'ultrasons":
                    materiaux_requis = ["modulateur", "batterie", "piles", "câbles", "microphone", "appareil-auditif", "carte-mère"]
                    for mat in materiaux_requis:
                        if mat in self.inventory:
                            del self.inventory[mat]
                return True
            else:
                current_room.items[reward.name] = reward
                print(f"\nVotre inventaire est trop plein pour {reward.name}. L'objet a été déposé dans la pièce.\n")
                return False

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

    def check_inventory_space(self, item_weight):
        """
        Check if the player has space in inventory for an item.
        
        Args:
            item_weight (float): The weight of the item to check.
            
        Returns:
            bool: True if there is space, False otherwise.
        """
        return self.get_weight() + item_weight <= self.max_weight