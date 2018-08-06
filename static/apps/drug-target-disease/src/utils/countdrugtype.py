import pandas as pd
def bar(topf):	
	atcdb=pd.read_csv('../data/atc.csv')
	atc=topf['atcs'].fillna('V')
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