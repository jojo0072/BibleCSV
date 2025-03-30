import requests
import csv
import time

# Konfigurationsvariablen
API_KEY = "bc5834903ffe33ae480eff20f733ea8b"  # Deinen API-Key hier einfügen
BASE_URL = "https://api.scripture.api.bible/v1/bibles/f492a38d0e52db0f-01"  # URL mit Bibel-ID

# Headers für API-Anfragen
headers = {"api-key": API_KEY}

# Funktion, um Bücher der Bibel abzurufen
def fetch_books():
    url = f"{BASE_URL}/books"  # Direkte URL zu Büchern
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

# Funktion, um Kapitel eines Buches abzurufen
def fetch_chapters(book_id):
    url = f"{BASE_URL}/books/{book_id}/chapters"  # Direkte URL zu Kapiteln
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

# Funktion, um Verse eines Kapitels abzurufen
def fetch_verses(chapter_id):
    url = f"{BASE_URL}/chapters/{chapter_id}/verses"  # Direkte URL zu Versen
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    time.sleep(1)
    data = response.json()["data"]
    # Debugging: Ausgabe der API-Datenstruktur
    print(f"Verse-Daten: {data}")
    return data


import time

def fetch_verses(chapter_id):
    url = f"{BASE_URL}/chapters/{chapter_id}/verses"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    time.sleep(1)  # 1 Sekunde Pause zwischen Anfragen
    return response.json()["data"]



# Daten sammeln und in CSV exportieren
def export_bible_to_csv():
    with open("bible.csv", mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Referenz", "Text"])

        # Bücher der Bibel abrufen
        books = fetch_books()
        for book in books:
            print(f"Verarbeite Buch: {book['name']}")
            chapters = fetch_chapters(book["id"])
            
            for chapter in chapters:
                print(f"  Kapitel: {chapter['reference']}")
                verses = fetch_verses(chapter["id"])
                
                for verse in verses:
                    reference = verse["reference"]
                    # Überprüfen, ob 'content' oder ein alternatives Feld existiert
                    text = verse.get("content") or verse.get("text") or "Kein Text verfügbar"
                    writer.writerow([reference, text])

# Ausführen
export_bible_to_csv()
print("Bibel erfolgreich exportiert: bible.csv")
