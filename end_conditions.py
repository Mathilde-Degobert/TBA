"""
Module de gestion des conditions de fin de jeu (victoire et défaite).
"""

class EndConditions:
    """Gère les conditions de fin de partie."""

    # Raisons de défaite possibles
    DEFEAT_FOREST_WOMAN = "Hurlée par la femme dans la forêt"
    DEFEAT_DEAD_BRANCHES = "Bruit de branches dans le champs"
    DEFEAT_MONSTER = "Attaqué par un monstre"
    DEFEAT_TRAP = "Piégé"

    @staticmethod
    def trigger_defeat(game, reason=None):
        """
        Déclenche une défaite et termine la partie.
        Args:
            game (Game): L'objet du jeu.
            reason (str): Raison de la défaite (optionnel).
        """
        print("──────────────────────────────────────────")
        print("               DÉFAITE  ")
        print("──────────────────────────────────────────")
        if reason:
            print(f"\nCause: {reason}\n")
        print("Vous êtes mort(e). La partie est terminée.\n")
        game.finished = True

    @staticmethod
    def check_defeat_forest_woman(game, character):
        """
        Vérifier si le joueur parle à la femme dans la forêt.
        Args:
            game (Game): L'objet du jeu.
            character (Character): Le personnage avec lequel parler.
        Returns:
            bool: True si défaite déclenchée, False sinon.
        """
        if character.name.lower() == "la femme dans la forêt":
            print("\n" + "─" * 60)
            print("La femme dans la forêt vous fixe de ses yeux vides,")
            print("puis pousse un hurlement strident et glaçant.\n")
            print("Le cri résonne à travers les arbres et attire des créatures.")
            print("Vous tentez de fuir, mais elles vous rattrapent...\n")
            print("─" * 60 + "\n")
            EndConditions.trigger_defeat(game, EndConditions.DEFEAT_FOREST_WOMAN)
            return True
        return False

    @staticmethod
    def check_defeat_hazards(game, tool_name=None):
        """
        Vérifier les dangers contextuels selon la localisation.
        Si un outil est fourni et que son utilisation échoue, affiche un message dramatique.
        Args:
            game (Game): L'objet du jeu.
            tool_name (str): Le nom de l'outil utilisé (optionnel).
        Returns:
            bool: True si défaite déclenchée, False sinon.
        """
        import random
        current_room = game.player.current_room
        if not current_room:
            return False
        
        room_name = current_room.name.lower()
        
        # Si un outil est fourni, afficher un message dramatique
        if tool_name:
            print("\n" + "─" * 60)
            print(f"Vous tentez d'utiliser {tool_name} de façon inappropriée...")
            print("Un bruit sourd résonne à travers la maison.")
            print("Le silence qui suit est encore plus terrifiant...\n")
            print("Des mouvements s'accélèrent partout autour de vous.")
            print("Des créatures émergent des ténèbres, attirées par le bruit.")
            print("Vous tentez de fuir, mais elles vous encerclent...\n")
            print("─" * 60 + "\n")
            EndConditions.trigger_defeat(game, f"Mauvaise utilisation de {tool_name}")
            return True
        
        # Danger: branches mortes dans le champs - évitable avec la clé à molette
        if room_name == "champs":
            # Vérifier si le joueur a la clé à molette pour se protéger
            has_protection = "clé-molette" in game.player.inventory or "clé à molette" in [item.lower() for item in game.player.inventory.keys()]
            
            if not has_protection:
                # Sans protection, risque de 40% de déclencher le danger
                if random.random() < 0.4:
                    print("\n" + "─" * 60)
                    print("Vous marchez sans précaution à travers le champs.")
                    print("Vous marchez sur des branches mortes:")
                    print("le craquement retentit dans le silence.\n")
                    print("Au loin, vous entendez des mouvements précipités...")
                    print("Des créatures approchent, attirées par le bruit.\n")
                    print("Vous courez, mais elles vous rattrapent...\n")
                    print("─" * 60 + "\n")
                    EndConditions.trigger_defeat(game, EndConditions.DEFEAT_DEAD_BRANCHES)
                    return True
            else:
                # Avec la clé à molette, message rassurant
                print("\nVous utilisez la clé à molette pour vous frayer un chemin silencieux à travers le champs.")
                print("Aucune créature ne vous remarque.\n")
        
        return False

    @staticmethod
    def check_victory_conditions(game):
        """
        Vérifier les conditions de victoire.
        Args:
            game (Game): L'objet du jeu.
        Returns:
            bool: True si victoire, False sinon.
        """
        # Victoire: avoir le dispositif à ultrasons dans l'inventaire
        player_items = [item.lower() for item in game.player.inventory.keys()]
        
        if "dispositif à ultrasons" in player_items or "dispositif-à-ultrasons" in player_items:
            return True
        return False

    @staticmethod
    def trigger_victory(game):
        """
        Déclenche une victoire et termine la partie.
        Args:
            game (Game): L'objet du jeu.
        """
        print("\n" + "-" * 60)
        print("               VICTOIRE  ")
        print("-" * 60)
        print("\nVous avez réuni tous les matériaux nécessaires!")
        print("Le dispositif à ultrasons est construit avec succès.")
        print("\nVous criez de toutes vos forces pour attirer les créatures.")
        print("Elles accourent de partout, prêtes à vous dévorer...\n")
        print("Vous allumez alors le dispositif à ultrasons devant les haut-parleurs!")
        print("Le son retentit tout autour de la maison, perçant et insupportable.\n")
        print("Les créatures s'effondrent, transpercées par les ultrasons.")
        print("Elles disparaissent dans les ténèbres, anéanties.\n")
        print("Vous avez sauvé la famille Abbott et ressortez vivant de cette histoire...!")
        print("Félicitations, vous avez gagné!\n")
        game.finished = True
