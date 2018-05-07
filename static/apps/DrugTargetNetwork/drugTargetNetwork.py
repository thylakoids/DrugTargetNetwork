#coding:utf-8
#read data from file, and translate to network
#from: target.csv
#to:networkNodes.csv
#to:networkNodes.csv
import pandas as pd 
def addnewrow(df,row):
	d=pd.DataFrame(row).T
	d.columns=df.columns
	df=pd.concat([df,d],ignore_index=True)
	return df

def netdata():
	target_all=pd.read_csv('doc/target.csv')
	edges=pd.DataFrame(columns=['from','to']);
	nodes=pd.DataFrame(columns=['id','label','group']);
	for index,row in target_all.iloc[0:500,:].iterrows():
		nodes=addnewrow(nodes,[row['ID'],row['Name'],'Target'])
		drugids=row['Drug IDs'].split(';')
		for drugid in drugids:
			nodes=addnewrow(nodes,[drugid,drugid,'drug'])
			edges=addnewrow(edges,[drugid,row['ID']])
	return nodes.drop_duplicates(),edges.drop_duplicates()
nodes,edges=netdata()
nodes.to_csv('doc/networkNodes.csv',index=False)
edges.to_csv('doc/networkEdges.csv',index=False)

