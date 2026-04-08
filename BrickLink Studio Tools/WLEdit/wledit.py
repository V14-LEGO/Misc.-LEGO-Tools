version = '260409b'
docstring = '''Rudimentary editor for BrickLink wanted lists.

-a, add        : Add parts from a Wanted List or a specified part
-c, clear      : Clear list
-d, div        : Divide the quantity of specified part
-h, help       : Show help
-kp, keep      : Remove everything else but the specified part
-l, lookup     : Open a BrickLink page of the specified part
-m, mul        : Multiply the quantity of specified part
-neg, negative : Keep only the parts with negative quantity
-o, out        : Save to XML file
-pos, positive : Keep only the parts with positive quantity
-p, print      : Print list
-q, quit       : Quit
-rm, remove    : Remove a specified part
-s, sub        : Subtract parts from a Wanted List or a specified part

Parts are specified as: [ItemID] [ColorID] [Qty]
* can be used as wildcard

Author: V.14
Version: ''' + version

from collections import Counter
from json import load
from math import ceil, floor
from os import system
from sys import argv, exit
from urllib.parse import quote
from webbrowser import open_new_tab
import xml.etree.ElementTree as ET

color = {}
try:
    with open('bricklink.json') as f:
        bricklink = load(f)
        for color_id, color_dict in bricklink['color'].items():
            color[int(color_id)] = color_dict['name']
except FileNotFoundError:
    pass

class WLEdit:
    def __init__(self):
        system('')
        self.counter = Counter()
        if len(argv) > 1:
            input_str = ' '.join(argv[1:]) + ' quit'
        else:
            input_str = ''
            print(f'''WLEdit {version}
Type 'help' or -h for a list of commands''')
        while True:
            if not input_str:
                try:
                    input_str = input('>>> ')
                except:
                    exit()
            while not input_str:
                try:
                    input_str = input('\033[1A\033[4C')
                except:
                    exit()
            args = input_str.lower().split()
            args = [self.aliases[arg] if arg in self.aliases
                    else arg for arg in args]
            if args[0] not in self.functions:
                args = ['clear', 'add', *args]
            commands = []
            self.arglist = []
            for arg in args:
                if arg in self.functions:
                    if self.arglist:
                        commands.append(self.arglist)
                    self.arglist = [arg]
                else:
                    self.arglist.append(arg)
            if self.arglist:
                commands.append(self.arglist)
            if commands[-1][0] != 'print':
                commands.append(['print'])
            for command in commands:
                self.arglist = command
                self.functions[command[0]](self)
                if command[0] in ('help', 'lookup'):
                    break
            input_str = ''

    def add_sub(self):
        mode = self.arglist[0]
        i = 1
        while i < len(self.arglist):
            self.clean()
            self.filename = self.arglist[i]
            items = self.load()
            if items is None:
                i += 3
                if i > len(self.arglist):
                    print('\033[37;41mInvalid syntax\033[0m')
                    return
                item_id = self.arglist[i-3]
                try:
                    qty = int(self.arglist[i-1])
                except ValueError:
                    print('\033[37;41mInvalid quantity\033[0m')
                    continue
                try:
                    item_color = int(self.arglist[i-2])
                except ValueError:
                    if self.arglist[i-2] != '*':
                        print('\033[37;41mInvalid color ID\033[0m')
                        continue
                    if item_id == '*':
                        if mode == 'add':
                            for item in self.counter:
                                self.counter[item] += qty
                            print(f'Added {qty}x of everything')
                        else:
                            for item in self.counter:
                                self.counter[item] -= qty
                            print(f'Subtracted {qty}x of everything')
                    else:
                        for item in self.counter:
                            if item[0] == item_id:
                                if mode == 'add':
                                    self.counter[item] += qty
                                    print(f'Added {qty}x {item_id}, ', end='')
                                else:
                                    self.counter[item] -= qty
                                    print(f'Subtracted {qty}x {item_id}, ',
                                          end='')
                                print(color[item[1]] if color else item[1])
                    continue
                if color and item_color not in color:
                    print('\033[37;41mUndefined color ID\033[0m')
                    continue
                if item_id == '*':
                    for item in self.counter:
                        if item[1] == item_color:
                            if mode == 'add':
                                self.counter[item] += qty
                                print(f'Added {qty}x {item[0]}, ', end='')
                            else:
                                self.counter[item] -= qty
                                print(f'Subtracted {qty}x {item[0]}, ', end='')
                            print(color[item_color] if color else item_color)
                    continue
                item = item_id, item_color
                if mode == 'add':
                    self.counter[item] += qty
                    print(f'Added {qty}x {item_id}, ', end='')
                else:
                    self.counter[item] -= qty
                    print(f'Subtracted {qty}x {item_id}, ', end='')
                print(color[item_color] if color else item_color)
            else:
                i += 1
                if mode == 'add':
                    for item, qty in items:
                        self.counter[item] += qty
                    print(f'Added {self.filename}')
                else:
                    for item, qty in items:
                        self.counter[item] -= qty
                    print(f'Subtracted {self.filename}')
        self.clean()
    
    def clean(self):
        empty_items = tuple(item for item, qty in self.counter.items()
                            if qty == 0)
        for item in empty_items:
            del self.counter[item]

    def clear(self):
        if not self.counter:
            return
        self.counter.clear()
        print('Cleared contents')

    def help(self):
        print(docstring)

    def kp_rm(self):
        mode = self.arglist[0]
        item_set = set()
        i = 1
        while i < len(self.arglist):
            i += 2
            if i > len(self.arglist):
                print('\033[37;41mInvalid syntax\033[0m')
                return
            item_id = self.arglist[i-2]
            try:
                item_color = int(self.arglist[i-1])
            except ValueError:
                if self.arglist[i-1] != '*':
                    print('\033[37;41mInvalid color ID\033[0m')
                    continue
                if item_id == '*':
                    item_set.update(tuple(self.counter))
                    if mode == 'keep':
                        print('Kept everything')
                else:
                    for item in self.counter:
                        if item[0] == item_id:
                            item_set.add(item)
                continue
            if color and item_color not in color:
                print('\033[37;41mUndefined color ID\033[0m')
                continue
            if item_id == '*':
                for item in self.counter:
                    if item[1] == item_color:
                        item_set.add(item)
                continue
            item = item_id, item_color
            item_set.add(item)
        for item in tuple(self.counter):
            if ((mode == 'keep' and item not in item_set) or
                (mode == 'remove' and item in item_set)):
                del self.counter[item]
                print(f'Removed {item[0]},',
                      color[item[1]] if color else item[1])
    
    def lookup(self):
        if len(self.arglist) > 1:
            url = 'https://www.bricklink.com/v2/catalog/catalogitem.page?'
            url += f'P={self.arglist[1]}#T=S&'
            if len(self.arglist) > 2:
                try:
                    color = int(self.arglist[2])
                except ValueError:
                    print('\033[37;41mInvalid color ID\033[0m')
                    return
                url += f'C={color}&O={{"color":{color},'
            else:
                url += 'O={'
            url += '"st":"4","ss":"JP","cond":"N","iconly":0}'
            safeurl = quote(url, safe='#&,/:=?')
            open_new_tab(safeurl)

    def load(self):
        if self.filename == '*':
            return None
        tree = None
        if not self.filename.endswith('.xml'):
            try:
                tree = ET.parse(self.filename)
            except FileNotFoundError:
                self.filename += '.xml'
        if tree is None:
            try:
                tree = ET.parse(self.filename)
            except FileNotFoundError:
                return None
        root = tree.getroot()
        items = []
        for element in root.iter('ITEM'):
            item_id = element.findtext('ITEMID')
            item_color = int(element.findtext('COLOR'))
            qty = (int(element.findtext('MINQTY')) if element.findtext('QTY')
                   is None else int(element.findtext('QTY')))
            items.append(((item_id, item_color), qty))
        return items

    def mul_div(self):
        mode = self.arglist[0]
        if len(self.arglist) == 2:
            try:
                factor = float(self.arglist[1])
            except ValueError:
                print('\033[37;41mInvalid factor\033[0m')
                return
            if mode == 'div' and factor == 0:
                print('\033[37;41mCannot divide by 0\033[0m')
                return
            for item in self.counter:
                if mode == 'mul':
                    self.counter[item] *= factor
                else:
                    self.counter[item] /= factor
                if self.counter[item] > 0:
                    self.counter[item] = ceil(self.counter[item])
                else:
                    self.counter[item] = floor(self.counter[item])
            if mode == 'mul':
                print(f'Multiplied everything by {factor}')
            else:
                print(f'Divided everything by {factor}')
            self.clean()
            return
        i = 1
        while i < len(self.arglist):
            self.clean()
            i += 3
            if i > len(self.arglist):
                print('\033[37;41mInvalid syntax\033[0m')
                return
            item_id = self.arglist[i-3]
            try:
                factor = float(self.arglist[i-1])
            except ValueError:
                print('\033[37;41mInvalid factor\033[0m')
                continue
            if mode == 'div' and factor == 0:
                print('\033[37;41mCannot divide by 0\033[0m')
                continue
            try:
                item_color = int(self.arglist[i-2])
            except ValueError:
                if self.arglist[i-2] != '*':
                    print('\033[37;41mInvalid color ID\033[0m')
                    continue
                if item_id == '*':
                    for item in self.counter:
                        if mode == 'mul':
                            self.counter[item] *= factor
                        else:
                            self.counter[item] /= factor
                        if self.counter[item] > 0:
                            self.counter[item] = ceil(self.counter[item])
                        else:
                            self.counter[item] = floor(self.counter[item])
                    if mode == 'mul':
                        print(f'Multiplied everything by {factor}')
                    else:
                        print(f'Divided everything by {factor}')
                else:
                    for item in self.counter:
                        if item[0] == item_id:
                            if mode == 'mul':
                                self.counter[item] *= factor
                                print(f'Multiplied {item_id}, ', end='')
                            else:
                                self.counter[item] /= factor
                                print(f'Divided {item_id}, ', end='')
                            if self.counter[item] > 0:
                                self.counter[item] = ceil(self.counter[item])
                            else:
                                self.counter[item] = floor(self.counter[item])
                            print(f'{color[item[1]] if color else item[1]} '
                                  f'by {factor}')
                continue
            if color and item_color not in color:
                print('\033[37;41mUndefined color ID\033[0m')
                continue
            if item_id == '*':
                for item in self.counter:
                    if item[1] == item_color:
                        if mode == 'mul':
                            self.counter[item] *= factor
                            print(f'Mutiplied {item[0]}, ', end='')
                        else:
                            self.counter[item] /= factor
                            print(f'Divided {item[0]}, ', end='')
                        if self.counter[item] > 0:
                            self.counter[item] = ceil(self.counter[item])
                        else:
                            self.counter[item] = floor(self.counter[item])
                        print(f'{color[item_color] if color else item_color} '
                              f'by {factor}')
                continue
            item = item_id, item_color
            if mode == 'mul':
                self.counter[item] *= factor
                print(f'Multiplied {item_id}, ', end='')
            else:
                self.counter[item] /= factor
                print(f'Divided {item_id}, ', end='')
            if self.counter[item] > 0:
                self.counter[item] = ceil(self.counter[item])
            else:
                self.counter[item] = floor(self.counter[item])
            print(f'{color[item_color] if color else item_color} by {factor}')     
        self.clean()

    def out(self):
        if not self.counter:
            print('\033[37;41mList is empty\033[0m')
            return
        self.filename = self.arglist[1] if len(self.arglist) > 1 else 'out.xml'
        if not self.filename.endswith('.xml'):
            self.filename += '.xml'
        root = ET.Element('INVENTORY')
        for item, qty in self.counter.items():
            element = ET.SubElement(root, 'ITEM')
            ET.SubElement(element, 'ITEMTYPE').text = 'P'
            ET.SubElement(element, 'ITEMID').text = item[0]
            ET.SubElement(element, 'COLOR').text = str(item[1])
            ET.SubElement(element, 'MINQTY').text = str(qty)
            ET.SubElement(element, 'CONDITION').text = 'N'
        ET.indent(root, '\t')
        tree = ET.ElementTree(root)
        tree.write(self.filename, encoding='UTF-8')
        print(f'Saved as {self.filename}')

    def pos_neg(self):
        mode = self.arglist[0]
        remove_list = []
        for item, qty in self.counter.items():
            if mode == 'positive':
                if qty < 0:
                    remove_list.append(item)
                    print(f'Removed {item[0]},',
                          color[item[1]] if color else item[1])
            elif qty > 0:
                remove_list.append(item)
                print(f'Removed {item[0]},',
                      color[item[1]] if color else item[1])
        for item in remove_list:
            del self.counter[item]
    
    def print(self):
        if not self.counter:
            print('0 Lots | 0 Items')
            return
        item_list = [(*item, qty) for item, qty in self.counter.items()]
        item_list.sort()
        a = max([len(item[0])        for item in item_list])
        b = max([len(str(item[1]))   for item in item_list])
        c = max([len(color[item[1]]) for item in item_list]) if color else -1
        d = max([len(str(item[2]))   for item in item_list])
        total_qty = 0
        for i, (item_id, item_color, qty) in enumerate(item_list):
            if i == 0 or item_id != item_list[i-1][0]:
                print(f'{item_id+" ":─<{a+1}}', end='')
                if i == len(item_list) - 1 or item_id != item_list[i+1][0]:
                    print('─', end='')
                else:
                    print('┬', end='')
            else:
                print(' '*(a+1), end='')
                if i == len(item_list) - 1 or item_id != item_list[i+1][0]:
                    print('└', end='')
                else:
                    print('├', end='')
            print(f'{"  "+str(item_color):─>{b+2}}',
                  f'{color[item_color]+" ":─<{c+2}}' if color else '─', end='')
            if qty > 0:
                print(f'  [ {qty:{d}} ]')
            else:
                print(f'  [ \033[37;41m{qty:{d}}\033[0m ]')
            total_qty += qty
        summary = f'  {len(item_list)} Lots | '
        if total_qty >= 0:
            summary += f'{total_qty} Items'
            print(f'{summary:─>{a+b+c+d+13}}')
        else:
            summary += f'\033[37;41m{total_qty}\033[0m Items'
            print(f'{summary:─>{a+b+c+d+25}}')

    def quit(self):
        exit()
    
    functions = {
        'add'     : add_sub,
        'clear'   : clear,
        'div'     : mul_div,
        'help'    : help,
        'keep'    : kp_rm,
        'lookup'  : lookup,
        'mul'     : mul_div,
        'negative': pos_neg,
        'out'     : out,
        'positive': pos_neg,
        'print'   : print,
        'quit'    : quit,
        'remove'  : kp_rm,
        'sub'     : add_sub
        }
    aliases = {
        '-a'  : 'add',
        '-c'  : 'clear',
        '-d'  : 'div',
        '-h'  : 'help',
        '-k'  : 'keep',
        '-kp' : 'keep',
        '-l'  : 'lookup',
        '-m'  : 'mul',
        '-n'  : 'negative',
        '-neg': 'negative',
        '-o'  : 'out',
        '-p'  : 'print',
        '-pos': 'positive',
        '-q'  : 'quit',
        '-r'  : 'remove',
        '-rm' : 'remove',
        '-s'  : 'sub'
        }

if __name__ == '__main__':
    WLEdit()
