#coding:utf-8
#read data from file, and translate to network
#read top100.csv, top100 network
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
	atcdb=pd.read_csv('work/atc.csv')
	return atcdb['abbclass'][atcdb.ATC==atcone].values[0]
def netdata():
	target_all=pd.read_csv('top100.csv').fillna('nan')
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
nodes.to_csv('top100Nodes.csv',index=False)
edges.to_csv('top100Edges.csv',index=False)

