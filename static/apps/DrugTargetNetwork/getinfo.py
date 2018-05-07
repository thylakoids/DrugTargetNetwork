#coding:utf-8
#get the infomation of topdrugs from mysql
#from:top100retail_name.csv
#to:top100.csv
import pymysql
import time
import pandas as pd 
def main():
	conn=pymysql.connect(user='root',charset='utf8')
	cur=conn.cursor()
	cur.execute('use drugbank')
	def addnewrow(df,row):
		d=pd.DataFrame(list(row)).T
		d.columns=df.columns
		df=pd.concat([df,d],ignore_index=True)
		return df
	top100=pd.DataFrame(columns=['primDrugbankID','drugType','name','cas','atc','targets','targetsAll'])
	top100name=pd.read_csv('doc/top100retail_name.csv')	

	for drug in top100name['name']:
		print drug
		cur.execute('select primDrugbankID,drugType,name, casNumber,atcCode,targets,targetsAll from drugbank where name=%s ',drug)
		x=cur.fetchone()
		top100=addnewrow(top100,x)
	cur.close()
	conn.close()
	top100.to_csv('doc/top100.csv',index=False)

if __name__=='__main__':
	main()

