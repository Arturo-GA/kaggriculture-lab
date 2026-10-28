"""Create the user-authorized private repository, using credentials only in memory."""
import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path


def main():
    result = subprocess.run(['git', 'credential', 'fill'],
                            input='protocol=https\nhost=github.com\n\n',
                            capture_output=True, text=True, check=True)
    fields = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    token = fields.get('password')
    if not token:
        raise SystemExit('No existing GitHub credential')

    def api(path, payload=None):
        req = urllib.request.Request('https://api.github.com' + path,
            data=None if payload is None else json.dumps(payload).encode(),
            headers={'Authorization': 'Bearer ' + token,
                     'Accept': 'application/vnd.github+json',
                     'Content-Type': 'application/json', 'User-Agent': 'kaggriculture-lab'})
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)

    user = api('/user')['login']
    name = 'kaggriculture-lab'
    try:
        repo = api('/repos/' + user + '/' + name)
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise
        repo = api('/user/repos', {'name': name, 'private': True, 'auto_init': False,
                   'description': 'Kaggriculture research, reproducible evaluation and experimental agents'})
    receipt = {k: repo[k] for k in ('full_name', 'html_url', 'clone_url', 'private')}
    Path('results').mkdir(exist_ok=True)
    Path('results/github.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    try:
        main()
    except urllib.error.HTTPError as error:
        raise SystemExit('GitHub HTTP status: ' + str(error.code)) from None
