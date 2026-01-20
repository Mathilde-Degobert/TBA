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
        use = Command("use", " <item> : utiliser un objet de l'inventaire", Actions.use, 1) 
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
      
        # Setup items - MATÉRIAUX trouvables sur la map
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

        # Setup items - OBJETS SPÉCIAUX
        Clés_sous_sol = Item("clés", "les clés menant au sous-sol", 1)
        Voiture.items[Clés_sous_sol.name] = Clés_sous_sol
        
        Clés_Etage = Item("clés-étage", "les clés menant à l'étage", 1)
        
        # Table de bricolage (pour l'assemblage du dispositif)
        Table_bricolage = Item("table", "une table de bricolage avec tous les outils nécessaires", 1000)
        Sous_sol.items[Table_bricolage.name] = Table_bricolage

        # Dispositif d'ultrasons (créé par crafting)
        Dispositif_ultrasons = Item("dispositif", "un dispositif à ultrasons (créé)", 8.0)
        
        # Items pour les récompenses de dialogue
        Microphone = Item("microphone", "Microphone de babyphone (matériau)", 15)
        AppareilAuditif = Item("appareil-auditif", "Appareil auditif ancien (matériau)", 8)
        
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

        #setup quests
        # Quête Principale: Assembler le dispositif d'ultrasons
        Quest_step_assembler = [
            QuestStep(
                "Assemblez le dispositif d'ultrasons au sous-sol sur la table de bricolage.",
                character=None,
                quest_responses=["Vous avez assemblé le dispositif d'ultrasons avec succès !"],
                reward_item=Dispositif_ultrasons
            ),
        ]
        Quete_assembler = Quest("Assembler le dispositif d'ultrasons",
                               "Collectez tous les matériaux et utilisez les outils sur la table de bricolage au sous-sol.",
                               Quest_step_assembler,
                               is_main_quest=True)
        self.quests.append(Quete_assembler)
        
        # Items pour les outils (récompenses de quête)
        Marteau = Item("marteau", "Un marteau robuste (outil)", 2.5)
        Tournevis = Item("tournevis", "Un tournevis multifonction (outil)", 1.5)
        Cle_a_molette = Item("clé-molette", "Une clé à molette (outil)", 3.0)
        
        # Quête 1: Aider Lee Abbott (dialogue avec choix multiples)
        Quest_step_lee_1 = QuestStep(
            "Lee Abbott est occupé à installer de l'isolant sur les murs du sous-sol. Il vous aperçoit et vous demande : 'Qu'est-ce que tu veux ?'",
            character="Lee Abbot",
            quest_responses=["Lee Abbott vous regarde en attendant votre réponse."],
            choices=[
                ["Puis-je vous aider ?", "Pouvez-vous me prêter un outil ?", "Je n'ai besoin de rien."]
            ],
            correct_choices=[
                ["Puis-je vous aider ?", "Pouvez-vous me prêter un outil ?"]
            ],
        )
        
        Quest_step_lee_2_help = QuestStep(
            "Lee Abbott sourit avec soulagement et vous dit : 'C'est gentil ! Tu peux m'aider à tenir les panneaux ? Avec toi, ce sera beaucoup plus facile.'",
            character="Lee Abbot",
            quest_responses=["Vous avez aidé Lee Abbott à installer l'isolant. Après plusieurs heures, le travail est enfin terminé. Il vous remercie chaleureusement et vous dit : 'Installe-toi à l'étage si tu veux. La pièce n'est pas utilisée par la famille. Tu y trouveras refuge.'"],
            choices=[],
            correct_choices=[],
            reward_item=Clés_Etage
        )
        
        # Créer une quête unique pour Lee Abbott
        Quete_lee = Quest("Interagir avec Lee Abbott",
                         "Lee Abbott demande de l'aide pour installer l'isolant.",
                         [Quest_step_lee_1, Quest_step_lee_2_help],
                         is_main_quest=False)
        
        self.quests.append(Quete_lee)
        
        # Quête 2: Trouver le modulateur dans la forêt
        Quest_step_modulateur = [
            QuestStep(
                "Vous êtes dans la forêt. Vous apercevez un vieux modulateur d'amplification caché sous des feuilles. Qu'allez-vous faire ?",
                character="La femme dans la forêt",
                quest_responses=["Vous avez trouvé le modulateur d'amplification !"],
                choices=[
                    ["Prendre le modulateur", "Demander à la femme", "Repartir"],
                ],
                correct_choices=[
                    ["Prendre le modulateur"]
                ],
                reward_item=Modulateur
            ),
        ]
        Quete_modulateur = Quest("Chercher le modulateur",
                                "Trouvez le modulateur d'amplification dans la forêt.",
                                Quest_step_modulateur,
                                is_main_quest=False)
        self.quests.append(Quete_modulateur)
        
        # Quête 3: Obtenir la batterie
        Quest_step_batterie = [
            QuestStep(
                "Sur le pont, vous trouvez une batterie. Elle semble encore en bon état. Voulez-vous la prendre ?",
                character=None,
                quest_responses=["Vous avez récupéré la batterie."],
                choices=[
                    ["Oui, prendre la batterie", "Non, ce n'est pas sûr", "Vérifier d'abord"]
                ],
                correct_choices=[
                    ["Oui, prendre la batterie", "Vérifier d'abord"]
                ],
                reward_item=Batterie
            ),
        ]
        Quete_batterie = Quest("Récupérer la batterie",
                              "Trouvez la batterie sur le pont.",
                              Quest_step_batterie,
                              is_main_quest=False)
        self.quests.append(Quete_batterie)
        
        # Quête 4: Obtenir les piles
        Quest_step_piles = [
            QuestStep(
                "Au magasin, vous trouvez des piles. Elles se trouvent sur une étagère fragile. Soyez prudent.",
                character=None,
                quest_responses=["Vous avez récupéré les piles sans faire de dégâts."],
                choices=[
                    ["Prendre les piles doucement", "Les arracher brutalement", "Appeler quelqu'un"]
                ],
                correct_choices=[
                    ["Prendre les piles doucement"]
                ],
                reward_item=Piles
            ),
        ]
        Quete_piles = Quest("Trouver les piles",
                           "Trouvez les piles au magasin.",
                           Quest_step_piles,
                           is_main_quest=False)
        self.quests.append(Quete_piles)
        
        # Quête 5: Obtenir les câbles dans la voiture
        Quest_step_cables = [
            QuestStep(
                "Dans la voiture, vous découvrez des câbles électriques. Ils semblent connectés à quelque chose.",
                character=None,
                quest_responses=["Vous avez extrait les câbles avec précaution."],
                choices=[
                    ["Débrancher et prendre", "Couper les câbles", "Étudier d'abord"],
                ],
                correct_choices=[
                    ["Débrancher et prendre"]
                ],
                reward_item=Câbles
            ),
        ]
        Quete_cables = Quest("Extraire les câbles",
                            "Trouvez les câbles électriques dans la voiture.",
                            Quest_step_cables,
                            is_main_quest=False)
        self.quests.append(Quete_cables)
        
        # Quête 6: Obtenir le microphone
        Quest_step_microphone = [
            QuestStep(
                "Vous parlez à Marcus Abbot. Il semble avoir un microphone ancien.",
                character="Marcus Abbot",
                quest_responses=["Marcus vous donne le microphone."],
                choices=[
                    ["Le demander poliment", "Lui l'enlever de force", "Lui proposer un échange"],
                ],
                correct_choices=[
                    ["Le demander poliment", "Lui proposer un échange"]
                ],
                reward_item=Microphone
            ),
        ]
        Quete_microphone = Quest("Récupérer le microphone",
                                "Parlez à Marcus Abbot pour obtenir le microphone.",
                                Quest_step_microphone,
                                is_main_quest=False)
        self.quests.append(Quete_microphone)
        
        # Quête 7: Obtenir l'appareil auditif
        Quest_step_auditif = [
            QuestStep(
                "Vous trouvez Evelyn Abbot. Elle possède un vieil appareil auditif.",
                character="Evelyn Abbot",
                quest_responses=["Evelyn vous donne l'appareil auditif."],
                choices=[
                    ["Expliquer vos intentions", "Prétendre avoir besoin", "Rester muet"],
                ],
                correct_choices=[
                    ["Expliquer vos intentions"]
                ],
                reward_item=AppareilAuditif
            ),
        ]
        Quete_auditif = Quest("Localiser l'appareil auditif",
                             "Parlez à Evelyn Abbot pour obtenir l'appareil auditif.",
                             Quest_step_auditif,
                             is_main_quest=False)
        self.quests.append(Quete_auditif)
        
        # Quête 8: Obtenir la carte mère
        Quest_step_cartmere = [
            QuestStep(
                "Vous trouvez une carte mère dans les champs. Elle est poussiéreuse mais semble intacte.",
                character=None,
                quest_responses=["Vous avez récupéré la carte mère."],
                choices=[
                    ["La nettoyer puis la prendre", "La prendre directement", "La laisser ici"],
                ],
                correct_choices=[
                    ["La nettoyer puis la prendre"]
                ],
                reward_item=CarteMere
            ),
        ]
        Quete_cartmere = Quest("Trouver la carte mère",
                              "Trouvez la carte mère dans les champs.",
                              Quest_step_cartmere,
                              is_main_quest=False)
        self.quests.append(Quete_cartmere)

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
