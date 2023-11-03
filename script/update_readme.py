import base64
import os
from datetime import datetime, timedelta

import requests

REPOSITORY = os.environ.get('GITHUB_REPOSITORY')
GH_TOKEN = os.environ.get('GH_TOKEN')

GIT_URL = f"https://github.com/{REPOSITORY}/blob/main"
ROOT = "./"
readme = "# TIL\n \n"


def get_update_time_ktc(target_dir):
    # 경로에 해당하는 파일의 KTC 시간을 반환한다.
    utc = datetime.utcfromtimestamp(os.stat(target_dir).st_mtime)
    return str(timedelta(hours=9) + utc).split()[0]  # 한국 시간으로 변경하기 위한 + 09:00


def get_title_md(target_title, target_count):
    return f"### {target_title} [{target_count}]\n"


def get_file_md(target_dir, target_file, ktc):
    target_file_url = f"{GIT_URL}/{target_dir}/{target_file}"
    return f"- [**[{ktc}]**  {split_extension(file)}]({target_file_url})\n"


def write_file(target, add):
    return target + add


def split_extension(file_name):
    # 언더바 -> 공백 변환
    file_name = file_name.replace("_", " ")
    if "." in file_name:
        return file_name.rsplit('.', 1)[0]
    return file_name


dirs = []
# find directory
for data in os.listdir(ROOT):
    # 폴더이고, 숨김 폴더와 script 폴더는 제외한다.
    if os.path.isdir(data) and data[0] != '.' and data != "script":
        dirs.append(data)

for dir in dirs:
    path = ROOT + dir
    files = os.listdir(path)
    total_files = 0

    # file의 개수 구하기
    for file in files:
        if os.path.isfile(path + "/" + file):
            total_files += 1

    readme = write_file(readme, get_title_md(dir, total_files))

    for file in files:
        ktc = get_update_time_ktc(path)
        readme = write_file(readme, get_file_md(dir, file, ktc))

print(f"Create README\n{readme}")

update_url = f"https://api.github.com/repos/{REPOSITORY}/contents/README.md"
headers = {
    "Authorization": f"token {GH_TOKEN}"
}

response = requests.get(update_url, headers=headers)

if response.status_code == 200:
    # Update the content
    data = {
        "message": "[Bot] Add Today I Learned",
        # 생성된 파일 내용을 base64로 인코딩
        "content": base64.b64encode(readme.encode('UTF-8')).decode('ascii'),
        "sha": response.json()["sha"],
    }

    response = requests.put(update_url, json=data, headers=headers)

    if response.status_code == 200:
        print("README updated successfully.")
    else:
        print(f"Failed to update README. Status code: {response.status_code}")
        print(f"Response Content: {response.content}")
else:
    print(f"Failed to fetch README content. Status code: {response.status_code}")
    print(f"Response Content: {response.content}")
