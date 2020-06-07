from flask import Flask, request, make_response
import json
# import pyowm
from flask_cors import CORS, cross_origin
import requests
import datetime

app = Flask(__name__)

owmAPIKey = "ed584474f0e7387cdeaf93f323b55285"

@app.route("/weather",methods=['POST'])
@cross_origin()
def getWeather():
    req = request.get_json()
    res = processRequest(req)
    res = json.dumps(res)

    finalRes = make_response(res)
    finalRes.headers['Content-type'] = 'Application/json'
    return finalRes

def getTemperatureInCelcius(temp):
    newTemp = round((temp - 273.15), 2)
    celcius = str(newTemp)
    strCelcius = celcius + "°C"
    return strCelcius

def processRequest(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    cityName = parameters.get("geo-city")

    url = "http://api.openweathermap.org/data/2.5/weather?q=" + cityName+ "&appid=" + owmAPIKey
    response = requests.get(url)
    responseJSON = response.json()

    weather = responseJSON["weather"][0]
    main = responseJSON["main"]
    temp = main["temp"]
    feelsLike = main["feels_like"]
    humidity = str(main["humidity"])
    windSpeed = str(responseJSON["wind"]["speed"])
    timeStamp = responseJSON["sys"]["sunrise"]
    value = datetime.datetime.fromtimestamp(timeStamp)
    sunrise = value.strftime('%H:%M')
    timeStamp = responseJSON["sys"]["sunset"]
    value = datetime.datetime.fromtimestamp(timeStamp)
    sunset = value.strftime('%H:%M')

    speech = "Temperature in " + cityName + ": " + getTemperatureInCelcius(temp) + ". It feels like " + getTemperatureInCelcius(feelsLike) + ". Humidity is " + humidity + "%. Wind Speed is " + windSpeed + "km/h. Sunrise at " + sunrise + "AM. Sunset at " + sunset + "PM. Overall - " + weather["description"]

    return {
        "cityName": cityName,
        "fulfillmentText" : speech,
        "response": responseJSON
    }

if __name__ == '__main__':
    app.run(debug=True)
