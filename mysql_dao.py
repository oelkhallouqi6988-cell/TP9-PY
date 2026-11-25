import mysql.connector
from mysql.connector import Error

from models import Produit, Client


class MySQLDAO:

    def __init__(
        self,
        host="localhost",
        user="root",
        password="G131006988",
        database="boutique"
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.creer_base()
        self.creer_tables()

    def connexion(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def creer_base(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )

            cursor = conn.cursor()

            cursor.execute("""
                CREATE DATABASE IF NOT EXISTS boutique
            """)

            conn.commit()
            cursor.close()
            conn.close()

        except Error as e:
            print("Erreur de connexion MySQL :", e)

    def creer_tables(self):
        try:
            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produits (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nom VARCHAR(100) NOT NULL,
                    prix DECIMAL(10,2) NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nom VARCHAR(100) NOT NULL,
                    email VARCHAR(150) NOT NULL UNIQUE
                )
            """)

            conn.commit()

            cursor.close()
            conn.close()

        except Error as e:
            print("Erreur lors de la création des tables :", e)

    # ---------------- PRODUITS ----------------

    def ajouter_produit(self, produit):
        try:
            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO produits (nom, prix)
                VALUES (%s, %s)
            """, (produit.nom, produit.prix))

            conn.commit()

            cursor.close()
            conn.close()

            print("Produit ajouté avec succès.")

        except Error as e:
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
                produits.append(
                    Produit(ligne[0], ligne[1], float(ligne[2]))
                )

            cursor.close()
            conn.close()

        except Error as e:
            print("Erreur :", e)

        return produits

    def modifier_prix_produit(self, id_produit, nouveau_prix):
        try:
            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE produits
                SET prix = %s
                WHERE id = %s
            """, (nouveau_prix, id_produit))

            conn.commit()

            if cursor.rowcount > 0:
                print("Prix modifié avec succès.")
            else:
                print("Produit introuvable.")

            cursor.close()
            conn.close()

        except Error as e:
            print("Erreur lors de la modification :", e)

    # ---------------- CLIENTS ----------------

    def ajouter_client(self, client):
        try:
            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO clients (nom, email)
                VALUES (%s, %s)
            """, (client.nom, client.email))

            conn.commit()

            cursor.close()
            conn.close()

            print("Client ajouté avec succès.")

        except Error as e:
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
                clients.append(
                    Client(ligne[0], ligne[1], ligne[2])
                )

            cursor.close()
            conn.close()

        except Error as e:
            print("Erreur :", e)

        return clients

    def rechercher_client_par_email(self, email):
        try:
            conn = self.connexion()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nom, email
                FROM clients
                WHERE email = %s
            """, (email,))

            ligne = cursor.fetchone()

            cursor.close()
            conn.close()

            if ligne:
                return Client(ligne[0], ligne[1], ligne[2])

            return None

        except Error as e:
            print("Erreur lors de la recherche :", e)
            return None