from flask import Flask, render_template
import math

app = Flask(__name__)

def hav_diff(lat1, lon1, lat2, lon2):
    # An approximate great_circle calculation of the distance between two points...
    # Code converted from JavaScript - from here:  https://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters
    R = 6378.137  # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000 # meters
   

@app.route('/')
def main():
    points = []

    # Define our marker points to plot...
    points.append([51.0606, -1.3131])
    points.append([51.0626, -1.3147])
    points.append([51.0667, -1.3046])
    points.append([51.0647, -1.3224])
    points.append([51.0548, -1.3168])
    points.append([51.0555, -1.3111])
    points.append([51.0987, -1.3064])

    # Lastly before we plot stuff – we need to get the centre & diameter of a bounding circle...  
    # To approximate that – here we'll get the "great circle" distance between the NE & SW corners...
    maxlt = max(points, key=lambda x: x[0])[0]
    maxln = max(points, key=lambda x: x[1])[1]
    minlt = min(points, key=lambda x: x[0])[0]
    minln = min(points, key=lambda x: x[0])[1]

    lt = minlt + (maxlt-minlt)/2
    ln = minln + (maxln-minln)/2

    h_dist = hav_diff(minlt, minln, maxlt, maxln)

    return render_template('pp.html', points = points, centre_point = [lt, ln], rad = (h_dist / 2) + 250)

app.run(host="0.0.0.0")
