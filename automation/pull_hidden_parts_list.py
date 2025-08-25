from sys import platform
from urllib.request import urlopen
import os

try:
    username = os.getlogin() # get local username
except Exception as e:
    print('Undefined Error in getting username:')
    print(e)

print(f'Logging in as {username}...')

if platform == 'darwin':
    path = f'/Users/{username}/.local/share/Stud.io/Buckets/Hidden Parts'
elif platform == 'win32':
    path = f'C:/Users/{username}/AppData/Local/Stud.io/Buckets/Hidden Parts'
else:
    print('Undefined platform:')
    print(platform)

url = 'https://drive.google.com/uc?id=1o5eNq-wsMopBCDx4LXp74d1N5xQJ39Vk'

with open(path, 'wb') as file:
    try:
        data = urlopen(url).read()
        file.write(data)
    except Exception as e:
        print(f'Undefined Error in opening {url} or editing {path}:')
        print(e)

