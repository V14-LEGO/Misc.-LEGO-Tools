"""Get color names and IDs from BrickLink.
Author: V.14
Version: 260409a"""

from json import dump, load
from urllib.request import Request, urlopen

try:
    with open('bricklink.json') as f:
        bricklink = load(f)
        color = bricklink['color']
        for color_id in tuple(color):
            color[int(color_id)] = color[color_id]
            del color[color_id]
except FileNotFoundError:
    color = {}
    bricklink = {'color': color}
url = 'https://v2.bricklink.com/en-us/catalog/color-guide'
header = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/143.0.0.0 '
                        'Safari/537.36'}
req = Request(url, headers=header)
data = urlopen(req).read().decode()
start = 0
while True:
    index = data.find(r'\"colorList\":[', start)
    if index == -1:
        break
    start = index + 15
    while True:
        index = data.find(r'\"id\":', start)
        if index == -1 or data.find(']', start, index) > 0:
            break
        start = index + 7
        end = data.find(',', start)
        color_id = int(data[start:end])
        start = data.find(r'\"name\":\"', end+1) + 11
        end = data.find(r'\",', start)
        color_name = data[start:end]
        color[color_id] = {'name': color_name}
        start = end + 3
if color:
    with open('bricklink.json', 'w') as f:
        dump(bricklink, f, indent=4, sort_keys=True)
