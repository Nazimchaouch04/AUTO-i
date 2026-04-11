import sqlite3
import os

# Connexion à la base de données
db_path = 'db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Lister toutes les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables dans la base de données:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Compter les enregistrements dans quelques tables importantes
    important_tables = ['annonces_annonce', 'auth_user', 'annonces_vehicule']
    print("\nNombre d'enregistrements:")
    for table_name in important_tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  {table_name}: {count} enregistrements")
        except sqlite3.OperationalError:
            print(f"  {table_name}: Table non trouvée")
    
    conn.close()
else:
    print("Base de données non trouvée")
