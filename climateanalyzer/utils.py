from matplotlib import pyplot as plt
import base64
import numpy as np
from io import BytesIO
from matplotlib.font_manager import FontProperties
import matplotlib.patheffects as path_effects

def getGraph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    img_png = buffer.getvalue()
    graph = base64.b64encode(img_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def displayText(numCity, numCountry, numState, numPres):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    sum = numCity + numCountry + numState + numPres
    tuples = 'Tuples in City: ' + str(numCity) + '\nTuples in State: ' + str(numState) + '\nTuples in Country: ' + str(numCountry) + '\nTuples in President: ' + str(numPres) + '\nTotal: ' + str(sum)
    text = fig.text(0.5, 0.5, tuples, ha='center', va='center', size=20)
    text.set_path_effects([path_effects.Normal()])
    graph = getGraph()
    return graph

def getScatterPlot1(x, y, z, location, yrBottom, yrTop):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    title = 'Average Yearly Temperature in ' + location + ' from ' + yrBottom + ' to ' + yrTop
    plt.title(title)
    plt.ylabel('Average Temperature (Degrees Celsius)')
    plt.xlabel('Year')
    i = 0
    while i < len(x):
        start = i
        while i < len(x)-1 and z[i] == z[i+1]:
            i = i + 1
        end = i + 1
        plt.scatter(x[start:end], y[start:end], label=z[start])
        i = i + 1
    plt.legend(title='Presidents', bbox_to_anchor=(1.05, 1), loc='upper left')
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"k--")
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
    for i in range(len(x)):
        plt.bar(x[i], y[i])
    graph = getGraph()
    return graph

def getBarPlot2(x, y, location):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.xticks(rotation='vertical')
    title = 'Average Temperature by Presidency in ' + location
    plt.title(title)
    plt.ylabel('Average Temperature (Degrees Celsius)')
    plt.xlabel('President')
    plt.bar(x, y)
    graph = getGraph()
    return graph

def getBarPlot3(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.xticks(rotation='vertical')
    title = 'Max Daily Temperature by Presidency in the US'
    plt.title(title)
    plt.ylabel('Average Temperature (Degrees Celsius)')
    plt.xlabel('President')
    plt.bar(x, y)
    graph = getGraph()
    return graph