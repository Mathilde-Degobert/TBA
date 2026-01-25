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
        cmd_help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = cmd_help
        cmd_quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = cmd_quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale"
                    " (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        history = Command("history", " : afficher l'historique des pièces visitées",
                 Actions.history, 0)
        self.commands["history"] = history
        back = Command("back", " : revenir au lieu précédent", Actions.go_back, 0)
        self.commands["back"] = back
        look = Command("look", " : regarder autour de vous", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <item> : prendre un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item> : déposer un objet de l'inventaire"
                      " dans la pièce", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : afficher le contenu de l'inventaire", Actions.check, 0)
        self.commands["check"] = check
        talk = Command("talk", " <character> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"] = talk
        use = Command("use", " <item> : utiliser un outil de l'inventaire", Actions.use, 1)
        self.commands["use"] = use
        quests = Command("quests", " : afficher la liste de toutes les quêtes", Actions.quests, 0)
        self.commands["quests"] = quests
        quest = Command("quest", " <nom> : afficher l'avancement d'une quête"
                       " spécifique", Actions.quest, 1)
        self.commands["quest"] = quest



        # Setup rooms
        forest = Room("forest", " un sentier sombre, au loin il y a une cabane abandonnée et "
        "le bruit assourdissant d'une cascade.")
        self.rooms.append(forest)

        maison_rez_de_chaussee = Room("rez de chaussée", " une grande pièce abandonée, "
        "un silence lugubre règne. La seule trace de vie : "
        "des traces de passage dans la poussière du parquet qui menace de craquer à chaque pas.")
        self.rooms.append(maison_rez_de_chaussee)

        maison_etage = Room("étage", " une odeur de pourriture et de moisissure, "
        "un fin rayon de lumière révèle les lieux, autrement noyés par le noir. "
        "Les murs semblent écouter, vous retenez votre souffle.")
        self.rooms.append(maison_etage)

        champs = Room("champs", " un champs de maïs peu entrenu, "
        "un petit sentier de sable sillone les brins séchés. "
        "Devant vous apercevez un silo abandonné, abimé par le passage du temps."
        "Vous y voyez une plaque métalique qui semble bouger au vent.")
        self.rooms.append(champs)

        magasin = Room("magasin", " une ruelle au bitume éclatée, "
        "la devanture cassée révèle une superette aux rayons renversés.")
        self.rooms.append(magasin)

        pont = Room("pont", " un grand pont un peu fissuré, plongé dans le silence. "
        "Menaçant de s'effondrer à chaque pas.")
        self.rooms.append(pont)

        voiture = Room("voiture", " une vielle cadillac bleu aux phares jaunies "
        "et à la carosserie cabossée. Sous le tableau de bord, des fils électriques pendent.")
        self.rooms.append(voiture)

        sous_sol = Room("sous-sol", " une pièce humide, plongée dans le noir, "
        "jonchée d'objets en tout genre.")
        self.rooms.append(sous_sol)

        # Create exits for rooms
        forest.exits = {"N" : None, "E" : None, "S" : maison_rez_de_chaussee,
        "O" : None, "U": None, "D": None}
        pont.exits = {"N" : None, "E" : maison_rez_de_chaussee, "S" : None,
        "O" : magasin, "U": None, "D": None}
        magasin.exits = {"N" : None, "E" : pont, "S" : None, "O" : None, "U": None, "D": None }
        champs.exits = {"N" : None, "E" : None, "S" : None, "O" : maison_rez_de_chaussee,
        "U": None, "D": None}
        maison_rez_de_chaussee.exits = {"N" : forest, "E" : champs, "S" : voiture, "O" : pont,
        "U": maison_etage, "D": sous_sol}
        maison_etage.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U": None,
        "D": maison_rez_de_chaussee}
        voiture.exits = {"N" : maison_rez_de_chaussee , "E" : None, "S" : None, "O" : None,
        "U": None, "D": None}
        sous_sol.exits = {"N" : None , "E" : None, "S" : None, "O" : None,
        "U": maison_rez_de_chaussee, "D": None}

        # Verrouiller l'étage et le sous-sol
        maison_etage.locked = True
        maison_etage.locked_message = ("La porte de l'étage est fermée à clé."
                                       " Vous avez besoin de la clé-étage pour l'ouvrir.")
        sous_sol.locked = True
        sous_sol.locked_message = ("L'escalier du sous-sol est bloqué"
                                   " par une grille rouillée. Vous avez"
                                   " besoin des clés pour y accéder.")

        # Setup items
        # Items trouvables sur la map
        # MATERIAUX
        modulateur = Item("modulateur", "Module d'amplification (matériau)", 12)
        forest.items[modulateur.name] = modulateur
        batterie = Item("batterie", "Vieille batterie (matériau)", 60)
        pont.items[batterie.name] = batterie
        piles = Item("piles", "Boîte de 4 piles (matériau)", 10)
        magasin.items[piles.name] = piles
        table_bricolage = Item("table", "une table de bricolage avec"
                                        " tous les outils nécessaires", 50000)
        sous_sol.items[table_bricolage.name] = table_bricolage
        # OUTILS
        cles_sous_sol = Item("clés", "les clés menant au sous-sol", 1)
        voiture.items[cles_sous_sol.name] = cles_sous_sol
        pied_de_biche = Item("pied-de-biche", "Un pied-de-biche solide (outil)",
        4.0)
        pont.items[pied_de_biche.name] = pied_de_biche
        sac_de_sable = Item("sac-de-sable", "Un sac de sable lourd --> peut"
                                           " amortir le son de vos pas (outil)", 20.0)
        sous_sol.items[sac_de_sable.name] = sac_de_sable

        # Récompenses de quêtes :
        # MATERIAUX
        carte_mere = Item("carte-mère", "Carte mère d'ordinateur (matériau)", 25)
        microphone = Item("microphone", "Microphone de babyphone (matériau)", 15)
        appareil_auditif = Item("appareil-auditif", "Appareil auditif (matériau)", 8)
        cables = Item("câbles", "Des câbles électriques (matériau)", 5)
        # OUTILS
        marteau = Item("marteau", "Un marteau robuste (outil)", 2.5)
        tournevis = Item("tournevis", "Un tournevis multifonction (outil)", 1.5)
        cle_a_molette = Item("clé-à-molette", "Une clé-à-molette (outil)", 3.0)
        cle_etage = Item("clé-étage", "la clé menant à l'étage (outil)", 1)
        dispositif_ultrasons = Item("dispositif à ultrasons",
        "un dispositif à ultrasons (créé)", 8.0)

        # Rendre accessibles ces outils/récompenses dans setup_quests
        self.marteau = marteau
        self.tournevis = tournevis
        self.cle_a_molette = cle_a_molette
        self.cle_etage = cle_etage
        self.cables = cables
        self.microphone = microphone
        self.appareil_auditif = appareil_auditif
        self.carte_mere = carte_mere
        self.dispositif_ultrasons = dispositif_ultrasons

        # Setup Characters
        beau_abbot = Character("Beau Abbot", "Le cadet de la famille Abbot,"
                       " agé d'a peine 4 ans. Il vous regarde"
                       " de ses petits yeux innocents.",
                       maison_rez_de_chaussee,
                       ["Bonjour...", "J'ai vu un monstre dehors... mais il dormait.'"],
                       can_move=True)
        self.character.append(beau_abbot)
        maison_rez_de_chaussee.characters[beau_abbot.name] = beau_abbot

        marcus_abbot = Character("Marcus Abbot", "Le deuxième fils de la famille Abbot,"
                     " agé de 12 ans. Il fuit votre regard, apeuré.",
                     maison_etage,
                     ["...Moins de bruit.", "Ils entendent tout. Même nos pas."],
                     can_move=True)
        self.character.append(marcus_abbot)
        maison_etage.characters[marcus_abbot.name] = marcus_abbot

        lee_abbot = Character("Lee Abbot", "Le père de famille, un homme d'une quarantaine"
                         " d'années. Il semble tendu.", sous_sol,
                     ["Rebonjour ! Encore Merci pour votre aide. Je peux vous prêter un outil"
                      " si vous avez besoin. \nLequel de ces outils veux-tu ?"],
                     can_move=True)
        self.character.append(lee_abbot)
        sous_sol.characters[lee_abbot.name] = lee_abbot
        lee_abbot.tool_choices = {
            "Marteau": marteau,
            "Tournevis": tournevis,
            "Clé-à-molette": cle_a_molette
        }

        regan_abbot = Character("Regan Abbot", "la fille aînée de la famille Abbot,"
                     " agée de 16 ans. Elle vous observe avec méfiance.",
                     maison_rez_de_chaussee,
                     ["Ne le pers pas... c'est rare.", "Fais attention à toi."],
                     can_move=True)
        self.character.append(regan_abbot)
        maison_rez_de_chaussee.characters[regan_abbot.name] = regan_abbot

        evelyn_abbot = Character("Evelyn Abbot", "la mère de la famille."
                     " Enceinte et très protectrice de ses enfants",
                     magasin,
                     ["Chut... fais attention où tu mets les pieds.",
                      "Je fouille depuis des heures... il reste presque plus rien."],
                     can_move=True)
        self.character.append(evelyn_abbot)
        magasin.characters[evelyn_abbot.name] = evelyn_abbot

        femme_dans_la_foret = Character("La femme dans la forêt",
                        "une vieille dame perdue rendue folle par le deuil",
                        forest,
                        ["Bonjour", "Je m'appelle... je ne me souviens plus"],
                        can_move=True)
        self.character.append(femme_dans_la_foret)
        forest.characters[femme_dans_la_foret.name] = femme_dans_la_foret

        # Setup player and starting room
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = maison_rez_de_chaussee

        # Setup quests
        self.setup_quests()

    def setup_quests(self):
        """Setup the quests for the game."""
        key_quest = Quest(
            title="1 - Obtenir la clé-étage",
            description="Parler aux personnages de la famille Abbot"
                       " vous en apprendra plus sur ce monde",
            objectives=[
                "Parler à Lee Abbot",
                "Aider Lee"
            ],
            character = "Lee Abbot",
            dialogue = [
                ("Lee Abbott est occupé à installer de l'isolant sur les murs du sous-sol.\n"
                " Il vous aperçoit et vous demande :'Qu'est-ce que tu veux ?'", None),
                ("Lee Abbott sourit avec soulagement et vous dit : 'C'est gentil !"
                " Tu peux m'aider à tenir les panneaux ? Avec toi, ce sera beaucoup plus facile.'",
                "Puis-je vous aider ?"),
                ("Vous avez aidé Lee Abbott à installer l'isolant. Après plusieurs heures,"
                " le travail est enfin terminé.\nIl vous remercie chaleureusement et vous dit :"
                " 'Installe-toi à l'étage si tu veux.\nLa pièce n'est pas utilisée par la famille."
                " Tu y trouveras refuge.'", "Puis-je vous aider ?")
            ],
            choices =  [["Puis-je vous aider ?", "Que faites-vous ici ?",
            "Je n'ai besoin de rien." ], [], []],
            correct_choices = [["Puis-je vous aider ?"], [], []],
            reward = self.cle_etage

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
            reward= self.cables
        )

        microphone_quest = Quest(
            title="3 - Trouver le microphone",
            description="Parvenez à entrer à l'étage pour faire une découverte importante",
            objectives=["Obtenir la clé-étage", "Aller à l'étage", "Utiliser la clé-étage"],
            character = None,
            dialogue = [],
            choices =  [],
            correct_choices = [],
            reward= self.microphone
        )


        piles_quest = Quest(
            title="4 - Trouver les piles",
            description="Explorer le magasin abandonné pourrait vous permettre"
                       " de trouver des piles",
            objectives=["Entrer dans le magasin", "Trouver les piles"],
            character = None,
            dialogue = [],
            choices =  [],
            correct_choices = [],
            reward= None
        )

        batterie_quest = Quest(
            title="5 - Trouver la batterie",
            description="Chercher sur le pont pourrait vous permettre"
                       " de trouver une batterie",
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
                ("Regan Abbot semble préoccupée et vous dit :'Je ne trouve plus mon appareil"
                " auditif. Sans lui, je n'entends rien dans cette maison sombre et silencieuse.'",
                None),
                ("Après avoir cherché avec Regan, vous trouvez son appareil auditif sous un"
                " meuble.\nElle vous remercie chaleureusement et vous dit : 'Merci beaucoup !"
                " Tu es vraiment gentil(le).'", "Puis-je vous aider ?")
            ],
            choices =  [["Puis-je vous aider ?", "Que faites-vous ici ?",
            "Je n'ai besoin de rien." ], []],
            correct_choices = [["Puis-je vous aider ?"], []],
            reward= self.appareil_auditif
        )

        carte_mere_quest = Quest(
            title="7 - Obtenir la carte-mère",
            description="Chercher dans les champs pourrait vous permettre"
                       " de trouver une carte-mère",
            objectives=["Obtenir la clé-à-molette", "Aller dans les champs",
            "Utiliser la clé-à-molette"],
            character = None,
            dialogue = [],
            choices =  [],
            correct_choices = [],
            reward= self.carte_mere
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
            reward= self.dispositif_ultrasons
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
