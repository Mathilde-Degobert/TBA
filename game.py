# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quest import quest

# Debug flag
DEBUG = False

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.character = []
    
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
        back = Command("back", " : revenir à la pièce précédente", Actions.go_back, 0)
        self.commands["back"] = back
        look = Command("look", " : observer la pièce actuelle", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <item> : prendre un objet dans la pièce", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item> : déposer un objet de l'inventaire dans la pièce", Actions.drop, 1)     
        self.commands["drop"] = drop
        check = Command("check", " : vérifier le contenu de l'inventaire", Actions.check, 0)
        self.commands["check"] = check
        talk = Command("talk", " <character> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"] = talk
        
        self.commands["quest"] = Command("quest"
                                         , " <titre> : afficher les détails d'une quête"
                                         , Actions.quest
                                         , 1)
        self.commands["activate"] = Command("activate"
                                            , " <titre> : activer une quête"
                                            , Actions.activate
                                            , 1)
        self.commands["rewards"] = Command("rewards"
                                           , " : afficher vos récompenses"
                                           , Actions.rewards
                                           , 0)



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
      
        # Add items to rooms
        forest.items = {
            "modulateur": Item("modulateur", "Module d'amplification", 4),
        }
        pont.items = {
            "batterie": Item("batterie", "vieille batterie", 2)
        }
        Magasin.items = {
            "piles": Item("piles", "boîte de 4 piles", 3),
            "radio": Item("radio", "vieille radio", 2),
            "jouet": Item("jouet", "petit avion avec un speaker des lumieres", 1)
        }
        Champs.items = {
            "transformateur": Item("transformateur", "un vieux transformateur électrique", "3")
        }
        Maison_rez_de_chaussée.items = {
            "clé": Item("clé", "une clé menant vers l'étage", 0.5)
        }
        Maison_étage.items = {
            "microphone": Item("microphone", "un microphone du babyphone", 0.5)
        }
        Voiture.items = {
            "clés": Item("clés", "les clés menant au sous-sol", 0.5),
            "câbles": Item("câbles", "des câbles électriques", 1)
        }
        Sous_sol.items = {
            "outils": Item("outils", "des outils divers", 2)
        }
        
        # Setup Character
        Beau_Abbot = Character("Beau Abbot", "Le cadet de la famille Abbot, agé d'a peine 4 ans. Il vous regarde de ses petits yeux innocents.", Maison_rez_de_chaussée)
        Beau_Abbot.msgs = ["Bonjour", "Je m'appelle Beau"]
        self.character.append(Beau_Abbot)
        Marcus_Abbot = Character("Marcus Abbot", "Le deuxième fils de la famille Abbot, agé de 12 ans, il fuit votre regard, apeuré.", Maison_étage)
        Marcus_Abbot.msgs = ["Bonjour", "Je m'appelle Marcus"]
        self.character.append(Marcus_Abbot)
        Lee_Abbot = Character("Lee Abbot", "Le père de famille, un homme d'une quarantaine d'années, il semble tendu.", Maison_rez_de_chaussée)
        Lee_Abbot.msgs = ["Bonjour", "Je m'appelle Lee"]
        self.character.append(Lee_Abbot)
        Evelyn_Abbot = Character("Evelyn Abbot", "la mère de la famille, enceinte et très protectrice de ses enfants", Maison_étage)
        Evelyn_Abbot.msgs = ["Bonjour", "Je m'appelle Evelyn"]
        self.character.append(Evelyn_Abbot)
        Femme_dans_la_foret = Character("La femme dans la forêt", "une vieille dame perdue rendue folle par le deuil", forest)
        Femme_dans_la_foret.msgs = ["Bonjour", "Je m'appelle... je ne me souviens plus"]
        self.character.append(Femme_dans_la_foret)
        
        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = Magasin


    #setup quests
    def setup_quests(self):
        """Initialize all quests."""
        exploration_quest = Quest(
            title="Grand Explorateur",
            description="Explorez tous les lieux de ce monde mystérieux.",
            objectives=["Visiter Magasin"
                        , "Visiter forest"
                        , "Visiter Champs"
                        , "Visiter pont"
                        , "Visiter Maison_rez_de_chaussée"
                        , "Visiter Maison_étage"
                        , "Visiter Voiture"
                        , "Visiter Sous_sol"],
            reward="Titre de Grand Explorateur"
        )


        travel_quest = Quest(
            title="Grand Voyageur",
            description="Déplacez-vous 10 fois entre les lieux.",
            objectives=["Se déplacer 10 fois"],
            reward="lampe torche"
        )


        discovery_quest = Quest(
            title="passepartout",
            description="parvenez à entrer à l'étage.",
            objectives=["Visiter Maison_étage"],
            reward="clé à molette"
        )

    def loose_quests(self):
        """Initialize loose quests."""
        die_quest = Quest(
            title="mort tragique",
            description="vous faites le mauvais choix et vous faites tuer par une créature",
            objectives=["prendre les piles", "parler a la femme dans la forêt"],
            reward="bandeau de deuil"
        )

    def win_quests(self):
        """Initialize win quests."""



      # Add quests to player's quest manager
        self.player.quest_manager.add_quest(exploration_quest)
        self.player.quest_manager.add_quest(travel_quest)
        self.player.quest_manager.add_quest(discovery_quest)



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
        if command_word not in self.commands:
            msg1 = f"\nCommande '{command_word}' non reconnue."
            msg2 = " Entrez 'help' pour voir la liste des commandes disponibles.\n"
            print(msg1 + msg2)
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
