import json

currently_owners=[]
past_owners=[]
common_data=[]
with open('result.json') as json_file:
    data = json.load(json_file)
    #Tratamento de common
    common = data['common']
    common_data = [[field['special_label'], field['revised_text']] for field in common['named_entities']]
    #Tratamento de Owners
    owners = data['owners']
    for owner in owners:
        owner_temp=[]
        for fields in owner['named_entities']:
            owner_temp.append(fields['revised_text'])
        if(owner['current']):
            currently_owners.append(owner_temp)
        else:
            past_owners.append(owner_temp)
requests=[]

for i in common_data:
    teste = {
                'replaceAllText': {
                    'containsText': {
                        'text': '{{{{{}}}}}'.format(i[0]),
                        'matchCase':  'true'
                    },
                    'replaceText': '{}'.format(i[1]),
                }
            }
    

    requests.append(teste)

print(type(requests))
print(requests)
