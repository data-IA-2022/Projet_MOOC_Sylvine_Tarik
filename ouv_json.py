import json


# with open('sample.json') as f:
#     for line in f:
#         # print(line)
#         x=json.loads(line)
#         utils.nombre_messages(x)
#         # print(json.dumps(x, indent=2)) # equivalent au pp_json sous bash

# en chantier
with open('sample_user.json') as f:
    username_len_list = []
    for line in f:
        # print(line)
        x=json.loads(line)
        username_len = len(x['username'])
        username_len_list.append(username_len)
    print(max(username_len_list))