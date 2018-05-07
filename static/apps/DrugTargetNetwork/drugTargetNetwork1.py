#coding:utf-8
#read data from file, and translate to network
#from:top100.csv
#from:atc.csv
#to:top100Nodes.csv
#to:top100Edges.csv
import pandas as pd 
def addnewrow(df,row):
	d=pd.DataFrame(row).T
	d.columns=df.columns
	df=pd.concat([df,d],ignore_index=True)
	return df
def getatcabbr(atc):
	if atc =='nan':
		atcone='V'
	else:
		atcone=atc.strip()[0]
	atcdb=pd.read_csv('doc/atc.csv')
	return atcdb['abbclass'][atcdb.ATC==atcone].values[0]
def netdata():
	target_all=pd.read_csv('doc/top100.csv').fillna('nan')
	edges=pd.DataFrame(columns=['from','to']);
	nodes=pd.DataFrame(columns=['id','label','group','shape','title']);
	for index,row in target_all.iterrows():
		print index
		nodes=addnewrow(nodes,[row['primDrugbankID'],row['name'],getatcabbr(row['atc']),'dot',getatcabbr(row['atc'])])
		targetids=row['targets'].split(';') if row['targets'] !='nan' else []
		for targetid in targetids:
			nodes=addnewrow(nodes,[targetid,targetid,'target','box','target'])
			edges=addnewrow(edges,[row['primDrugbankID'],targetid])
	return nodes.drop_duplicates(),edges.drop_duplicates()
nodes,edges=netdata()
nodes.to_csv('doc/top100Nodes.csv',index=False)
edges.to_csv('doc/top100Edges.csv',index=False)

