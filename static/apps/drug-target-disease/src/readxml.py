#coding:utf-8
#parse full database.xml and save it to mysql
#from:full database.xml
#to:pymysql.drugbank.drugbank5.1

from xml.etree import cElementTree as ET
import pymysql
import time
import re
import pandas as pd 

def loadxml(xmlfilepath):
    start = time.time()
    print '*'*30+'loading {}'.format(xmlfilepath)
    drugbank=ET.parse(xmlfilepath).getroot()
    loadedtime=time.time()
    loadingtime=loadedtime-start
    totaldrug=len(drugbank)
    print ('done loading! Time:%.2fs'%loadingtime)
    version = drugbank.attrib['version']

    print 'version:{}'.format(version)
    print ('total drug:%d'%totaldrug)
    return drugbank
def getprefix(drugbank):
    tag = drugbank[0].tag
    try:
        return re.findall('{.+}',tag)[0]
    except:
        return ''
def fixpath(prefix,xpath):
    path = xpath.replace('/','/'+prefix)
    return path
def save2mysql(drugbank,drop=False):#todo
    #connect to mysql,utf-8
    conn=pymysql.connect(user='root',charset='utf8')
    cur=conn.cursor()

    #creat database drugbank
    cur.execute('CREATE DATABASE IF NOT EXISTS drugbank')
    cur.execute('use drugbank')

    #creat table V5v1
    version = drugbank.attrib['version']
    versions = version.split('.')
    tablename = 'V{}v{}'.format(versions[0],versions[1])
    if drop:
        cur.execute('DROP TABLE IF EXISTS {}'.format(tablename))

    cur.execute('CREATE TABLE IF NOT EXISTS {}(primDrugbankID varchar(15),drugType varchar(20),name varchar(1000),casNumber varchar(20),drugGroups varchar(100),atcCodes varchar(2000),targets varchar(2000),FDA int(3),actionss varchar(2000),primary key (primDrugbankID))'.format(tablename))
    conn.commit()
    # save the drugbank to mysql
    prefix = getprefix(drugbank)
    loadedtime = time.time()
    totaldrug=len(drugbank)
    drugsql=0
    for drug in drugbank:
        #type
        drugType=drug.attrib['type']
        #name ID 
        name= drug.find(fixpath(prefix,'./name')).text
        primDrugbankID=drug.find(fixpath(prefix,'./drugbank-id[@primary="true"]')).text
        print primDrugbankID

        #cas
        try:
            casNumber = drug.find(fixpath(prefix,'./cas-number')).text
        except:
            casNumber = None
        #groups approved;approved
        groups=';'.join([x.text for x in drug.find(fixpath(prefix,'./groups'))])
        #atcCodes
        try:
            atcCodes = ';'.join([x.attrib['code'] for x in drug.findall(fixpath(prefix,'./atc-codes/atc-code'))])
        except:
            atcCodes = None


        #targets exits? nonetype?
        try:
            targets=';'.join([x.attrib['id'] for x in drug.findall(fixpath(prefix,'./targets/target/polypeptide'))])
            actionss=';'.join(['#'.join([action.text for action in actions]) for actions in drug.findall(fixpath(prefix,'./targets/target/actions'))])
        except:
            targets = None
            actionss = None
            
        #FDA
        products = drug.findall(fixpath(prefix,'./products/product'))
        for product in products:
            source = product.find(fixpath(prefix,'./source')).text
            if 'FDA' in source:
                FDA = 1
                break
        else:
            FDA = 0


        try:

            cur.execute('INSERT INTO {}(primDrugbankID,drugType,name,casNumber,drugGroups,atcCodes,targets,FDA,actionss) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'.format(tablename),(primDrugbankID,drugType,name,casNumber,groups,atcCodes,targets,FDA,actionss))
            conn.commit()
        except Exception,e:
            print e
            conn.rollback()
            raw_input()
        drugsql+=1
        usedtime=time.time()-loadedtime
        remainingtime=1.0*totaldrug*usedtime/drugsql - usedtime
        process=100.0*drugsql/totaldrug;
        print '%d/%d drugs:%.2fs'% (drugsql,totaldrug,time.time()-loadedtime)
        print 'process:%.2f  remainint time:%.2fs'%(process,remainingtime)
        print int(round(process))*'='

    cur.close()
    conn.close()

def main():
    
    xmlfilepath = '../data/full database.xml'
    drugbank = loadxml(xmlfilepath)
    save2mysql(drugbank,drop=True)

if __name__ == '__main__':
    main()

