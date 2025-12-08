# Define the Room class.

class Room:
    """
        This class represents a room. A room is composed of a name, a description, and exits.

        Attributes:
            name (str): The name of the room.
            description (str): The description of the room.
            exits (dictionnaire): The different exits possible.out
    """
    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.items = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes dans{self.description}\n\n{self.get_exit_string()}\n"

    # Display the items in the room.
    def get_inventory(self):
        """Display items available in the room."""
        if not self.items:
            print("\nIl n'y a rien ici.\n")
            return False
        
        else:
            print("\nLa pièce contient :")
            for item_name, item in self.items.items():
                print(f"- {item}")
            return True

            """ne marche pas quand on fait back !!"""
