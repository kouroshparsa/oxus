mpld3.draw_figure("{{id}}",
{
	"axes": [{
		"xlim": {{xlim}},
		"yscale": "linear",
		"axesbg": "#EEEEEE",
		"texts": [{
			"v_baseline": "hanging",
			"h_anchor": "middle",
			"color": "#000000",
			"text": "{{xaxis}}",
			"coordinates": "axes",
			"zorder": 3,
			"alpha": 1,
			"fontsize": 12.0,
			"position": [0.5, -0.059895833333333329],
			"rotation": -0.0,
			"id": "el18376132984112"
		}, {
			"v_baseline": "auto",
			"h_anchor": "middle",
			"color": "#000000",
			"text": "{{yaxis}}",
			"coordinates": "axes",
			"zorder": 3,
			"alpha": 1,
			"fontsize": 12.0,
			"position": [-0.059979838709677422, 0.5],
			"rotation": -90.0,
			"id": "el18376133003136"
		}, {
			"v_baseline": "auto",
			"h_anchor": "middle",
			"color": "#000000",
			"text": "{{title}}",
			"coordinates": "axes",
			"zorder": 3,
			"alpha": 1,
			"fontsize": {{title_font_size}},
			"position": [0.5, 1.0144675925925926],
			"rotation": -0.0,
			"id": "el18376133065136"
		}, {
			"v_baseline": "auto",
			"h_anchor": "start",
			"color": "#FF0000",
			"text": "dataA",
			"coordinates": "axes",
			"zorder": 1000003.0,
			"alpha": 1,
			"fontsize": 14.399999999999999,
			"position": [0.11935483870967742, 0.93124999999999991],
			"rotation": -0.0,
			"id": "el18376133140432"
		}, {
			"v_baseline": "auto",
			"h_anchor": "start",
			"color": "#008000",
			"text": "dataB",
			"coordinates": "axes",
			"zorder": 1000003.0,
			"alpha": 1,
			"fontsize": 14.399999999999999,
			"position": [0.11935483870967742, 0.87135416666666654],
			"rotation": -0.0,
			"id": "el18376133149472"
		}],
		"zoomable": true,
		"images": [],
		"xdomain": {{xlim}},
		"ylim": {{ylim}},
		"sharey": [],
		"sharex": [],
		"axesbgalpha": null,
		"axes": [{
			"scale": "linear",
			"tickformat": null,
			"grid": {
				"color": "#FFFFFF",
				"alpha": 1.0,
				"dasharray": "10,0",
				"gridOn": true
			},
			"fontsize": 12.0,
			"position": "bottom",
			"nticks": 7,
			"tickvalues": null
		}, {
			"scale": "linear",
			"tickformat": null,
			"grid": {
				"color": "#FFFFFF",
				"alpha": 1.0,
				"dasharray": "10,0",
				"gridOn": true
			},
			"fontsize": 12.0,
			"position": "left",
			"nticks": 8,
			"tickvalues": null
		}],
		"lines": [{
                "color": "{{ fit_line_color }}",
                "yindex": 1,
                "coordinates": "data",
                "dasharray": "10,0",
                "zorder": 2,
                "alpha": 1,
                "xindex": 0,
                "linewidth": 1,
                "data": "linedata",
                "id": "el13160132814888"
                }],
		"markers": [],
		"id": "el18376132980864",
		"ydomain": {{ylim}},
		"collections": [
                {% for data in datasets %}
  		    {"paths": {{data.shape}},
		     "edgecolors": ["#000000"],
		     "edgewidths": [1.0],
		     "offsets": "{{data.id}}",
		     "yindex": 1,
		     "id": "tooltip_{{data.id}}",
		     "pathtransforms": [
				[11.11111111111111, 0.0, 0.0, 11.11111111111111, 0.0, 0.0]
		     ],
		     "pathcoordinates": "display",
		     "offsetcoordinates": "data",
	   	     "zorder": 1,
		     "xindex": 0,
		     "alphas": [0.3],
		     "facecolors": ["{{data.color}}"]
		    }{% if not loop.last %},{% endif %}
                 {% endfor %}
		],
		"xscale": "linear",
		"bbox": [0.125, 0.099999999999999978, 0.77500000000000002, 0.80000000000000004]
	}],
	"height": 480.0,
	"width": 640.0,
	"plugins": [{
		"type": "reset"
	}, {
		"enabled": false,
		"button": true,
		"type": "zoom"
	}, {
		"enabled": false,
		"button": true,
		"type": "boxzoom"
	},
        {% for data in datasets %}
	   {"voffset": 10,
	   "labels": {{data.tooltips}},
	   "hoffset": 0,
	   "location": "mouse",
	   "type": "tooltip",
	   "id": "tooltip_{{data.id}}"}
           {% if not loop.last %},{% endif %}
        {% endfor %}
	],
        "data": {
          {% for data in datasets %}
            "{{data.id}}": {{data.points}}
            {% if not loop.last %},{% endif %}
          {% endfor %}
          ,"linedata": {{ fit_line }}
        },
	"id": "el18376131347232"
}
);

