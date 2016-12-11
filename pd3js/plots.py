import os
import operator
BASE_DIR = os.path.dirname(__file__)
from jinja2 import Environment, PackageLoader
TMP_ENV = Environment(loader=PackageLoader('pd3js', 'templates'))


def get_header(static_root='/static/'):
    return TMP_ENV.get_template('header.html').render(static=static_root)


class Plot(object):
    def __init__(self, id, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.id = id
        self.data = kwargs.get('data', [])
        self.left_margin = kwargs.get('left_margin', 60);
        self.right_margin = kwargs.get('right_margin', 60);
        self.top_margin = kwargs.get('top_margin', 30);
        self.bottom_margin = kwargs.get('bottom_margin', 30);

        self.width = kwargs.get('width', 800);
        self.height = kwargs.get('height', 350);

        self.show_legend = str(kwargs.get('show_legend', True)).lower()

    def get_script(self):
        return TMP_ENV.get_template(self.template).render(**self.__dict__)



class ScatterPlot(Plot):
    def __init__(self, *args, **kwargs):
        self.template = 'scatter_plot.js'
        super(ScatterPlot, self).__init__(*args, **kwargs)

    def add_data(self, name='category1', x=[], y=[], tooltips=[], shape='circle', size=5):
        cat_data = []
        for ind, val in enumerate(x):
            datum ={'x': val, 'y': y[ind], 'shape': shape, 'size': size}
            if len(tooltips) > ind:
                datum['tooltip'] = tooltips[ind]
            cat_data.append(datum)

        cat_data.sort(key=operator.itemgetter('x'))
        self.data.append({'values': cat_data, "key": name, "yAxis": "1"})
        self.tooltips = []
        if len(tooltips) > 0:
            if hasattr(self, 'tooltips'):
                self.tooltips = {name: {}}
            if not name in self.tooltips:
                self.tooltips[name] = {}

            tips = {}
            for val in cat_data:
                tips[str(val['x'])] = val['tooltip']
            self.tooltips[name] = tips


class PieChart(Plot):
    def __init__(self, *args, **kwargs):
        """
        id, values=[], labels=[],
        tooltips=[], is_donut=False, is_lbl_percent=False, labels_outside=True
        """
        self.template = 'pie_chart.js'

        kwargs['is_donut'] = str(kwargs.get('is_donut', False)).lower()
        kwargs['is_lbl_percent'] = str(kwargs.get('is_lbl_percent', False)).lower()
        kwargs['labels_outside'] = str(kwargs.get('labels_outside', True)).lower()
        super(PieChart, self).__init__(*args, **kwargs)

        self.data = []
        self.tooltips = []
        for ind, val in enumerate(kwargs['values']):
            datum = {'value': val, 'label': kwargs['labels'][ind]}
            self.data.append(datum)
            if 'tooltips' in kwargs and len(kwargs['tooltips']) > ind:
                self.tooltips.append(kwargs['tooltips'][ind])


class TreeChart(Plot):
    def convert_to_tree(self, data, parent='null'):
        """
        @data: either str, list, dict
        @parent: str
        recursively converts the data to the treenode data format
        """
        if isinstance(data, basestring):
            return {'name': str(data), 'parent': str(parent)}

        output = []
        if isinstance(data, list):
            if len(data) == 1:
                return self.convert_to_tree(data[0], parent)

            for val in data:
                val = self.convert_to_tree(val, parent)
                if isinstance(val, list) and len(val) == 1:
                    val = val[0]
                output.append(val)
            return output

        for key, val in data.items():
            subdata = {'name': str(key), 'parent': str(parent)}
            children = self.convert_to_tree(val, key)
            if len(children) > 0:
                subdata['children'] = children
            output.append(subdata)
        return output


    def __init__(self, *args, **kwargs):
        """
        id, values={}, add_br=True, enable_click=True, wrap_width=150 (pixels)
        """
        self.template = 'tree_chart.js'

        kwargs['add_br'] = str(kwargs.get('add_br', True)).lower()
        kwargs['enable_click'] = str(kwargs.get('enable_click', True)).lower()
        kwargs['wrap_width'] = str(kwargs.get('wrap_width', 150)).lower()
        super(TreeChart, self).__init__(*args, **kwargs)
        self.data = self.convert_to_tree(kwargs['values'])[0]
