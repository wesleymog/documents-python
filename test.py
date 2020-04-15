from __future__ import print_function
import pickle
import os.path
import json
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from gdoctableapppy import gdoctableapp

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1xxpl8MBLvG2HwIxuLGHNN-c9eIl5I1oGnzLS9IkrvIw'

def main():
    common_data, currently_owners, past_owners, special_transactions, transactions = jsonToArray()
    creds = connection()
    service = build('docs', 'v1', credentials=creds)

    lco, lt, lst = len(currently_owners),len(transactions), len(special_transactions)
    #criar tabela de special_transactions
    createTables(lst,1, 1,530,service)
    #criar tabela de transactions
    createTables(lt,1, 1,421,service)
    #criar tabela de owners
    createTables(lco,len(currently_owners[0]),2,407,service)
    for i in range(lco):
        insertTableOwner(creds, i, currently_owners[i])
    for i in range(lco,lco+lt):
        insertTable(creds, i, transactions[i-lco])
    for i in range(lco+lt,lco+lt+lst):
        insertTable(creds, i, transactions[i-lco-lt])
    insertCommon(common_data, service)
    
def connection():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds
def jsonToArray():
    currently_owners=[]
    past_owners=[]
    common_data=[]
    special_transactions=[]
    transactions=[]
    with open('result.json') as json_file:
        data = json.load(json_file)
        #Tratamento de common
        common = data['common']
        common_data = [[field['special_label'], field['revised_text']] for field in common['named_entities']]
        special_transections = [[field['real_text']] for field in data['special_transactions']]
        transactions = [[field['real_text']] for field in data['transactions']]
        #Tratamento de Owners
        owners = data['owners']
        for owner in owners:
            owner_temp={}
            for i in owner['named_entities']:
                owner_temp[i['label']] = i['revised_text']
            if(owner['current']):
                currently_owners.append(owner_temp)
            else:
                past_owners.append(owner_temp)
    return common_data, currently_owners, past_owners, special_transactions, transactions
def insertCommon(common_data, service):
    requests= []
    for i in common_data:
        request = {
                    'replaceAllText': {
                        'containsText': {
                            'text': '{{{{{}}}}}'.format(i[0]),
                            'matchCase':  'true'
                        },
                        'replaceText': '{}'.format(i[1]),
                    }
                }
        requests.append(request)
    result = service.documents().batchUpdate(
        documentId=DOCUMENT_ID, body={'requests': requests}).execute()
def createTables(num_tables,num_rows,num_col,index, service):
    for i in range(num_tables):    
        requests = [{
            'insertTable': {
                'rows': num_rows,
                'columns': num_col,
                'location': {
                    'index': index,
                    'segmentId':''
                }
            },
        }]
        result = service.documents().batchUpdate(
            documentId=DOCUMENT_ID, body={'requests': requests}).execute()
def insertTableOwner(creds, index, owner):
    resource = {
        "oauth2": creds,
        "documentId": DOCUMENT_ID,
        "tableIndex": index,
        "values": [
            ["Nome", owner['PER']], ["Tipo Documento - I", "Identidade"], 
            ["Nº Documento",  owner['id_card']], ["Órgão Emissor",  owner['id_card_issuing_agency']], 
            ["Tipo Documento - II",  "CPF"], ["Nº Documento",  owner['cpf']], 
            ["Órgão Emissor",  owner['cpf']], 
            ["Profissão",  owner['profession']], 
            ["Estado Civíl",  "viuva"],
            ["Porcentagem de Participação",  owner['portion']], 
            ["Título Aquisitivo",  owner['property_purchase_title']], 
            ["Data de Aquisição",  owner['register_date']], 
            ["Endereço do Proprietário",  owner['address']]
        ]

    }
    res = gdoctableapp.SetValues(resource)
def insertTable(creds, index, transaction):
    resource = {
        "oauth2": creds,
        "documentId": DOCUMENT_ID,
        "tableIndex": index,
        "values": [[str(transaction)]]

    }
    res = gdoctableapp.SetValues(resource)
def makeDict(a,b):
    dict = {}
    for A, B in zip(a, b):
        dict[A] = B
    return dict


if __name__ == '__main__':
    main()