# Define the character class
import random
from settings import DEBUG

class Character():
    """
    A class to represent a character in the game.

    Attributes:
        name (str): The name of the character.
        description (str): A brief description of the character.
        msgs (list): A list of messages associated with the character.
        
    """

    # Constructor
    def __init__(self, name: str, description: str, current_room, msgs, can_move=True):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        self.can_move = can_move
        # Optional tool reward handling per character
        self.tool_choices = None  # dict name -> Item
        self.given_tools = []  # list of item names already given

    def __str__(self):
        return f"{self.name} : {self.description}"

    def move_aleatoire(self):
        """ Move randomly the character to an adjacent room.
        Returns:
            bool: True if the character can move, False otherwise.
        """
        return random.choice([True, False])
#####
    def move(self):
        if not self.can_move:
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
        """ Display the next message of the character
        Returns:
            str: The next message if there are messages.
        """
        msg = self.msgs.pop(0) if self.msgs else None
        self.msgs.append(msg)
        return msg
    