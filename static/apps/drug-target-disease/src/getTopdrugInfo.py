#coding:utf-8
#get the infomation of topdrugs from mysql
#from:druglibpath
#to:fromcas.csv , outcas.csv
'''
ts: top science
'''
import pymysql
import time
import pandas as pd 
import re 

def addnewrow(df,row):    
    if row:
        d=pd.DataFrame(list(row)).T
        d.columns=df.columns
        df=pd.concat([df,d],ignore_index=True)
    return df

def searchCAS(cass,df):
    conn=pymysql.connect(user='root',charset='utf8')
    cur=conn.cursor()
    cur.execute('use drugbank')
    top100=pd.DataFrame(columns=['primDrugbankID','drugType','name','cas','atcs','targets','actionss'])

    wrongcas = []
    for cas_raw in cass:
        cas = re.findall('[0-9]+-[0-9]+-[0-9]+',cas_raw)[0]
        cur.execute('select primDrugbankID,drugType,name, casNumber,atcCodes,targets,actionss from V5v1 where casNumber=%s ',cas)
        x=cur.fetchone()
        if  x:
            top100=addnewrow(top100,x)
        else:            
            wrongcas.append(cas_raw)
    cur.close()
    conn.close()
    print 'total drugs:{}'.format(len(top100))
    top100.to_csv('../out/druglibFromCAS.csv',index=False)
    print 'save file at:{}'.format('../out/druglibFromCAS.csv')

    wrongcas = pd.DataFrame(wrongcas,columns=['CAS'])
    dfoutcas = pd.merge(df, wrongcas,how='right',right_on='CAS',left_on='CAS')
    dfoutcas.to_csv('../out/druglibOutCAS.csv',index=False,encoding='utf-8')
    print 'save file at:{}'.format('../out/druglibOutCAS.csv')

def searchName(df):
    # mysql
    conn=pymysql.connect(user='root',charset='utf8')
    cur=conn.cursor()
    cur.execute('use drugbank')
    #result
    result=pd.DataFrame(columns=['primDrugbankID','drugType','name','cas','atcs','targets','actionss','tsName'])
    outresult=[]
    for i in range(len(df)):
        name = df['Name'][i]
        print name
        #search
        cur.execute('select primDrugbankID,drugType,name, casNumber,atcCodes,targets,actionss from V5v1 where name=%s ',name)
        x=cur.fetchone()
        if not x: #try to search the first part of name
            cur.execute('select primDrugbankID,drugType,name, casNumber,atcCodes,targets,actionss from V5v1 where name=%s ',name.split()[0])
            x=cur.fetchone()

        if x:
            x=list(x)
            x.append(name)
            result = addnewrow(result,x)
        else:
            outresult.append(name)

    #end of the search
    cur.close()
    conn.close()

    #save the result
    result.to_csv('../out/druglibFromName.csv',index=False)
    outresult = pd.DataFrame(outresult,columns=['Name'])
    outresult = pd.merge(df, outresult,how='right',right_on='Name',left_on='Name')
    outresult.to_csv('../out/druglibOutName.csv',index=False,encoding='utf-8')

def searchinfo(df):
    # mysql
    conn=pymysql.connect(user='root',charset='utf8')
    cur=conn.cursor()
    cur.execute('use drugbank')
    #result
    result=pd.DataFrame(columns=['primDrugbankID','drugType','name','cas','atcs','targets','actionss','FDA','tsID','tsName'])
    outresult=[]
    j=0
    for i in range(len(df)):
        cas_raw = df['CAS'][i]
        cas = re.findall('[0-9]+-[0-9]+-[0-9]+',cas_raw)[0]
        name = df['Name'][i]
        #search the casNumber
        cur.execute('select primDrugbankID,drugType,name, casNumber,atcCodes,targets,actionss,FDA from V5v1 where casNumber=%s ',cas)
        x=cur.fetchone()
        # if not x: #search name
        #     cur.execute('select primDrugbankID,drugType,name, casNumber,atcCodes,targets,actionss,FDA from V5v1 where name=%s ',name)
        #     x=cur.fetchone()
        # else:
        #     j+=1
        # if not x: #try to search the first part of name
        #     cur.execute('select primDrugbankID,drugType,name, casNumber,atcCodes,targets,actionss,FDA from V5v1 where name=%s ',name.split()[0])
        #     x=cur.fetchone()
        if x:
            x=list(x)
            tsID = df['ID'][i]
            x.append(tsID)
            x.append(name)
            result = addnewrow(result,x)
        else:
            outresult.append(name)

    #end of the search
    cur.close()
    conn.close()

    #save the result
    result.to_csv('../out/druginbank.csv',index=False,encoding='Utf-8')
    outresult = pd.DataFrame(outresult,columns=['Name'])
    outresult = pd.merge(df, outresult,how='right',right_on='Name',left_on='Name')
    outresult.to_csv('../out/drugoutbank.csv',index=False,encoding='utf-8')
    print len(df)
    print len(result)
    print len(outresult)
def steps():
    #step1
    druglibpath = '../doc/L1000-Targetmol-Approved Drug Library.xlsx'
    df = pd.read_excel(druglibpath)
    casNumbers = df['CAS']
    searchCAS(casNumbers,df)
    # step2
    outcas = '../out/druglibOutCAS.csv'
    df = pd.read_csv(outcas)
    searchName(df)

def Targetmol2Drugbank():
    druglibpath = '../doc/L1000-Targetmol-Approved Drug Library.xlsx'
    df = pd.read_excel(druglibpath)# CAS Name ID
    searchinfo(df)
def getUniprotlist():
    druginbankpath = '../out/druginbank.csv'
    df = pd.read_csv(druginbankpath)

    uniprot = []
    targets = df['targets']
    for target in targets:
        try:
            uniprot.extend(target.split(';'))
        except : #nan case
            pass
    uniprot = list(set(uniprot))
    print len(uniprot)
    return uniprot

def load_TTD(file):
    df = pd.read_csv(file,sep='\t')
    return df

def uniprot2TTD():
    #load the data as Dataframe
    TTD_uniprot = '../data/P2-01-TTD_uniprot_all.csv'
    TTD_disease = '../data/P1-05-Target_disease.csv'
    uniprot = getUniprotlist()
    uniprot = pd.DataFrame(uniprot,columns = ['Uniprot ID'])
    TTD_uniprot = load_TTD(TTD_uniprot)
    TTD_disease = load_TTD(TTD_disease)

    #uniprot-TTD
    TTD = pd.merge(uniprot,TTD_uniprot,how='inner',on='Uniprot ID')
    #TTD-ICD10
    disease = pd.merge(TTD,TTD_disease[['TTDTargetID','ICD10']],how='inner',left_on='TTD Target ID',right_on='TTDTargetID')
    disease.to_csv('../out/target-disease.csv',index=False,encoding='utf-8')
    print len(disease)
    return disease
    

if __name__=='__main__':
    #step 1
    Targetmol2Drugbank()

    #step 2
    uniprot2TTD()