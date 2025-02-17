import os
import json

import requests as re

from logger import logger

def download_epdb(base_path: os.PathLike):
    url = "https://raw.githubusercontent.com/vanishedbydefa/WBCH-decider/refs/heads/main/epdb_new.json"
    resp = re.get(url, timeout=10)
    if resp.status_code == 200:
        filename = os.path.join(base_path, os.path.basename(url))
        with open(filename, "wb") as f:
            f.write(resp.content)
        logger.info(f"epdb downloaded and saved to: {filename}")
        return os.path.join(base_path, filename)
    else:
        logger.error(f"Failed to download epdb. Status code: {resp.status_code}")
        return None

def load_db(file_path: str):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        logger.error(f"Error while decoding json db: {file_path}")
        return None

def find_episode_by_hash(db, hash_value: str):
    for season, season_data in db.items():
        for episode in season_data.get("episodes"):
            if episode.get("hash") == hash_value:
                return episode
    return None 


def report(db, wbch_files: list):
    # Create a dictionary for quick lookup of available files (hash → file path)
    system_files = {file_hash: file_path for file_path, file_hash in wbch_files}

    total_episodes = 0
    found_episodes = 0

    print("\n📢  WBCH Collection Report  📢\n")

    for season, season_data in sorted(db.items()):
        season_total = len(season_data.get("episodes", []))
        season_found = 0

        print(f"🎬 Season {season}\n" + "-" * 40)

        for episode in season_data.get("episodes", []):
            episode_name = episode.get("name", "Unknown Episode")
            episode_hash = episode.get("hash")

            total_episodes += 1

            if not episode_hash:
                print(f"  ⚠️  '{episode_name}' - No hash available")
                continue

            if episode_hash in system_files:
                found_episodes += 1
                season_found += 1
                print(f"  ✅ '{episode_name}' - Found at '{system_files[episode_hash]}'")
            else:
                print(f"  ❌ '{episode_name}' - Missing")

        print(f"\n📊 Season {season}: Found {season_found}/{season_total} episodes\n")

    print("📋 Final Report")
    print(f"📀 Total Episodes Found: {found_episodes}/{total_episodes}")
    print(f"✅ Completion: {found_episodes / total_episodes:.2%}\n" if total_episodes > 0 else "⚠️ No episodes in database.")
