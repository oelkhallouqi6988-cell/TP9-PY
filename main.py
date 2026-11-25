from models import Produit, Client
from sqlite_dao import SQLiteDAO
from mysql_dao import MySQLDAO


def afficher_menu():
    print("\n========== BOUTIQUE ==========")
    print("1. Ajouter un produit")
    print("2. Lister les produits")
    print("3. Modifier le prix d'un produit")
    print("4. Ajouter un client")
    print("5. Lister les clients")
    print("6. Rechercher un client par email")
    print("0. Quitter")
    print("==============================")


def main():

    print("Choisissez le type de base de données :")
    print("1. SQLite")
    print("2. MySQL")

    choix_db = input("Votre choix : ")

    if choix_db == "1":
        dao = SQLiteDAO()
        print("\nBase SQLite sélectionnée.")

    elif choix_db == "2":
        print("\nConnexion MySQL...")

        dao = MySQLDAO(
            host="localhost",
            user="root",
            password="G131006988"
        )

        print("Base MySQL sélectionnée.")

    else:
        print("Choix invalide.")
        return

    while True:

        afficher_menu()
        choix = input("Votre choix : ")

        # Ajouter produit
        if choix == "1":
            nom = input("Nom du produit : ")

            try:
                prix = float(input("Prix : "))
                produit = Produit(None, nom, prix)
                dao.ajouter_produit(produit)

            except ValueError:
                print("Erreur : le prix doit être numérique.")

        # Lister produits
        elif choix == "2":
            produits = dao.lister_produits()

            if not produits:
                print("Aucun produit.")

            else:
                print("\n--- Liste des produits ---")
                for produit in produits:
                    print(produit)

        # Modifier prix
        elif choix == "3":
            try:
                id_produit = int(input("ID du produit : "))
                nouveau_prix = float(input("Nouveau prix : "))

                dao.modifier_prix_produit(
                    id_produit,
                    nouveau_prix
                )

            except ValueError:
                print("Erreur : veuillez saisir des nombres valides.")

        # Ajouter client
        elif choix == "4":
            nom = input("Nom du client : ")
            email = input("Email du client : ")

            client = Client(None, nom, email)
            dao.ajouter_client(client)

        # Lister clients
        elif choix == "5":
            clients = dao.lister_clients()

            if not clients:
                print("Aucun client.")

            else:
                print("\n--- Liste des clients ---")

                for client in clients:
                    print(client)

        # Recherche client
        elif choix == "6":
            email = input("Email à rechercher : ")

            client = dao.rechercher_client_par_email(email)

            if client:
                print("Client trouvé :")
                print(client)

            else:
                print("Aucun client trouvé.")

        # Quitter
        elif choix == "0":
            print("Au revoir !")
            break

        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()