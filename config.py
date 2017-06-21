token = '411245168:AAFOx4aRwPd45F_mtTjVLjcxqycTqeEo2ig' \
        '' \
        ''
request = 'https://api.telegram.org/bot<297545998:AAEW7FEyEiu6fTVhfIzg0AA_QInPfnnVCaQ>/'

import json
with open('custom_buttons.json') as data_file:
    custom_butons = json.load(data_file)
# n = 0
# for i in list(custom_butons.keys()):
#     print(i)
#     if i == 'user_dir_name':
#         n+=1
# print(n)
print(custom_butons.get('user_dir_name' + '1'))