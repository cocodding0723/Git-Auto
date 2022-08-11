from os.path import exists
from git import Repo
import pathlib


path = str(pathlib.Path().resolve())
title_path = path + '/title.txt'
update_path = path + '/update_path.txt'

if exists(update_path):
    with open(update_path, 'r') as f:
        path = f.read()
else:
    print('update path is not exist!')
    exit(0)

repo = Repo(path)

status = repo.head.commit.diff(None)

if len(status) == 0:
    print('clean')
    exit(0)

commit_items = {}
commit_msg = ''

if exists(title_path):
    with open(title_path, 'r') as f:
        commit_msg += f.read().format(len(status)) + '\n\n'

# Find Changed Item
for x in status:
    comment = ''
    if x.change_type == 'A':
        comment = 'Add'
    elif x.change_type == 'D':
        comment = 'Delete'
    elif x.change_type == 'R':
        comment = 'Rename'
    elif x.change_type == 'M':
        comment = 'Modify'
    elif x.change_type == 'T':
        comment = 'Modify'
    else:
        comment = 'Modify'

    commit_items[x.a_path] = comment

# Sort Stage Items
sort_dic = sorted(commit_items.items(), key=lambda item: item[1])
for x in sort_dic:
    commit_msg += f'{x[1]} {x[0]}\n'

# Add Items
print('add items')
print("\n".join(commit_items))
repo.git.add(all=True)

# Commit Items
print('commit items')
print(commit_msg)
repo.index.commit(commit_msg)

print(repo.remotes.origin.url)
origin = repo.remotes.origin

origin.fetch()
origin.pull()
origin.push()

print('finish')