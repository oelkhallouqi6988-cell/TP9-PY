import sqlite3

from models import Produit, Client


class SQLiteDAO:

    def __init__(self, db_name="boutique.db"):
        self.db_name = db_name
        self.creer_tables()

    def connexion(self):
        return sqlite3.connect(self.db_name)

    def creer_tables(self):
        try:
            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prix REAL NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            """)

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print("Erreur SQLite :", e)

    # ---------------- PRODUITS ----------------

    def ajouter_produit(self, produit):
        try:
            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO produits (nom, prix)
                VALUES (?, ?)
            """, (produit.nom, produit.prix))

            conn.commit()
            conn.close()

            print("Produit ajouté avec succès.")

        except sqlite3.Error as e:
            print("Erreur lors de l'ajout du produit :", e)

    def lister_produits(self):
        produits = []

        try:
            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nom, prix
                FROM produits
            """)

            lignes = cursor.fetchall()

            for ligne in lignes:
                produit = Produit(ligne[0], ligne[1], ligne[2])
                produits.append(produit)

            conn.close()

        except sqlite3.Error as e:
            print("Erreur :", e)

        return produits

    def modifier_prix_produit(self, id_produit, nouveau_prix):
        try:
            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE produits
                SET prix = ?
                WHERE id = ?
            """, (nouveau_prix, id_produit))

            conn.commit()

            if cursor.rowcount > 0:
                print("Prix modifié avec succès.")
            else:
                print("Produit introuvable.")

            conn.close()

        except sqlite3.Error as e:
            print("Erreur lors de la modification :", e)

    # ---------------- CLIENTS ----------------

    def ajouter_client(self, client):
        try:
            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO clients (nom, email)
                VALUES (?, ?)
            """, (client.nom, client.email))

            conn.commit()
            conn.close()

            print("Client ajouté avec succès.")

        except sqlite3.IntegrityError:
            print("Erreur : cet email existe déjà.")

        except sqlite3.Error as e:
            print("Erreur lors de l'ajout du client :", e)

    def lister_clients(self):
        clients = []

        try:
            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nom, email
                FROM clients
            """)

            lignes = cursor.fetchall()

            for ligne in lignes:
                client = Client(ligne[0], ligne[1], ligne[2])
                clients.append(client)

            conn.close()

        except sqlite3.Error as e:
            print("Erreur :", e)

        return clients

    def rechercher_client_par_email(self, email):
        try:
            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nom, email
                FROM clients
                WHERE email = ?
            """, (email,))

            ligne = cursor.fetchone()
            conn.close()

            if ligne:
                return Client(ligne[0], ligne[1], ligne[2])

            return None

        except sqlite3.Error as e:
            print("Erreur lors de la recherche :", e)
            return None