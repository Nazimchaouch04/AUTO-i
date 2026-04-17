#!/usr/bin/env python
"""
Fix date_collecte NOT NULL constraint by adding default values
"""
import sqlite3
from pathlib import Path

# Chemin vers la base de données SQLite
db_path = Path(__file__).parent / 'db.sqlite3'

def fix_date_collecte():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier si la colonne date_collecte existe
        cursor.execute("PRAGMA table_info(annonces_annonce)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'date_collecte' in columns:
            print("Mise à jour des enregistrements sans date_collecte...")
            # Mettre à jour les enregistrements NULL avec date_publication
            cursor.execute("""
                UPDATE annonces_annonce 
                SET date_collecte = date_publication 
                WHERE date_collecte IS NULL
            """)
            
            # Si date_publication est aussi NULL, utiliser la date actuelle
            cursor.execute("""
                UPDATE annonces_annonce 
                SET date_collecte = datetime('now'), date_publication = datetime('now')
                WHERE date_collecte IS NULL
            """)
            
            conn.commit()
            print(f"  {cursor.rowcount} enregistrements mis à jour")
        else:
            print("La colonne date_collecte n'existe pas dans la table annonces_annonce")
            
    except Exception as e:
        print(f"Erreur: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    fix_date_collecte()
    print("Fix terminé")
