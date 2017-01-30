import sys
import os
BASE_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) )
sys.path.append(BASE_DIR)
from oxus.plots import *
import random
import string

def make_plots(output_path):
    SIZE = 20
    xdata = range(SIZE)
    ydata = [i * random.randint(1, 10) for i in range(SIZE)]
    ydata2 = [x * 2 for x in ydata]

    plt1 = ScatterPlot('plot1')
    plt1.add_data(name="data1", y=ydata, x=xdata, shape='circle')

    tooltips = []
    for i in range(SIZE):
        tt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        tooltips.append(tt)
    plt1.add_data(name="data2", y=ydata2, x=xdata, shape='cross', tooltips=tooltips, size=20)

    values = [2, 3, 5]
    labels = ['apple', 'orange', 'banana']
    plt2 = PieChart('plot2', values=values, labels=labels, is_donut=True, is_lbl_percent=True, labels_outside=True)

    values = {'food': {'fruits': ['apple', 'orange', 'banana'], 'vegetables': ['mint', 'asparagus', 'eggplant', 'avocado', 'braccoli']}}
    plt3 = TreeChart('plot3', values=values)

    plt4 = CorrelationPlot("plot4", title='Correlation', xaxis='Expected', yaxis='Actual')
    plt4.add_data('set1', exp=[1,2,3], act=[1.3,2,3.5], tooltips=['A', 'B', 'C'], color='red')
    plt4.add_data('set1', exp=[1,2,3], act=[1,2.2,2.6], tooltips=['alpha', 'beta', 'gamma'], color='green')

    make_html([plt1, plt2, plt3, plt4], output_path)


make_plots('demo.html')
