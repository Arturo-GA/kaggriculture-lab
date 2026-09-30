"""Read-only reconciliation of the two existing submission IDs; never uploads."""
from datetime import datetime, timezone

from release_f19 import ROOT, read, write
from research_f16 import plain
from research_top100 import api, limited


def main():
    client = api()
    submissions = limited(client.competition_submissions, 'kaggriculture') or []
    by_id = {s.ref: s for s in submissions if s is not None}
    names = read(ROOT / 'release.json')['candidates']
    assert len(names) == 2
    for name in names:
        path = ROOT / (name + '_submission_receipt.json')
        receipt = read(path)
        s = by_id[receipt['id']]
        assert s.description == receipt['description']
        receipt.update(status=str(s.status), public_score=s.public_score,
                       error=s.error_description, date=str(s.date),
                       checked_utc=datetime.now(timezone.utc).isoformat())
        write(path, receipt)
        print(name, receipt['id'], receipt['status'], 'score', receipt['public_score'],
              'error', receipt['error'])
    active = plain(limited(client.competition_team_submissions, 16639155))
    limits = plain(limited(client.competition_get_submission_limits, 'kaggriculture'))
    write(ROOT / 'active_after_submission.json', dict(checked_utc=datetime.now(timezone.utc).isoformat(), active=active, limits=limits))
    print('Daily submissions used:', limits['num_today'])


if __name__ == '__main__':
    main()
