from matplotlib import pyplot as plt
import base64
from io import BytesIO

def getGraph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_png = buffer.getvalue()
    graph = base64.b64encode(img_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def getPlot(x, y):
    plt.switch_backend('AGG')
    #plt.figure(figsize=(10,5))
    plt.title('Average Yearly Temperature in Miami from 1900 - 2013')
    plt.ylabel('Average Temperature (Degrees Celsius)')
    plt.xlabel('Year')
    plt.scatter(x, y)
    #plt.show()
    graph = getGraph()
    return graph