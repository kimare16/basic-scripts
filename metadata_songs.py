import os
import re
import time
import eyed3
import requests

music_dir = r"C:\Users\Froze\Desktop\90's"

def sanitize(text):
    return re.sub(r"[^\w\s]", "", text)

def get_cover(artist, title):
    clean_artist = sanitize(artist)
    clean_title = sanitize(title)
    search = f"{clean_artist} {clean_title}".replace(" ", "+")
    url = f"https://itunes.apple.com/search?term={search}&entity=song&limit=1"

    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"   ⚠️ iTunes não respondeu bem: {resp.status_code}")
            return None

        data = resp.json()
        results = data.get("results")
        if results:
            artwork_url = results[0].get("artworkUrl100", "").replace("100x100", "600x600")
            image_resp = requests.get(artwork_url)
            return image_resp.content
    except Exception as e:
        print(f"Erro ao obter capa para {artist} - {title}: {e}")
    return None

for filename in os.listdir(music_dir):
    if filename.lower().endswith(".mp3") and " - " in filename:
        path = os.path.join(music_dir, filename)
        base = os.path.splitext(filename)[0]
        artist, title = base.split(" - ", 1)
        print(f"🎵 Processando: {artist} - {title}")

        audio = eyed3.load(path)
        if not audio:
            print("   ⚠️ Não foi possível ler o ficheiro.")
            continue

        audio.tag = audio.tag or eyed3.id3.Tag()
        audio.tag.artist = artist.strip()
        audio.tag.title = title.strip()

        if audio.tag.images:
            print("   ⏭️ Já tem capa — a saltar.")
        else:
            time.sleep(0.75)  # Espera 750ms entre chamadas para evitar bloqueio
            cover = get_cover(artist.strip(), title.strip())
            if cover:
                audio.tag.images.set(3, cover, "image/jpeg")
                print("   ✅ Capa aplicada.")
            else:
                print("   ⚠️ Capa não encontrada.")

        audio.tag.save()
