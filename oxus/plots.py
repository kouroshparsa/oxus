import os
import operator
import numpy as np
BASE_DIR = os.path.dirname(__file__)
from jinja2 import Environment, PackageLoader
TMP_ENV = Environment(loader=PackageLoader('oxus', 'templates'))
import codecs

def get_header(static_root='/static/', embed=False):
    params = {'static': static_root}
    css_files = ['nv.d3.min', 'node_tree']
    if embed:
        css = ''
        for filename in css_files:
            path = '{}/static/oxus/css/{}.css'.format(BASE_DIR, filename)
            css = '{} {}'.format(css, open(path, 'r').read())
        params['css'] = css
    else:
        params['css_files'] = css_files

    js_files = ['common', 'd3.min', 'nv.d3.min', 'tree_node', 'mpld3.v0.2']
    if embed:
        js = ''
        for filename in js_files:
            path = '{}/static/oxus/js/{}.js'.format(BASE_DIR, filename)
            js = u'{} {}'.format(js, codecs.open(path, 'rb', 'utf-8').read())
        params['javascript'] = js
    else:
        params['js_files'] = js_files

    return TMP_ENV.get_template('header.html').render(**params)


def make_html(plots, output_path):
    """
    generates an html
    @plots: list of Plot objects
    @output_path: str
    """
    page_data = {'plot_header': get_header(embed=True)}

    for plt in plots:
        plt.script = plt.get_script()

    page_data['plots'] = plots
    html = TMP_ENV.get_template('basic.html').render(page_data)
    with codecs.open(output_path, 'wb', 'utf-8') as out:
        out.write(html)


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

    def add_data(self, name='category1', x=[], y=[], tooltips=[], shape='circle', size=10):
        cat_data = []
        for ind, val in enumerate(x):
            datum ={'x': val, 'y': y[ind], 'shape': shape, 'size': str(size)}
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


class CorrelationPlot(Plot):
    SHAPES = {'circle': [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]]
    }

    def __init__(self, *args, **kwargs):
        self.template = 'correlation_plot.js'
        kwargs['title'] = kwargs.get('title', '')
        kwargs['title_font_size'] = kwargs.get('title_font_size', 20)
        kwargs['datasets'] = []
        kwargs['fit_line_color'] = kwargs.get('fit_line_color', 'blue')
        super(CorrelationPlot, self).__init__(*args, **kwargs)

    def add_data(self, name, exp=[], act=[], tooltips=[], shape='circle', size=10, color='green'):
        data = {'id': 'data00{}'.format(len(self.datasets)),\
               'shape': CorrelationPlot.SHAPES[shape], 'exp': exp, 'act': act,\
               'points': [list(val) for val in zip(exp, act)],\
               'tooltips': tooltips, 'size': size, 'color': color}
        self.datasets.append(data)

    def get_correlation():
        exp = []
        act = []
        for val in self.datasets:
            exp = exp + val['exp']
            act = act + val['act']
        return np.corrcoef(act, exp)[0][1]

    def get_script(self):
        if len(self.datasets) < 1:
            raise Exception('Please add data sets using the add_data method.')
        self.xlim = [min(min(data['exp']) for data in self.datasets),\
                     max(max(data['exp']) for data in self.datasets)]
        self.ylim = [min(min(data['act']) for data in self.datasets),\
                     max(max(data['act']) for data in self.datasets)]
        deltax = self.xlim[1] - self.xlim[0]
        deltay = self.ylim[1] - self.ylim[0]
        self.xlim = [0.4 * deltax - self.xlim[0], 0.4 * deltax + self.xlim[1]]
        self.ylim = [0.4 * deltay - self.ylim[0], 0.4 * deltay + self.ylim[1]]
        exp = []
        act = []
        for val in self.datasets:
            exp = exp + val['exp']
            act = act + val['act']
        
        pt1 = np.unique(exp)
        pt2 = np.poly1d(np.polyfit(exp, act, 1))(pt1)
        self.fit_line = [[pt1[0], pt2[0]], [pt1[-1], pt2[-1]]]
        return super(CorrelationPlot, self).get_script()

