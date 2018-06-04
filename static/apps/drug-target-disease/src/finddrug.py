import pandas as pd 
import numpy as np 



'''
ICD10 :"C11, C44, K75.9, M00-M25", I20-I25
icd : C11-I22 


'''
def compare(icd,icdrange ):
    ranges = icdrange.split('-')
    icd = icd.strip(' ')
    if '-' in icd:
        icds = icd.split('-')

        return icds[0]<=ranges[1] and icds[1]>=ranges[0]
    else:
        return icd>=ranges[0] and icd<=ranges[1]


def isneoplasms(ICD10,icdrange):
    # print ICD10
    try:    
        ICD10 = ICD10.strip('"')
        ranges = icdrange.split('-')
        ICD10s = ICD10.split(',')

        for icd in ICD10s:
            icd = icd.strip(' ')
            if compare(icd,icdrange):
                return True
                break
        else:
            return False
    except:
        return False #nan

def isInUniprot(target,uniprot):

    n = 0 #how many targets of the drug is related
    try:
        targets = target.split(';')
        for t in targets:
            if t in uniprot:
                n+=1
    except: #nan
        n = 0
    return n

def getDrug(icdrange):
    druginbankPath = '../out/druginbank.csv'
    druginbank = pd.read_csv(druginbankPath)
    uniprot = getUniprot(icdrange) # targets
    print 'targets:',len(uniprot)
    b = [isInUniprot(x,uniprot) for x in druginbank['targets'] ] #ntargets
    


    druginbank['ntargets']=b
    df=druginbank[druginbank['ntargets']>0]
    df = df[df['FDA']==1]

    df=df.sort_values('ntargets',ascending=False)
    df.to_csv('../out/tumordrug.csv')


    # dup = ['L' not in x for x in df['tsID']]
    # print sum(dup)
    print 'drugs:',len(df['primDrugbankID'].unique())


def getUniprot(icdrange):
    '''
    find disease related targets(uniprot) 
    '''
    targetDiseasePath = '../out/target-disease.csv'
    targetDisease = pd.read_csv(targetDiseasePath)

    # get Uniprot
    b = [isneoplasms(x,icdrange) for x in targetDisease['ICD10']]
    df = targetDisease[b]
    df.to_csv('../out/neoplasms.csv')
    uniprot = df['Uniprot ID'].unique()  
    return uniprot
if __name__ =='__main__':
    getDrug('C34-C34.9')
    
