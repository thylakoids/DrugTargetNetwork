import pandas as pd
import sys
import os

sys.path.append('../')
from config import conf

def Uniprot2String(uniprot='Q96P26',string=['ENSP00000352904'],reverse=False):
    '''
    uniprot : list/tuple of uniprot_ac(str)
    return : list of string_id(str)

    eg:
    Uniprot2String(['Q96P26'])

    notes: return nan when no match
    notes: the two direction may not be identical 
    '''
    # convert string to list
    if isinstance(uniprot,str):
        uniprot = [uniprot]
    if isinstance(string,str):
        string = [string]
    # load mapping data
    filePath = conf.FILEPATH_uniprot2string
    data = pd.read_csv(filePath,sep=r'\s+|\|',engine='python')
    if not reverse:
        # remove duplicate
        data = data.drop_duplicates(subset=['uniprot_ac'])
        # query id
        query_Uniprot_ac = pd.DataFrame(list(uniprot),columns=['uniprot_ac'])
        result = pd.merge(query_Uniprot_ac,data,how='left',on='uniprot_ac')
        result =  list(result['string_id'])
    else:
        # remove duplicate
        data = data.drop_duplicates(subset=['string_id'])
        query_string_id = pd.DataFrame(list(string),columns=['string_id'])
        result = pd.merge(query_string_id,data,how='left',on='string_id')
        result = list(result['uniprot_ac'])
    return result

    

def String2Uniprot(string=['ENSP00000352904']):
    return Uniprot2String(string=string,reverse=True)

if __name__ == '__main__':
    print Uniprot2String(reverse=False)