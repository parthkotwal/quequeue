import os
import requests
import psycopg2
from psycopg2.extras import DictCursor
from PIL import Image
from io import BytesIO

# ==== CONFIGURATION ====
DB_CONFIG = {
    "dbname": "quequeue_db",
    "user": "quequeue_user",
    "password": "quequeue_pass",
    "host": "localhost",
    "port": 5432,
}

OUTPUT_DIR = "/Users/parthkotwal/Projects/quequeue/quequeue-frontend/src/assets/album_covers"  # directory to store images
TABLE_NAME = "queues_track"
IMAGE_COLUMN = "album_image_url"
ID_COLUMN = "id"  # unique identifier column (assumed)
# =======================


def get_unique_filename(base_path):
    """Return a unique filename by appending (1), (2), ... if file exists."""
    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    counter = 1
    new_path = f"{base} ({counter}){ext}"
    while os.path.exists(new_path):
        counter += 1
        new_path = f"{base} ({counter}){ext}"
    return new_path


def download_and_save_image(url, filename):
    """Download image from URL and save as .webp"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Open image in memory
        img = Image.open(BytesIO(response.content)).convert("RGB")

        # Ensure unique filename
        filename = get_unique_filename(filename)

        # Save as .webp
        img.save(filename, "webp")
        print(f"✅ Saved: {filename}")
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")


def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Connect to PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=DictCursor)

    # Fetch all rows
    cursor.execute(f"SELECT {ID_COLUMN}, {IMAGE_COLUMN} FROM {TABLE_NAME}")
    rows = cursor.fetchall()

    print(f"Found {len(rows)} rows to process...")

    for row in rows:
        track_id = row[ID_COLUMN]
        url = row[IMAGE_COLUMN]

        if not url:
            print(f"⚠️ Skipping track {track_id}: no URL")
            continue

        filename = os.path.join(OUTPUT_DIR, f"{track_id}_2.webp")
        download_and_save_image(url, filename)

    cursor.close()
    conn.close()
    print("🎉 Done!")


if __name__ == "__main__":
    main()