# Define the character class
class Character():
    """
    A class to represent a character in the game.

    Attributes:
        name (str): The name of the character.
        description (str): A brief description of the character.
        current_room (Room): The room where the character is currently located.
        msgs (list): A list of messages associated with the character.
        
    """

    # Constructor
    def __init__(self, name: str, description: str, current_room, msgs : list):
        self.name = name
        self.description = description
        self.current_room = None
        self.msgs = []

