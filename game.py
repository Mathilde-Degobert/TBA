# Description: Game class

# Import modules

from settings import DEBUG
from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quest import Quest, QuestStep


class Game:
    """ This class represents the game. """

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.character = []
        self.quests = []
    
    # Setup the game
    def setup(self):
        """Setup the game rooms, items, characters, and player."""

        # Setup commands
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        history = Command("history", " : afficher l'historique des pièces visitées", Actions.history, 0)
        self.commands["history"] = history
        back = Command("back", " : revenir au lieu précédent", Actions.go_back, 0)
        self.commands["back"] = back
        look = Command("look", " : regarder autour de vous", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <item> : prendre un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item> : déposer un objet de l'inventaire dans la pièce", Actions.drop, 1)     
        self.commands["drop"] = drop
        check = Command("check", " : afficher le contenu de l'inventaire", Actions.check, 0)
        self.commands["check"] = check
        talk = Command("talk", " <character> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"] = talk
        use = Command("use", " <item> : utiliser un outil de l'inventaire", Actions.use, 1) 
        self.commands["use"] = use
        quests = Command("quests", " : afficher la liste de toutes les quêtes", Actions.quests, 0)
        self.commands["quests"] = quests
        quest = Command("quest", " <nom> : afficher l'avancement d'une quête spécifique", Actions.quest, 1)
        self.commands["quest"] = quest


        # Setup rooms
        forest = Room("Forest", " un sentier sombre, une cabane abandonnée et "
        "le bruit assourdissant d'une cascade.")
        self.rooms.append(forest)

        Maison_rez_de_chaussée = Room("Rez de chaussée", " une grande pièce abandonée, "
        "un silence lugubre règne. La seule trace de vie : "
        "des traces de passage dans la poussière du parquet qui menace de craquer à chaque pas.")
        self.rooms.append(Maison_rez_de_chaussée)

        Maison_étage = Room("Etage", " une odeur de pourriture et de moisissure,"
        "un fin rayon de lumière révèle les lieux autrement noyé par le noir. "
        "Les murs semblent écouter, vous retenez votre souffle.")
        self.rooms.append(Maison_étage)

        Champs = Room("Champs", " un champs de maïs peu entrenu, "
        "un petit sentier de sable sillone les brins séchés. "
        "Au loin vous apercevez un silo abandonné, abimé par le passage du temps.")
        self.rooms.append(Champs)

        Magasin = Room("Magasin", " une ruelle au bitume éclatée, "
        "la devanture cassée révèle une superette aux rayons renversés.")
        self.rooms.append(Magasin)

        pont = Room("pont", " un grand pont un peu fissuré.")
        self.rooms.append(pont)

        Voiture = Room("Voiture", " une vielle cadillac bleu aux phares jaunies et à la carosserie.")
        self.rooms.append(Voiture)

        Sous_sol = Room("Sous-sol", " une pièce humide, plongée dans le noir, "
        "jonchée d'objets en tout genre.")
        self.rooms.append(Sous_sol)

        # Create exits for rooms
        forest.exits = {"N" : None, "E" : None, "S" : pont, "O" : None, "U": None, "D": None}
        pont.exits = {"N" : forest, "E" : None, "S" : Magasin, "O" : None, "U": None, "D": None}
        Magasin.exits = {"N" : pont, "E" : Champs, "S" : None, "O" : None, "U": None, "D": None }
        Champs.exits = {"N" : None, "E" : None, "S" : Maison_rez_de_chaussée, "O" : Magasin, 
        "U": None, "D": None}
        Maison_rez_de_chaussée.exits = {"N" : Champs, "E" : None, "S" : Voiture, "O" : None, 
        "U": Maison_étage, "D": Sous_sol}
        Maison_étage.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U": None, 
        "D": Maison_rez_de_chaussée}
        Voiture.exits = {"N" : Maison_rez_de_chaussée , "E" : None, "S" : None, "O" : None, 
        "U": None, "D": None}
        Sous_sol.exits = {"N" : None , "E" : None, "S" : None, "O" : None, 
        "U": Maison_rez_de_chaussée, "D": None}
      
        # Setup items
        # Items : MATÉRIAUX trouvables sur la map
        Modulateur = Item("modulateur", "Module d'amplification (matériau)", 12)
        forest.items[Modulateur.name] = Modulateur

        Batterie = Item("batterie", "Vieille batterie (matériau)", 60)
        pont.items[Batterie.name] = Batterie

        Piles = Item("piles", "Boîte de 4 piles (matériau)", 10)
        Magasin.items[Piles.name] = Piles

        CarteMere = Item("carte-mère", "Carte mère d'ordinateur (matériau)", 25)
        Champs.items[CarteMere.name] = CarteMere

        Câbles = Item("câbles", "Des câbles électriques (matériau)", 5)
        Voiture.items[Câbles.name] = Câbles

        Clés_sous_sol = Item("clés", "les clés menant au sous-sol", 1)
        Voiture.items[Clés_sous_sol.name] = Clés_sous_sol
        
        # Table de bricolage (pour l'assemblage du dispositif final)
        Table_bricolage = Item("table", "une table de bricolage avec tous les outils nécessaires", 50000)
        Sous_sol.items[Table_bricolage.name] = Table_bricolage

        # Récompenses de quêtes :
            # MATERIAUX
        Microphone = Item("microphone", "Microphone de babyphone (matériau)", 15)
        Appareil_Auditif = Item("appareil-auditif", "Appareil auditif ancien (matériau)", 8)
            # OUTILS
        Marteau = Item("marteau", "Un marteau robuste (outil)", 2.5)
        Tournevis = Item("tournevis", "Un tournevis multifonction (outil)", 1.5)
        Cle_a_molette = Item("clé-molette", "Une clé à molette (outil)", 3.0)
        Clé_Etage = Item("clé-étage", "la clé menant à l'étage (outil)", 1)
        Dispositif_ultrasons = Item("dispositif", "un dispositif à ultrasons (créé)", 8.0)
        pied_de_biche = Item("pied-de-biche", "Un pied-de-biche solide (outil)", 4.0)
        Sous_sol.items[pied_de_biche.name] = pied_de_biche

        # Setup Characters
        Beau_Abbot = Character("Beau Abbot", "Le cadet de la famille Abbot, agé d'a peine 4 ans. Il vous regarde de ses petits yeux innocents.", 
        Maison_rez_de_chaussée,
        ["Bonjour", "Je m'appelle Beau"],can_move=True)
        self.character.append(Beau_Abbot)
        Maison_rez_de_chaussée.characters[Beau_Abbot.name] = Beau_Abbot

        Marcus_Abbot = Character("Marcus Abbot", "Le deuxième fils de la famille Abbot, agé de 12 ans. Il fuit votre regard, apeuré.", Maison_étage, 
        ["Bonjour", "Je m'appelle Marcus"], can_move=True)
        self.character.append(Marcus_Abbot)
        Maison_étage.characters[Marcus_Abbot.name] = Marcus_Abbot

        Lee_Abbot = Character("Lee Abbot", "Le père de famille, un homme d'une quarantaine d'années. Il semble tendu.", Sous_sol, 
        ["Bonjour", "Je m'appelle Lee"], can_move=True)
        self.character.append(Lee_Abbot)
        Sous_sol.characters[Lee_Abbot.name] = Lee_Abbot

        Regan_Abbot = Character("Regan Abbot", "la fille aînée de la famille Abbot, agée de 16 ans. Elle vous observe avec méfiance.", Maison_étage, 
        ["Bonjour", "Je m'appelle Regan"], can_move=True)
        self.character.append(Regan_Abbot)
        Maison_étage.characters[Regan_Abbot.name] = Regan_Abbot

        Evelyn_Abbot = Character("Evelyn Abbot", "la mère de la famille. Enceinte et très protectrice de ses enfants", Maison_étage, 
        ["Bonjour", "Je m'appelle Evelyn"], can_move=True)
        self.character.append(Evelyn_Abbot)
        Maison_étage.characters[Evelyn_Abbot.name] = Evelyn_Abbot

        Femme_dans_la_foret = Character("La femme dans la forêt", "une vieille dame perdue rendue folle par le deuil", forest,["Bonjour", "Je m'appelle... je ne me souviens plus"], can_move=True)
        self.character.append(Femme_dans_la_foret)
        forest.characters[Femme_dans_la_foret.name] = Femme_dans_la_foret

        # Setup player and starting room
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = Sous_sol

        # Setup quests
        def _setup_quests(self):
        """Initialize all quests."""
        key_quest = Quest(
            title="Obtenez la clé de l'étage",
            description="Parlez au personnage de la famille Abbot vous en apprendra plus sur ce monde",
            objectives=["Parler à Lee Abbot", "Aider le"],
            reward="clé-étage"
        )

        cables_quest = Quest(
            title="obtenez des câbles",
            description="Fouillez la voiture abandonnée",
            objectives=["Trouver le pied de biche","Entrer dans la voiture", "utiliser le pied de biche pour ouvrir le tableau de bord"],
            reward="câbles"
        )

        microphone_quest = Quest(
            title="Trouvez un microphone",
            description="Parvenez à entrer à l'étage pour trouver un microphone",
            objectives=["Obtenir la clé de l'étage", "Aller à l'étage"]
            reward="microphone"
        )

        # Add quests to player's quest manager
        self.player.quest_manager.add_quest(key_quest)
        self.player.quest_manager.add_quest(cables_quest)
        self.player.quest_manager.add_quest(microphone_quest)

    def play(self):
        """Play the game."""
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    def process_command(self, command_string) -> None:
        """Process the command entered by the player.
        Args:
            command_string (str): The command entered by the player.
        """
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

    def print_welcome(self):
        """Print the welcome message."""
        print(f"\nBienvenue {self.player.name} dans ce jeu d'horreur !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        print(self.player.current_room.get_long_description())


def main():
    """Create a game object and play the game."""
    Game().play()


if __name__ == "__main__":
    main()
