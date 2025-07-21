import pandas as pd
from pymongo import MongoClient
import os  # Ajouté pour la gestion des chemins de fichiers
def get_db():
    try:
        # Correction : Ajout des options de connexion recommandées
        client = MongoClient(
            "mongodb+srv://itrebmalak:azerty1234@chatbotp6projet.9v7hlst.mongodb.net/",
            serverSelectionTimeoutMS=5000  # Timeout de 5 secondes
)
        # Test de la connexion
        client.admin.command('ping')
        db = client.chatbot_db
        print("✅ Connexion à MongoDB établie")
        return db
    except Exception as e:
        print("❌ Erreur de connexion à MongoDB :", e)
        return None
def create_collections():
    db = get_db()
    if db is None:
        return False
    try:
        # Création des collections si elles n'existent pas
        collections_created = False
        if "qa" not in db.list_collection_names():
            db.create_collection("qa")
            print("✅ Collection 'qa' créée.")
            collections_created = True
        if "unanswered" not in db.list_collection_names():
            db.create_collection("unanswered")
            print("✅ Collection 'unanswered' créée.")
            collections_created = True
        return collections_created
    except Exception as e:
        print("❌ Erreur lors de la création des collections :", e)
        return False
def import_csv_to_mongodb(csv_path, collection_name):
    try:
        # Correction du chemin avec raw string ou double backslashes
        df = pd.read_csv(csv_path)
        # Nettoyage des données NaN
        df = df.where(pd.notnull(df), None)
        db = get_db()
        if db is None:
            return False
        collection = db[collection_name]
        # Conversion et insertion par lots de 1000 documents
        data = df.to_dict("records")
        collection.insert_many(data)
        print(f"✅ {len(data)} documents insérés dans la collection '{collection_name}'")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'import du CSV : {e}")
        return False

if __name__ == "__main__":
    # 1. Création des collections
    create_collections()
    # 2. Import des données
    # Correction : Utilisation d'un raw string ou double backslashes
    csv_path = r"D:\Stage 2025 Banque populaire\Logiciels\data.csv"  # À adapter
    if os.path.exists(csv_path):
        import_csv_to_mongodb(csv_path, "qa")
    else:
        print(f"❌ Fichier CSV introuvable : {csv_path}")