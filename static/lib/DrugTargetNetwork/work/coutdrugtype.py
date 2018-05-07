#coding:utf-8
#drug statics
#read top100.csv
import pandas as pd 
top100=pd.read_csv('top100.csv').fillna('V')
def bar(topf):	
	atcdb=pd.read_csv('atc.csv')
	atc=topf['atc']
	#deal nan and combine 
	atcs=''
	for x in atc:
		tmp=x.split(';')
		tmp=list(set([x[0] for x in tmp]))
		tmp=''.join(tmp)
		atcs+=tmp
	result=dict()
	for x in atcs:
		x=atcdb['abbclass'][atcdb.ATC==x].values[0]
		if x in result:
			result[x]+=1
		else:
			result[x]=1
	return result
result100=bar(top100)
resultsmall=bar(top100[top100.drugType=='small molecule'])
resultbio=bar(top100[top100.drugType=='biotech'])
','.join([str(resultsmall[x]) for x in result100])
','.join([str(resultbio[x]) if x in resultbio else '' for x in result100])



