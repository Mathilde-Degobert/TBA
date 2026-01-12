# Define the character class
import random

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
    def __init__(self, name: str, description: str, current_room): #msg : list
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = []

    def move(self):
        from game import DEBUG
        if not random.choice([True, False]):
            return False
        exits = [room for room in self.current_room.exits.values() if room is not None  ]
        if not exits:
            return False
        next_room = random.choice(exits)
        if next_room is self.current_room:
            return False
        self.current_room = next_room
        if DEBUG:
            print(f"DEBUG : {self.name} se déplace vers {next_room.name}")
        return True
    def get_msg(self):
        if not self.msgs:
            return "None"
        msg = self.msgs.pop(0)
        print(f"\n{msg}\n")
        self.msgs.append(msg)
        return True