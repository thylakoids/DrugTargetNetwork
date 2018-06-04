import pymysql
import pickle

import pandas as pd
import networkx as nx
import nxviz as nv  
import numpy as np 
import matplotlib.pyplot as plt

from finddrug import getUniprot
from utils.mappingID import Uniprot2String



def buildPPIFromDisease(icdrange='C34-C34.9'):
    uniprot_list = getUniprot(icdrange)
    #nodes info
    string_list = Uniprot2String(uniprot_list)
    #edge info
    edge_list =[]
    ppi_all_df=pd.read_csv('../out/ppi_ensp.txt',sep=' ')

    for i in range(len(ppi_all_df)):
        protein1=ppi_all_df.iloc[i,0]
        protein2=ppi_all_df.iloc[i,1]

        if protein1 in string_list and protein2 in string_list:
            edge_list.append((protein1,protein2))

    # convery string_id to uniprot_ac
    def String2Uniprot(query):
        mapping = [string_list,uniprot_list]
        index = [mapping[0].index(b) for b in query]
        return mapping[1][index]
    edges = zip(*edge_list)
    edge_list = zip(String2Uniprot(edges[0]),String2Uniprot(edges[1]))

    G = nx.Graph()
    G.add_nodes_from(uniprot_list)
    G.add_edges_from(edge_list)
    return G

def buildDTNFromDisease(icdrange='C34-C34.9'):
    # connet mysql
    conn=pymysql.connect(user='root',charset='utf8')
    cur=conn.cursor()
    cur.execute('use drugbank')
    #search target-drug relations
    # edges
    uniprot_list = getUniprot(icdrange)
    edge_list=[]
    for target in uniprot_list:
        cur.execute("select primDrugbankID from V5v1 where targets regexp %s",target)
        drugs=cur.fetchall()
        if drugs:
            for drug in drugs:
                edge_list.append((target,drug[0]))                
        else:
            print 'no drug found!'            
    # nodes
    nodes = zip(*edge_list)
    node_list = list(set(nodes[1]))
    node_list.extend(list(set(nodes[0])))

    # for debug -------------------------------
    print 'number edge:', len(edge_list)
    print 'number targets:',len(set(nodes[0]))
    print 'number drugs:',len(set(nodes[1]))
    print 'number nodes', len(node_list)
    # -----------------------------------------

    G = nx.Graph()
    G.add_nodes_from(node_list)
    G.add_edges_from(edge_list)
    return G





def getDrugImportance():
    '''
    assign a importance score to each disease related drug
    return: DataFrame
    head:
              importance primDrugbankID
    0           17.0        DB08424
    1           17.0        DB08423
    2           11.0        DB08422
    '''
    ######build net
    # ppi = buildPPIFromDisease()
    DTN = buildDTNFromDisease()
    ######save net
    # with open('ppi.txt','w') as f:
    #     ppi = pickle.dump(ppi,f)
    ######load net
    with open('../out/ppiNetwork.txt','r') as f:
        ppi = pickle.load(f)
    ######analysis  
    target_list = list(ppi.node)
    drug_list = list(set.difference(set(DTN.node),set(target_list)))
    targetDrug_list=target_list[:]
    targetDrug_list.extend(drug_list)
    # degree of ppi
    ppi_A = nx.to_numpy_array(ppi,nodelist=target_list)
    
    target_degree = ppi_A.sum(axis=0)+1 # those degree = 0
    # importance of drus
    DTN_A = nx.to_numpy_array(DTN,nodelist=targetDrug_list)

    DTN_A = DTN_A[:len(ppi),len(ppi):]

    drug_ip=[]#drug importance
    for i in range(DTN_A.shape[1]):
        drug_ip.append(np.dot(DTN_A[:,i],target_degree))


    df_drugIP=pd.DataFrame({'primDrugbankID':drug_list,'importance':drug_ip})
    #todo: correction drug_ip by devide number_target of each drug
    return df_drugIP


def getTopScienceDrugInfo():
    # read topscience data info,produced by getTopdrugInfo.py
    df_drugts = pd.read_csv('../out/druginbank.csv')
    #
    def targetsNumber(targets):
        try:
            return len(targets.split(';'))
        except Exception as e:
            return 0

    targetsNumber = [targetsNumber(targets) for targets in df_drugts['targets']]
    df_drugts['targetsNumber']=targetsNumber
    return df_drugts
def main():
    df_drugts=getTopScienceDrugInfo()
    df_drugIP=getDrugImportance()
    df_result =  pd.merge(df_drugts,df_drugIP,how='inner',on='primDrugbankID')
    df_result['normalImportance']=df_result['importance']/df_result['targetsNumber']
    df_result.sort_values(by='normalImportance',ascending = False,inplace=True)
    df_result[df_result['FDA']==1].to_csv('../out/choose_drugs.csv')
    return df_result   
if __name__ == '__main__':
    main()
    
    




