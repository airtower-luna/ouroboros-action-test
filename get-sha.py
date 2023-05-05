import os
import requests
import sys

action_repo = sys.argv[1]
action_ref = sys.argv[2]

try:
    b = bytes.fromhex(action_ref)
    if len(b) == 20:
        print(f'Looks like a commit hash already!', file=sys.stderr)
        print(f'{action_ref}')
        sys.exit(0)
except ValueError:
    pass

print(f'Looking up ref: {action_ref}', file=sys.stderr)

session = requests.Session()
session.headers.update({
    'X-GitHub-Api-Version': '2022-11-28',
    'Accept': 'application/vnd.github+json'
})
if (token := os.environ.get('GITHUB_TOKEN')) is not None:
    session.headers.update({'Authorization': f'Bearer {token}'})

r = session.get(f'https://api.github.com/repos/{action_repo}')
print(r.headers, file=sys.stderr)
try:
    refs_url = r.json()['git_refs_url'].removesuffix('{/sha}')
finally:
    print(r.text, file=sys.stderr)

print(f'retrieving refs from {refs_url}', file=sys.stderr)
r = session.get(refs_url)
print(r.headers, file=sys.stderr)
for ref in r.json():
    print(ref, file=sys.stderr)
    ref_str = ref['ref'].removeprefix('refs/heads/').removeprefix('refs/tags/')
    if ref_str == action_ref:
        print(f'{ref["object"]["sha"]}')
