#coding:utf-8
#flask frame for network visualization
#vis.js
from flask import Flask,render_template
import json
import pandas as pd
import re
#function to read data from excel
def frame2json(df):
	d=[
	dict(
		[(colname,row[i] )for i,colname in enumerate(df.columns)]
		) 
	for row in df.values]
	return json.dumps(d)
def getdata(fnode,fedge):
	def readfile(fs):
		import re
		if re.search('\.csv',fs):
			fdata=pd.read_csv(fs)
		elif re.search('\.xlsx',fs):
			fdata=pd.read_excel(fs)
		return fdata
	data={'nodes':readfile(fnode),'edges':readfile(fedge)}
	return frame2json(data['nodes']),frame2json(data['edges'])
nodes,edges=getdata('static/lib/miRNA/nodesZhu.xlsx','static/lib/miRNA/edgesZhu.xlsx')

Dnodes,Dedges=getdata('static/lib/DrugTargetNetwork/top100Nodes.csv','static/lib/DrugTargetNetwork/top100Edges.csv')
app=Flask(__name__,static_url_path='')
@app.route('/miRNA')
def netvisualize():
	return render_template('miRNA.html',nodes=nodes,edges=edges)

@app.route('/DTN')
def Dnetvisualize():
	return render_template('miRNA.html',nodes=Dnodes,edges=Dedges)
@app.route('/bar')
def bar():
	return render_template('ec.html')
if __name__=='__main__':
	app.run(debug=True,threaded=True,port=4001,host='127.0.0.1')