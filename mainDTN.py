#coding:utf-8
#flask frame for network visualization
#vis.js
from flask import Flask,render_template
import json
import pandas as pd
#function to read data from excel
def frame2json(df):
	d=[
	dict(
		[(colname,row[i] )for i,colname in enumerate(df.columns)]
		) 
	for row in df.values]
	return json.dumps(d)
def getdata(fnode,fedge):
	data={'nodes':pd.read_excel(fnode),'edges':pd.read_excel(fedge)}
	return frame2json(data['nodes']),frame2json(data['edges'])
nodes,edges=getdata('static/lib/miRNA/nodesZhu.xlsx','static/lib/miRNA/edgesZhu.xlsx')
app=Flask(__name__,static_url_path='')
@app.route('/miRNA')
def netvisualize():
	return render_template('miRNA.html',nodes=nodes,edges=edges)

if __name__=='__main__':
	app.run(debug=True,threaded=True,port=4000,host='127.0.0.1')