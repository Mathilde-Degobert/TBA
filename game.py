# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        history = Command("history", " : afficher l'historique des pièces visitées", Actions.history, 0)
        self.commands["history"] = history
        
        # Setup rooms

        forest = Room("Forest", " un sentier sombre, une cabane abandonnée et le bruit assourdissant d'une cascade.")
        self.rooms.append(forest)
        Maison_rez_de_chaussée = Room("Rez de chaussée", " une grande pièce abandonée, un silence lugubre règne. La seule trace de vie : des traces de passage dans la poussière du parquet qui menace de craquer à chaque pas.")
        self.rooms.append(Maison_rez_de_chaussée)
        Maison_étage = Room("Etage", " une odeur de pourriture et de moisissure, un fin rayon de lumière révèle les lieux autrement noyé par le noir. Les murs semblent écouter, vous retenez votre souffle.")
        self.rooms.append(Maison_étage)
        Champs = Room("Champs", " un champs de maïs peu entrenu, un petit sentier de sable sillone les brins séchés. Au loin vous apercevez un silo abandonné, abimé par le passage du temps.")
        self.rooms.append(Champs)
        Magasin = Room("Magasin", " une ruelle au bitume éclatée, la devanture cassée révèle une superette aux rayons renversés.")
        self.rooms.append(Magasin)
        pont = Room("pont", " un grand pont un peu fissuré.")
        self.rooms.append(pont)
        Voiture = Room("Voiture", " une vielle cadillac bleu aux phares jaunies et à la carosserie.")
        self.rooms.append(Voiture)
        Sous_sol = Room("Sous-sol", " une pièce humide, plongée dans le noir, jonchée d'objets en tout genre.")
        self.rooms.append(Sous_sol)

        # Create exits for rooms

        forest.exits = {"N" : None, "E" : None, "S" : pont, "O" : None, "U": None, "D": None}
        pont.exits = {"N" : forest, "E" : None, "S" : Magasin, "O" : None, "U": None, "D": None}
        Magasin.exits = {"N" : pont, "E" : Champs, "S" : None, "O" : None, "U": None, "D": None }
        Champs.exits = {"N" : None, "E" : None, "S" : Maison_rez_de_chaussée, "O" : Magasin, "U": None, "D": None}
        Maison_rez_de_chaussée.exits = {"N" : Champs, "E" : None, "S" : Voiture, "O" : None, "U": Maison_étage, "D": Sous_sol}
        Maison_étage.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U": None, "D": Maison_rez_de_chaussée}
        Voiture.exits = {"N" : Maison_rez_de_chaussée , "E" : None, "S" : None, "O" : None, "U": None, "D": None}
        Sous_sol.exits = {"N" : None , "E" : None, "S" : None, "O" : None, "U": Maison_rez_de_chaussée, "D": None}
      
        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = Magasin

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(" \n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
