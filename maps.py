from flask import Flask
from flask import render_template, request
import json
import re
import sys
import math 

# creates a Flask application, named app
app = Flask(__name__)

#########################################################
@app.route("/")
def hello():
    message = "Hello, World"
    return render_template('index.html', message=message)

#########################################################
@app.route("/manufacturing", methods=['GET','POST'])
def manufacturing():
	title = "Manufacturing"
	if request.method == "POST":
		title = request.form['sectorInput']

	data = GetManufacturingData(title)

	title = data[0]
	maxValue = data[1]
	tickInterval = data[2]
	return render_template('manufacturing.html', 
		title=title,
		maxValue=maxValue,
		tickInterval=tickInterval
		)



#########################################################
if __name__ == "__main__":
    app.run(host='0.0.0.0')



#########################################################
def GetManufacturingData(targetSector):
	# get manufacturing cencus data (2012)
	filename = "./ECN_2012_US_31A1_with_ann.csv"
	with open(filename) as f:
	    content = f.readlines()

	content = [x.strip() for x in content] 

	#get state codes JSON
	with open('./state-codes.json') as json_file:
	    stateCodes = (dict)(json.load(json_file))

	#Parse Data
	numberPerState = []
	maxValue = 0
	for state, code in stateCodes.items():
		
		for csvLine in content:
			lineSplit = csvLine.split(",")
			#lineSplit[2] = State name
			#lineSplit[4] = Sector
			#lineSplit[7] = Number of establishments
			if lineSplit[2] == state and lineSplit[4] == targetSector:
				value = lineSplit[7]
				if int(value) > maxValue:
					maxValue = int(value)
				numberPerState.append({"value":value, "code":code})
				break

	#write out json result data			
	with open('./static/SectorData.json', 'w') as outfile:
	    json.dump(numberPerState, outfile)

	#return title and max value
	title = targetSector.replace("'", "`")
	tickInterval = math.floor(maxValue/3)
	return [title, maxValue, tickInterval]