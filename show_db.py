import sqlite3

def show_db_summary():
    try:
        conn = sqlite3.connect('backend/db.sqlite3')
        cursor = conn.cursor()
        
        # 1. List Tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        
        print("--- TABLES DANS LA BASE DE DONNEES ---")
        for t in tables:
            try:
                count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                print(f"| {t:35} | {count:5} lignes |")
            except Exception:
                pass
        
        # 2. Sample Data (Annonces)
        print("\n--- APERCU DES ANNONCES (Top 5) ---")
        try:
            cursor.execute("SELECT id, prix, annee, carburant FROM annonces_annonce LIMIT 5")
            rows = cursor.fetchall()
            print(f"{'ID':<5} | {'Prix':<10} | {'Annee':<6} | {'Carburant':<10}")
            print("-" * 40)
            for r in rows:
                print(f"{r[0]:<5} | {r[1]:<10} | {r[2]:<6} | {r[3]:<10}")
        except Exception as e:
            print(f"Erreur apercu : {e}")
            
        conn.close()
    except Exception as e:
        print(f"Erreur connection : {e}")

if __name__ == "__main__":
    show_db_summary()
