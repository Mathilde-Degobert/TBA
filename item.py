""" This module contains the Item class which represents an item in the game. """

class Item:
    """
    This class represents an item that can be found in rooms and picked up by the player.
    
    Attributes:
        name (str): The name of the item.
        description (str): The description of the item.
        weight (float): The weight of the item in kg.
    
    Methods:
        __init__(self, name, description, weight): The constructor.
        __str__(self): Return a textual representation of the item.
    """

    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        """ Returns a textual representation of the item."""
        return f"{self.name} : {self.description} ({self.weight} g)"

    def is_heavy(self, threshold=10.0):
        """
        Check if the item is heavy based on a weight threshold.
        
        Args:
            threshold (float): The weight threshold in kg (default: 10.0).
            
        Returns:
            bool: True if the item's weight exceeds the threshold, False otherwise.
        """
        return self.weight > threshold
