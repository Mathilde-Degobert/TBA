# Define the Room class.
""" Module for room representation in the game. """

class Room:
    """
        This class represents a room. A room is composed of a name, a description, and exits.

        Attributes:
            name (str): The name of the room.
            description (str): The description of the room.
            exits (dictionnaire): The different exits possible.
    """
    # Define the constructor.
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = {}
        self.characters = {}
        self.locked = False
        self.locked_message = "La porte est fermée à clé."

    # Define the get_exit method.
    def get_exit(self, direction):
        """ Get the exit in the given direction.
        Args:
            direction (str): The direction of the exit.
        Returns:
            Room: The room in the given direction."""
        # Return the room in the given direction if it exists.
        if direction in self.exits:
            return self.exits[direction]
        return None

    # Return a string describing the room's exits.
    def get_exit_string(self):
        """ Returns a string describing the room's exits."""
        exit_string = "Sorties: "
        for exit_dir in self.exits:
            if self.exits.get(exit_dir) is not None:
                exit_string += exit_dir + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        """ Returns a long description of this room including exits."""
        return f"\nVous êtes dans{self.description}\n\n{self.get_exit_string()}\n"

    # Display the items in the room.
    def get_inventory(self):
        """Display items available in the room.
        Returns:
            bool: True if there are items, False otherwise.
        """
        if not self.items:
            print("\nIl n'y a rien ici.\n")
            return False
        print("\nLa pièce contient :")
        for item in self.items.values():
            print(f"- {item}")
        return True
