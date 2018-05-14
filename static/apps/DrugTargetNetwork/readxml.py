#coding:utf-8
#parse full database.xml and save it to mysql
#from:full database.xml
from xml.etree import cElementTree as ET
import pymysql
import time
#connect to mysql,utf-8
conn=pymysql.connect(user='root',charset='utf8')
cur=conn.cursor()
cur.execute('use drugbank')

#creat database
cur.execute('CREATE DATABASE IF NOT EXISTS drugbank')
cur.execute('use drugbank')
#create tabel
cur.execute('CREATE TABLE IF NOT EXISTS drugbank(primDrugbankID varchar(15),drugType varchar(20),name varchar(1000),casNumber varchar(20),drugGroup varchar(100),atcCode varchar(2000),targets varchar(2000),FDA int(3),targetsAll varchar(2000),primary key (primDrugbankID))')
start=time.time()
print 'loading xml----------------------->>' 
drugbank=ET.parse('doc/full database.xml').getroot()
loadedtime=time.time()
loadingtime=loadedtime-start
totaldrug=len(drugbank)
print ('done loading! Time:%.2fs'%loadingtime)
print ('total drug:%d'%totaldrug)
drugsql=0
for drug in drugbank:
    #type
    drugType=drug.attrib['type']
    #name ID 
    name= drug.find('./name').text
    primDrugbankID=drug.find('./drugbank-id[@primary="true"]').text
    print primDrugbankID
    #cas
    casNumber=drug.find('./cas-number')
    casNumber=drug.find('./cas-number').text if casNumber is not None else None
    #groups
    group=';'.join([x.text for x in drug.find('./groups')])
    #atcCodes
    atcCode=drug.find('./atc-codes')
    atcCodeAll=None
    if atcCode is not None:
        atcCode=';'.join([x.attrib['code'] for x in drug.findall('./atc-codes/atc-code')])
        atcCodeAll=';'.join(['%'.join([x.text for x in atccode.findall('level')])   for atccode in drug.findall('./atc-codes/atc-code')])
    #targets exits? nonetype?
    targets=drug.find('./targets')
    targetsAll=None
    if targets is not None:
        targets=';'.join([x.attrib['id'] for x in drug.findall('./targets/target/polypeptide')])
        targetsAll=';'.join(['#'.join([action.text for action in actions]) for actions in drug.findall('./targets/target/actions')])
        #targetsAll=';'.join(['%'.join(['%'.join([x.text if x.text else 'Not Available' for x in target[0:3]]),'#'.join(x.text for x in target[3])]) for target in drug.findall('./targets/target')])
    #FDA
    approved=drug.findall('./products/product/source')
    FDA=0
    if approved is not None:
        approved=';'.join([x.text for x in approved]) 
        FDA=1 if 'FDA' in approved else 0
    try:
        cur.execute('INSERT INTO drugbank(primDrugbankID,drugType,name,casNumber,drugGroup,atcCode,targets,FDA,targetsAll) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(primDrugbankID,drugType,name,casNumber,group,atcCode,targets,FDA,targetsAll))
    except Exception,e:
        print e
        raw_input( )
    conn.commit()
    drugsql+=1
    usedtime=time.time()-loadedtime
    remainingtime=1.0*totaldrug*usedtime/drugsql - usedtime
    process=100.0*drugsql/totaldrug;
    print '%d/%d drugs:%.2fs'% (drugsql,totaldrug,time.time()-loadedtime)
    print 'process:%.2f  remainint time:%.2fs'%(process,remainingtime)
    print int(round(process))*'='
cur.close()
conn.close()
