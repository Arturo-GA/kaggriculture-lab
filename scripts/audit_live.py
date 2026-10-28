"""Download the user's public match records; keep replay data outside Git."""
import json
from datetime import datetime, timezone
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi


def main():
    api = KaggleApi()
    api.authenticate()
    folder = Path('vendor/live')
    folder.mkdir(parents=True, exist_ok=True)
    episodes = api.competition_list_episodes(56190498)
    for ep in episodes:
        episode_id = ep.id
        target = folder/f'episode-{episode_id}-replay.json'
        if not target.exists():
            api.competition_episode_replay(episode_id,path=str(folder))
        print('DOWNLOADED', episode_id, target.stat().st_size, flush=True)
    print('Episodes:',len(episodes))


if __name__ == '__main__':
    main()
