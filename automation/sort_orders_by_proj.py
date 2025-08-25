import xml.etree.ElementTree as ET

# order_file: 注文した全体のorderをxmlでダウンロードしたもの
# proj_files: プロジェクトごとに必要なパーツリストをxmlでダウンロードしたもの
# TODO: order_fileのpathを手動で追加するor空の場合に追記を促す指示を出力して以上終了する処理を書く
# TODO: proj_filesのpathについてもorder_fileと同様な処理を加える

order_file = 'hoge.xml'
proj_files = [
    'fuga.xml',
    'piyo.xml',
]

colorlist = (
        '(Not Applicable)',         'White',
        'Tan',                      'Yellow',
        'Orange',                   'Red',
        'Green',                    'Blue',
        'Brown',                    'Light Gray',
        'Dark Gray',                'Black',
        'Trans-Clear',              'Trans-Brown (Old Trans-Black)',
        'Trans-Dark Blue',          'Trans-Light Blue',
        'Trans-Neon Green',         'Trans-Red',
        'Trans-Neon Orange',        'Trans-Yellow',
        'Trans-Green',              'Chrome Gold',
        'Chrome Silver',            'Pink',
        'Purple',                   '',
        '',                         'Rust',
        'Nougat',                   'Earth Orange',
        '',                         'Medium Orange',
        'Light Orange',             'Light Yellow',
        'Lime',                     'Light Lime',
        'Bright Green',             'Medium Green',
        'Light Green',              'Dark Turquoise',
        'Light Turquoise',          'Aqua',
        'Medium Blue',              'Violet',
        'Light Violet',             '',
        'Glow In Dark Opaque',      'Dark Pink',
        'Sand Green',               'Very Light Gray',
        'Trans-Dark Pink',          'Trans-Purple',
        'Chrome Blue',              '',
        'Sand Purple',              'Sand Blue',
        'Light Pink',               'Chrome Antique Brass',
        'Sand Red',                 'Dark Red',
        'Milky White',              'Pearl Light Gold',
        'Light Blue',               'Dark Blue',
        'Chrome Green',             'Metallic Gold',
        'Pearl Light Gray',         'Metallic Silver',
        'Dark Orange',              'Dark Tan',
        'Metallic Green',           'Magenta',
        'Maersk Blue',              'Medium Violet',
        'Trans-Medium Blue',        '',
        'Medium Lime',              'Pearl Dark Gray',
        'Pearl Sand Blue',          '',
        'Dark Green',               'Flat Dark Gold',
        'Chrome Pink',              'Pearl White',
        'Copper',                   'Dark Bluish Gray',
        'Light Bluish Gray',        'Sky Blue',
        'Reddish Brown',            'Dark Purple',
        'Light Nougat',             'Light Brown',
        '',                         'Light Purple',
        'Medium Dark Pink',         'Flat Silver',
        'Very Light Orange',        'Blue-Violet',
        'Trans-Orange',             'Very Light Bluish Gray',
        'Glitter Trans-Dark Pink',  'Glitter Trans-Clear',
        'Glitter Trans-Purple',     'Bright Light Yellow',
        'Bright Pink',              'Bright Light Blue',
        'Fabuland Brown',           'Trans-Pink',
        'Trans-Bright Green',       'Dark Blue-Violet',
        'Bright Light Orange',      'Speckle Black-Silver',
        '',                         'Trans-Aqua',
        'Trans-Light Purple',       'Pearl Gold',
        'Speckle Black-Copper',     'Speckle DBGray-Silver',
        'Glow In Dark Trans',       'Pearl Very Light Gray',
        'Dark Brown',               'Trans-Neon Yellow',
        'Chrome Black',             'Mx White',
        'Mx Light Bluish Gray',     'Mx Light Gray',
        'Mx Charcoal Gray',         'Mx Tile Gray',
        'Mx Black',                 'Mx Red',
        'Mx Pink Red',              'Mx Tile Brown',
        'Mx Brown',                 'Mx Buff',
        'Mx Terracotta',            'Mx Orange',
        'Mx Light Orange',          'Mx Light Yellow',
        'Mx Ochre Yellow',          'Mx Lemon',
        'Mx Olive Green',           'Mx Pastel Green',
        'Mx Aqua Green',            'Mx Tile Blue',
        'Mx Medium Blue',           'Mx Pastel Blue',
        'Mx Teal Blue',             'Mx Violet',
        'Mx Pink',                  'Mx Clear',
        'Medium Nougat',            'Speckle Black-Gold',
        'Light Aqua',               'Dark Azure',
        'Lavender',                 'Olive Green',
        'Medium Azure',             'Medium Lavender',
        'Yellowish Green',          'Glow In Dark White',
        'Fabuland Orange',          'Dark Yellow',
        'Glitter Trans-Light Blue', 'Glitter Trans-Neon Green',
        'Trans-Light Orange',       'Neon Orange',
        'Neon Green',               'Reddish Orange',
        'Umber',                    'Sienna',
        'Satin Trans-Yellow',       '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        '',                         '',
        'Mx Foil Dark Gray',        'Mx Foil Light Gray',
        'Mx Foil Dark Green',       'Mx Foil Light Green',
        'Mx Foil Dark Blue',        'Mx Foil Light Blue',
        'Mx Foil Violet',           'Mx Foil Red',
        'Mx Foil Yellow',           'Mx Foil Orange',
        'Coral',                    'Trans-Light Green',
        'Glitter Trans-Orange',     'Satin Trans-Light Blue',
        'Satin Trans-Dark Pink',    'Dark Nougat',
        'Trans-Light Bright Green', 'Clikits Lavender',
        'Satin Trans-Clear',        'Satin Trans-Brown',
        'Satin Trans-Purple',       'Dark Salmon',
        'Satin Trans-Dark Blue',    'Satin Trans-Bright Green',
        'Trans-Medium Purple',      'Reddish Gold',
        'Neon Yellow',              'Bionicle Copper',
        'Bionicle Gold',            'Bionicle Silver',
        'Medium Brown',             'Medium Tan',
        'Dark Olive Green',         'Pearl Sand Purple',
        'Pearl Black',              'Lilac',
        'Light Lilac',              'Little Robots Blue',
        'Fabuland Lime',            'Reddish Copper',
        'Metallic Copper',          'Trans-Black (2023)',
        'Pearl Red',                'Pearl Green',
        'Pearl Blue',               'Pearl Brown'
        )

# それぞれのショップに対して支払った各通貨の額とJPYで支払った額を対応させる
# TODO: orderxmlで並んでいるORDERの順に店のコストを日本円で割り振っていく必要がある（ORDERIDで対応付ければ良いが、面倒だったので未実装）
# TODO: それぞれの日本円を手動で追記する必要があるand店の数と釣り合っていない時の例外処理を書く必要がある
order_cost_jpy = [1000, 2000] # ←fugaの店舗で1000円、piyoの店舗で2000円かかった時の例

order_tree = ET.parse(order_file)
order_root = order_tree.getroot()

order_list = [] ## [ITEMID, COLOR, int(QTY), float(PRICE), int(ORDERID)]
shop_list = [] ## [int(ORDERID), float(ORDERTOTAL), float(BASEGRANDTOTAL)]

for order in order_root.findall('ORDER'):
    orderid = int(order.find('ORDERID').text)
    ordertotal = order.find('ORDERTOTAL').text
    basegrandtotal = order.find('BASEGRANDTOTAL').text
    shop_list.append([orderid, float(ordertotal), float(basegrandtotal)])
    for item in order.findall('ITEM'):
        itemid = item.find('ITEMID').text
        color = item.find('COLOR').text
        qty = int(item.find('QTY').text)
        price = float(item.find('PRICE').text)
        order_list.append([itemid, color, qty, price, orderid])

# for i in range(5):
#     print(order_list[i])

# for i in range(len(shop_list)):
#     print(shop_list[i][0], shop_list[i][1], shop_list[i][2])

proj_trees = []
proj_roots = []
for proj_file in proj_files:
    proj_tree = ET.parse(proj_file)
    proj_root = proj_tree.getroot()
    proj_trees.append(proj_tree)
    proj_roots.append(proj_root)

proj_cost_list = []

for i in range(len(proj_files)):
    # order_list = [] ## [ITEMID, COLOR, int(QTY), float(PRICE), ORDERID]
    proj_list = [] ## [ITEMID, COLOR, int(MINQTY)]
    proj_cost = [[0.0] * 3 for j in range(len(shop_list))] ## [float(COST), float(ORDERTOTAL), float(BASEGRANDTOTAL)]
    for j in range(len(shop_list)):
        proj_cost[j][0] = 0.0
        proj_cost[j][1] = shop_list[j][1]
        proj_cost[j][2] = shop_list[j][2]
    # print(proj_cost)

    for item in proj_roots[i].findall('ITEM'):
        itemid = item.find('ITEMID').text
        color = item.find('COLOR').text
        minqty = int(item.find('MINQTY').text)
        proj_list.append([itemid, color, minqty])
    
    # for j in range(5):
    #     print(proj_list[j])

    for proj_item in proj_list:
        for order in order_list:
            order_index = -1
            for k in range(len(shop_list)):
                if order[4] == shop_list[k][0]:
                    order_index = k
                    break
            if order_index == -1:
                print(f"order_index: {order[4]} not found")
                continue
            # print(order_index)
            # print(f"proj_item: {proj_item[0]}, {proj_item[1]}, {proj_item[2]}, order: {order[0]}, {order[1]}, {order[2]}")
            if proj_item[0] == order[0] and proj_item[1] == order[1]:
                # print(f"proj_item: {proj_item[0]}, {proj_item[1]}, order: {order[0]}, {order[1]}")
                if proj_item[2] >= order[2]:
                    proj_cost[order_index][0] += float(order[2]) * order[3]
                    proj_item[2] -= order[2]
                    order[2] = 0
                else:
                    proj_cost[order_index][0] += float(proj_item[2]) * order[3]
                    order[2] -= proj_item[2]
                    proj_item[2] = 0
            if proj_item[2] == 0:
                break
    print(f"proj_file: {proj_files[i]}")
    print(proj_cost)
    str_jpy = "JPY: "
    jpy_sum = 0.0
    for j in range(len(shop_list)):
        jpy_each = proj_cost[j][0] * order_cost_jpy[j] / proj_cost[j][1]
        jpy_sum += jpy_each
        str_jpy += str(round(jpy_each, 2)) + ", "
    print(str_jpy)
    print("JPY sum: " + str(round(jpy_sum, 2)))
    print("----------------------")
    proj_cost_list.append(proj_cost)

# それぞれのプロジェクトにおいてかかったコストが、orderxmlで示されている合計コストに一致するか確認
sum_proj_cost = [[0.0] * 2 for i in range(len(shop_list))]
for i in range(len(proj_cost_list)):
    for j in range(len(shop_list)):
        sum_proj_cost[j][0] += proj_cost_list[i][j][0]
        sum_proj_cost[j][1] = proj_cost_list[i][j][1]
print(sum_proj_cost)
print("----------------------")

# order_listの中で、proj_listに含まれなかったものを表示
for order in order_list:
    if order[2] != 0:
        print(f"order: {order[0]}, {colorlist[int(order[1])]}, {order[2]}, {order[3]}, {order[4]} not found")
        continue

