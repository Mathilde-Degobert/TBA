# Define the Player class.
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
        self.current_room.get_inventory()
        self.get_inventory()
        self.get_history()
        return True


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