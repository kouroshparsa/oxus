        nv.addGraph(function() {
         var chart = nv.models.scatterChart();

         chart.margin({
          top: {{top_margin}},
          right: {{right_margin}},
          bottom: {{bottom_margin}},
          left: {{left_margin}}
         });

         var data = {{data}};

         chart.xAxis.tickFormat(d3.format(',.02f'));
         chart.yAxis.tickFormat(d3.format(',.02f'));

         chart.showLegend({{show_legend}});
         chart.showDistX({{show_distx}});
         chart.showDistY({{show_disty}});

         {% if color_category %}chart.color(d3.scale.{{color_category}}().range());{% endif %}

         var tooltips = {{tooltips}};
         chart.tooltipContent(function(key, x, y, graph) {
           if(tooltips[key] != undefined && tooltips[key][parseFloat(x)] != undefined){
             return tooltips[key][parseFloat(x)];
           }else{
             return y;
           }
         });

         d3.select('#{{id}} svg')
          .datum(data)
          .transition().duration(500)
          .attr('width', {{width}})
          .attr('height', {{height}})
          .call(chart);
        });
