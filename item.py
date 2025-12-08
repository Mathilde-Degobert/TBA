
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
        """
        Initialize an Item.
        
        Args:
            name (str): The name of the item.
            description (str): The description of the item.
            weight (float): The weight of the item in kg.
        """
        self.name = name
        self.description = description
        self.weight = weight
    
    def __str__(self):
        """
        Return a textual representation of the item.
        
        Returns:
            str: A formatted string with the item's name, description, and weight.
        """
        return f"{self.name} : {self.description} ({self.weight} kg)"