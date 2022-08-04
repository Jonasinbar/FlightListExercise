from flask import Flask, redirect, url_for, request

from main import getFlightInfoFromFlightNumber, updateFlightInCsvAndReturnIfChanged
app = Flask(__name__)

@app.route('/info/<fight_num>/<arrivalTime>/<depatureTime>/<status>')
def success(fight_num, arrivalTime, depatureTime, status):
   return 'flight N° :' + fight_num + " - depatureTime :" + depatureTime +  " - arrivalTime :" + arrivalTime + ". Status : " + status

@app.route('/FlightNotFound/')
def fail():
   return "Flight not found"

@app.route('/Update/')
def updated():
   return "Updated"

@app.route('/NotUpdate/')
def notUpdated(message=""):
   return "Row not found -" + message

@app.route('/getInfoByFlightNum',methods = ['GET'])
def getInfoByFlightNum():
   if request.method == 'GET':
      fight_num = request.args.get('fight_num')
      info = getFlightInfoFromFlightNumber(fight_num)
      if(info):
         return redirect(url_for('success',fight_num = info[0], arrivalTime = info[1], depatureTime = info[2], status = info[3]))
      else:
         return redirect(url_for('fail'))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/updateFlight',methods = ['POST'])
def updateFlight():
   if request.method == 'POST':
      flightNumber = request.form['flightNumber']
      arrivalTime = request.form['arrivalTime']
      depatureTime = request.form['depatureTime']
      status = request.form['status']
      try :
         rowChanged = updateFlightInCsvAndReturnIfChanged(flightNumber, arrivalTime, depatureTime, status)
      except Exception as e:
         return redirect(url_for('notUpdated', message=e))
      if rowChanged:
         return redirect(url_for('updated'))
      else :
         return redirect(url_for('notUpdated'))
if __name__ == '__main__':
   app.run(debug = True)