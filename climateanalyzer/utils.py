from matplotlib import pyplot as plt
import base64
import numpy as np
from io import BytesIO
from matplotlib.font_manager import FontProperties

def getGraph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_png = buffer.getvalue()
    graph = base64.b64encode(img_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def getScatterPlot1(x, y, location, yrBottom, yrTop):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    title = 'Average Yearly Temperature in ' + location + ' from ' + yrBottom + ' to ' + yrTop
    plt.title(title)
    plt.ylabel('Average Temperature (Degrees Celsius)')
    plt.xlabel('Year')
    i = 0
    for a in x:
        plt.scatter(x[i], y[i])
        i = i + 1
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--")
    graph = getGraph()
    return graph

def getScatterPlot2(x, y, president, location):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    title = 'Average Daily Temperature in ' + location + ' during ' + president + '\'s term'
    plt.title(title)
    plt.ylabel('Average Temperature (Degrees Celsius)')
    plt.xlabel('Date')
    plt.scatter(x, y)
    graph = getGraph()
    return graph

def getBarPlot(x, y, location, dtBottom, dtTop):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    title = 'Average Temperature in ' + location + ' by Party from ' + dtBottom + ' to ' + dtTop
    plt.title(title)
    plt.ylabel('Average Temperature (Degrees Celsius)')
    plt.xlabel('Party')
    plt.bar(x, y)
    graph = getGraph()
    return graph

def getBarPlot2(x, y, location):
    plt.switch_backend('AGG')
    plt.tight_layout()
    plt.xticks(rotation=-45)
    title = 'Average Temperature by Presidency in ' + location
    plt.title(title)
    plt.ylabel('Average Temperature (Degrees Celsius)')
    plt.xlabel('President')
    plt.bar(x, y)
    graph = getGraph()
    return graph

def getBarPlot3(x, y):
    plt.switch_backend('AGG')
    plt.tight_layout()
    plt.xticks(rotation=-45)
    title = 'Max Daily Temperature by Presidency'
    plt.title(title)
    plt.ylabel('Average Temperature (Degrees Celsius)')
    plt.xlabel('President')
    plt.bar(x, y)
    graph = getGraph()
    return graph