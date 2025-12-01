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
            
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.history.append(next_room)
        self.current_room = next_room
        print(self.current_room.get_long_description())
        self.get_history()
        return True

    def go_back(self):
        # If the history has less than 2 entries, there's no previous room to go back to.
        if len(self.history) <= 1:
            print("\nVous n'avez pas d'historique de déplacement.\n")
            return False
        # Remove the current room from history
        self.history.pop()
        # Get the previous room (now the last element)
        previous_room = self.history[-1]
        # Set the current room to the previous room
        self.current_room = previous_room
        print(self.current_room.get_long_description())
        self.get_history()
        return True



    # Define the history method.
    def get_history(self):
        print("\nVous avez déjà visité les lieux suivants :")
        for room in self.history:
            print(f"- {room.name}")