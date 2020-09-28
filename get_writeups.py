import json
import os
from pathlib import Path
import shutil

with open('./writeups.json', 'r') as f:
    writeups = json.loads(f.read())

root = '../ctf_solutions/'
Path('downloads').mkdir(parents=True, exist_ok=True)
Path('assets').mkdir(parents=True, exist_ok=True)

for writeup in writeups:
    directory = writeup["directory"]
    directory_name = directory.split('/')[-1]
    posts_dir = f'_posts/{directory_name}'

    Path(posts_dir).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(f'{root}/{directory}/README.md', f'{posts_dir}/README.md')

    # dealing with assets
    if Path.is_dir(Path(f'{root}/{directory}/assets')):
        assets_dir = f'assets/{directory_name}'
        if os.path.exists(assets_dir):
            shutil.rmtree(assets_dir)
        shutil.copytree(f'{root}/{directory}/assets', assets_dir)

        with open(f'{posts_dir}/README.md', 'r') as f:
            text = f.read()
            text = text.replace('(./assets', f'(/{assets_dir}')
            text = text.replace('(assets', f'(/{assets_dir}')
            text = text.replace('"assets', f'"/{assets_dir}')
            text = text.replace('"./assets', f'"/{assets_dir}')

        with open(f'{posts_dir}/README.md', 'w') as f:
            f.write(text)

    # dealing with file attachments
    if 'files' in writeup and writeup['files']:
        downloads_dir = f'downloads/{directory_name}'
        if os.path.exists(downloads_dir):
            shutil.rmtree(downloads_dir)
        Path(downloads_dir).mkdir(parents=True, exist_ok=True)

        for f in writeup['files']:
            print(f'{root}/{directory}/{f}', f'{downloads_dir}/{f}')
            shutil.copyfile(f'{root}/{directory}/{f}', f'{downloads_dir}/{f}')



    # writing the main article file
    date = writeup['date']
    title = writeup['title']
    excerpt = writeup['excerpt']
    tags = writeup['tags']
    categories = writeup['categories']
    article_file = f'{posts_dir}/{date}-{directory_name}.md'
    text = '---\n' \
           f'title: {title}\n' \
           f'excerpt: {excerpt}\n'  \
           f'tags: {tags}\n'  \
           f'categories: {categories}\n'  \
           f'---\n'  \
           '{% include_relative README.md %}\n' 

    if 'files' in writeup and writeup['files']:
        text += f'#### Files\n\n'
        for f in writeup['files']:
            text += f'[{f}](/{downloads_dir}/{f})\n\n'

    with open(article_file, 'w') as f:
        f.write(text)

