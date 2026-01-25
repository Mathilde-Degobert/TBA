# Description: Game class
""" This module contains the Game class which represents the game. """
# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quest import Quest
from end_conditions import EndConditions

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
        self.dialogue_steps = []

    # Setup the game
    def setup(self):
        """Setup the game rooms, items, characters, and player."""

        # Setup commands
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale \
        (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        history = Command("history", " : afficher l'historique des pièces visitées",\
        Actions.history, 0)
        self.commands["history"] = history
        back = Command("back", " : revenir au lieu précédent", Actions.go_back, 0)
        self.commands["back"] = back
        look = Command("look", " : regarder autour de vous", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <item> : prendre un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item> : déposer un objet de l'inventaire \
        dans la pièce", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : afficher le contenu de l'inventaire", Actions.check, 0)
        self.commands["check"] = check
        talk = Command("talk", " <character> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"] = talk
        use = Command("use", " <item> : utiliser un outil de l'inventaire", Actions.use, 1)
        self.commands["use"] = use
        quests = Command("quests", " : afficher la liste de toutes les quêtes", Actions.quests, 0)
        self.commands["quests"] = quests
        quest = Command("quest", " <nom> : afficher l'avancement d'une quête \
        spécifique", Actions.quest, 1)
        self.commands["quest"] = quest


        # Setup rooms
        forest = Room("forest", " un sentier sombre, au loin il y a une cabane abandonnée et "
        "le bruit assourdissant d'une cascade.")
        self.rooms.append(forest)

        Maison_rez_de_chaussée = Room("rez de chaussée", " une grande pièce abandonée, "
        "un silence lugubre règne. La seule trace de vie : "
        "des traces de passage dans la poussière du parquet qui menace de craquer à chaque pas.")
        self.rooms.append(Maison_rez_de_chaussée)

        Maison_étage = Room("étage", " une odeur de pourriture et de moisissure,"
        "un fin rayon de lumière révèle les lieux, autrement noyés par le noir. "
        "Les murs semblent écouter, vous retenez votre souffle.")
        self.rooms.append(Maison_étage)

        Champs = Room("champs", " un champs de maïs peu entrenu, "
        "un petit sentier de sable sillone les brins séchés. "
        "Devant vous apercevez un silo abandonné, abimé par le passage du temps."
        "Vous y voyez une plaque métalique qui semble bouger au vent.")
        self.rooms.append(Champs)

        Magasin = Room("magasin", " une ruelle au bitume éclatée, "
        "la devanture cassée révèle une superette aux rayons renversés.")
        self.rooms.append(Magasin)

        pont = Room("pont", " un grand pont un peu fissuré, plongé dans le silence."
        "Menaçant de s'effondrer à chaque pas.")
        self.rooms.append(pont)

        Voiture = Room("voiture", " une vielle cadillac bleu aux phares jaunies"
        "et à la carosserie cabossée. Sous le tableau de bord, des fils électriques pendent.")
        self.rooms.append(Voiture)

        Sous_sol = Room("sous-sol", " une pièce humide, plongée dans le noir, "
        "jonchée d'objets en tout genre.")
        self.rooms.append(Sous_sol)

        # Create exits for rooms
        forest.exits = {"N" : None, "E" : None, "S" : Maison_rez_de_chaussée,
        "O" : None, "U": None, "D": None}
        pont.exits = {"N" : None, "E" : Maison_rez_de_chaussée, "S" : None,
        "O" : Magasin, "U": None, "D": None}
        Magasin.exits = {"N" : None, "E" : pont, "S" : None, "O" : None, "U": None, "D": None }
        Champs.exits = {"N" : None, "E" : None, "S" : None, "O" : Maison_rez_de_chaussée,
        "U": None, "D": None}
        Maison_rez_de_chaussée.exits = {"N" : forest, "E" : None, "S" : Voiture, "O" : Champs,
        "U": Maison_étage, "D": Sous_sol}
        Maison_étage.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U": None,
        "D": Maison_rez_de_chaussée}
        Voiture.exits = {"N" : Maison_rez_de_chaussée , "E" : None, "S" : None, "O" : None,
        "U": None, "D": None}
        Sous_sol.exits = {"N" : None , "E" : None, "S" : None, "O" : None,
        "U": Maison_rez_de_chaussée, "D": None}

        # Verrouiller l'étage et le sous-sol
        Maison_étage.locked = True
        Maison_étage.locked_message = "La porte de l'étage est fermée à clé.\
        Vous avez besoin de la clé-étage pour l'ouvrir."
        Sous_sol.locked = True
        Sous_sol.locked_message = "L'escalier du sous-sol est bloqué\
        par une grille rouillée. Vous avez besoin des clés pour y accéder."

        # Setup items
        # Items trouvables sur la map
            # MATERIAUX
        Modulateur = Item("modulateur", "Module d'amplification (matériau)", 12)
        forest.items[Modulateur.name] = Modulateur
        Batterie = Item("batterie", "Vieille batterie (matériau)", 60)
        pont.items[Batterie.name] = Batterie
        Piles = Item("piles", "Boîte de 4 piles (matériau)", 10)
        Magasin.items[Piles.name] = Piles
        Table_bricolage = Item("table", "une table de bricolage avec \
        tous les outils nécessaires", 50000)
        Sous_sol.items[Table_bricolage.name] = Table_bricolage
            # OUTILS
        Clés_sous_sol = Item("clés", "les clés menant au sous-sol", 1)
        Voiture.items[Clés_sous_sol.name] = Clés_sous_sol
        pied_de_biche = Item("pied-de-biche", "Un pied-de-biche solide (outil)",
        4.0)
        pont.items[pied_de_biche.name] = pied_de_biche
        Sac_de_sable = Item("sac-de-sable", "Un sac de sable lourd --> peut \
        amortir le son de vos pas (outil)", 20.0)
        Sous_sol.items[Sac_de_sable.name] = Sac_de_sable

        # Récompenses de quêtes :
            # MATERIAUX
        CarteMere = Item("carte-mère", "Carte mère d'ordinateur (matériau)", 25)
        Microphone = Item("microphone", "Microphone de babyphone (matériau)", 15)
        Appareil_Auditif = Item("appareil-auditif", "Appareil auditif (matériau)", 8)
        Câbles = Item("câbles", "Des câbles électriques (matériau)", 5)
            # OUTILS
        Marteau = Item("marteau", "Un marteau robuste (outil)", 2.5)
        Tournevis = Item("tournevis", "Un tournevis multifonction (outil)", 1.5)
        Cle_a_molette = Item("clé-à-molette", "Une clé-à-molette (outil)", 3.0)
        Clé_Etage = Item("clé-étage", "la clé menant à l'étage (outil)", 1)
        Dispositif_ultrasons = Item("dispositif à ultrasons",
        "un dispositif à ultrasons (créé)", 8.0)

        # Rendre accessibles ces outils/récompenses dans setup_quests
        self.Marteau = Marteau
        self.Tournevis = Tournevis
        self.Cle_a_molette = Cle_a_molette
        self.Cle_Etage = Clé_Etage
        self.Câbles = Câbles
        self.Microphone = Microphone
        self.Appareil_Auditif = Appareil_Auditif
        self.CarteMere = CarteMere
        self.Dispositif_ultrasons = Dispositif_ultrasons

        # Setup Characters
        Beau_Abbot = Character("Beau Abbot","Le cadet de la famille Abbot,\
        agé d'a peine 4 ans. Il vous regarde de ses petits yeux innocents.",
        Maison_rez_de_chaussée,
        ["Bonjour...", "J'ai vu un monstre dehors... mais il dormait.'"],can_move=True)
        self.character.append(Beau_Abbot)
        Maison_rez_de_chaussée.characters[Beau_Abbot.name] = Beau_Abbot

        Marcus_Abbot = Character("Marcus Abbot", "Le deuxième fils de la famille Abbot,\
        agé de 12 ans. Il fuit votre regard, apeuré.", Maison_étage,
        ["...Moins de bruit.", "Ils entendent tout. Même nos pas."], can_move=True)
        self.character.append(Marcus_Abbot)
        Maison_étage.characters[Marcus_Abbot.name] = Marcus_Abbot

        Lee_Abbot = Character("Lee Abbot", "Le père de famille, un homme d'une quarantaine\
        d'années. Il semble tendu.", Sous_sol,
        ["Rebonjour ! Encore Merci pour votre aide. Je peux vous prêter un outil\
         si vous avez besoin. \nLequel de ces outils veux-tu ?"], can_move=True)
        self.character.append(Lee_Abbot)
        Sous_sol.characters[Lee_Abbot.name] = Lee_Abbot
        Lee_Abbot.tool_choices = {
            "Marteau": Marteau,
            "Tournevis": Tournevis,
            "Clé-à-molette": Cle_a_molette
        }

        Regan_Abbot = Character("Regan Abbot", "la fille aînée de la famille Abbot,\
         agée de 16 ans. Elle vous observe avec méfiance.", Maison_rez_de_chaussée,
        ["Ne le pers pas... c'est rare.", "Fais attention à toi."], can_move=True)
        self.character.append(Regan_Abbot)
        Maison_rez_de_chaussée.characters[Regan_Abbot.name] = Regan_Abbot

        Evelyn_Abbot = Character("Evelyn Abbot", "la mère de la famille.\
        Enceinte et très protectrice de ses enfants", Magasin,
        ["Chut... fais attention où tu mets les pieds.",
        "Je fouille depuis des heures... il reste presque plus rien."], can_move=True)
        self.character.append(Evelyn_Abbot)
        Magasin.characters[Evelyn_Abbot.name] = Evelyn_Abbot

        Femme_dans_la_foret = Character("La femme dans la forêt",
        "une vieille dame perdue rendue folle par le deuil", forest,
        ["Bonjour", "Je m'appelle... je ne me souviens plus"], can_move=True)
        self.character.append(Femme_dans_la_foret)
        forest.characters[Femme_dans_la_foret.name] = Femme_dans_la_foret

        # Setup player and starting room
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = pont

        # Setup quests
        self.setup_quests()

    def setup_quests(self):
        """Setup the quests for the game."""
        key_quest = Quest(
            title="1 - Obtenir la clé-étage",
            description="Parler aux personnages de la famille Abbot\
            vous en apprendra plus sur ce monde",
            objectives=[
                "Parler à Lee Abbot",
                "Aider Lee"
            ],
            character = "Lee Abbot",
            dialogue = [
                ("Lee Abbott est occupé à installer de l'isolant sur les murs du sous-sol.\n \
                Il vous aperçoit et vous demande :'Qu'est-ce que tu veux ?'", None),
                ("Lee Abbott sourit avec soulagement et vous dit : 'C'est gentil !\
                Tu peux m'aider à tenir les panneaux ? Avec toi, ce sera beaucoup plus facile.'",
                "Puis-je vous aider ?"),
                ("Vous avez aidé Lee Abbott à installer l'isolant. Après plusieurs heures,\
                le travail est enfin terminé.\nIl vous remercie chaleureusement et vous dit :\
                'Installe-toi à l'étage si tu veux.\nLa pièce n'est pas utilisée par la famille.\
                Tu y trouveras refuge.'", "Puis-je vous aider ?")
            ],
            choices =  [["Puis-je vous aider ?", "Que faites-vous ici ?",
            "Je n'ai besoin de rien." ], [], []],
            correct_choices = [["Puis-je vous aider ?"], [], []],
            reward = self.Cle_Etage

        )

        cables_quest = Quest(
            title="2 - Obtenir les câbles",
            description="Fouiller la voiture abandonnée pourrait vous être utile",
            objectives=["Trouver un pied-de-biche","Entrer dans la voiture",
            "Utiliser le pied-de-biche"],
            character = None,
            dialogue = [],
            choices =  [],
            correct_choices = [],
            reward= self.Câbles
        )

        microphone_quest = Quest(
            title="3 - Trouver le microphone",
            description="Parvenez à entrer à l'étage pour faire une découverte importante",
            objectives=["Obtenir la clé-étage", "Aller à l'étage", "Utiliser la clé-étage"],
            character = None,
            dialogue = [],
            choices =  [],
            correct_choices = [],
            reward= self.Microphone
        )


        piles_quest = Quest(
            title="4 - Trouver les piles",
            description="Explorer le magasin abandonné pourrait vous permettre\
            de trouver des piles",
            objectives=["Entrer dans le magasin", "Trouver les piles"],
            character = None,
            dialogue = [],
            choices =  [],
            correct_choices = [],
            reward= None
        )

        batterie_quest = Quest(
            title="5 - Trouver la batterie",
            description="Chercher sur le pont pourrait vous permettre\
            de trouver une batterie",
            objectives=["Explorer le pont", "Trouver la batterie"],
            character = None,
            dialogue = [],
            choices =  [],
            correct_choices = [],
            reward= None
        )

        appareil_auditif_quest = Quest(
            title="6 - Obtenir l'appareil auditif",
            description="Parler à Regan pourrait vous aider",
            objectives=["Parler à Regan Abbot", "Aider Regan" ],
            character = "Regan Abbot",
            dialogue = [
                ("Regan Abbot semble préoccupée et vous dit :'Je ne trouve plus mon appareil\
                auditif. Sans lui, je n'entends rien dans cette maison sombre et silencieuse.'",
                None),
                ("Après avoir cherché avec Regan, vous trouvez son appareil auditif sous un \
                meuble.\nElle vous remercie chaleureusement et vous dit : 'Merci beaucoup !\
                Tu es vraiment gentil(le).'", "Puis-je vous aider ?")
            ],
            choices =  [["Puis-je vous aider ?", "Que faites-vous ici ?",
            "Je n'ai besoin de rien." ], []],
            correct_choices = [["Puis-je vous aider ?"], []],
            reward= self.Appareil_Auditif
        )

        carte_mere_quest = Quest(
            title="7 - Obtenir la carte-mère",
            description="Chercher dans les champs pourrait vous permettre\
            de trouver une carte-mère",
            objectives=["Obtenir la clé-à-molette", "Aller dans les champs",
            "Utiliser la clé-à-molette"],
            character = None,
            dialogue = [],
            choices =  [],
            correct_choices = [],
            reward= self.CarteMere
        )

        modulateur_quest = Quest(
            title="8 - Trouver le modulateur",
            description="Chercher dans la forêt pourrait vous permettre de trouver un modulateur",
            objectives=["Explorer la forêt", "Trouver le modulateur"],
            character = None,
            dialogue = [],
            choices =  [],
            correct_choices = [],
            reward= None
        )

        dispositif_ultrasons_quest = Quest(
            title="9 - Construire le dispositif à ultrasons",
            description="Rassembler tous les matériaux pour construire le dispositif à ultrasons",
            objectives=[
                "Obtenir le tournevis",
                "Obtenir la batterie",
                "Obtenir les piles",
                "Obtenir les câbles",
                "Obtenir le microphone",
                "Obtenir l'appareil auditif",
                "Obtenir la carte-mère",
                "Utiliser le tournevis"
            ],
            character = None,
            dialogue = [],
            choices =  [],
            correct_choices = [],
            reward= self.Dispositif_ultrasons
        )

        # Add quests to player's quest manager
        self.player.quest_manager.add_quest(key_quest)
        self.player.quest_manager.add_quest(cables_quest)
        self.player.quest_manager.add_quest(microphone_quest)
        self.player.quest_manager.add_quest(piles_quest)
        self.player.quest_manager.add_quest(batterie_quest)
        self.player.quest_manager.add_quest(appareil_auditif_quest)
        self.player.quest_manager.add_quest(carte_mere_quest)
        self.player.quest_manager.add_quest(modulateur_quest)
        self.player.quest_manager.add_quest(dispositif_ultrasons_quest)

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

        # Vérifier les conditions de victoire après chaque commande
        if EndConditions.check_victory_conditions(self):
            EndConditions.trigger_victory(self)

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
