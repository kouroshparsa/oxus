nv.addGraph(function() {
         var chart = nv.models.pieChart();

         chart.margin({
          top: {{top_margin}},
          right: {{right_margin}},
          bottom: {{bottom_margin}},
          left: {{left_margin}}
         });

         var data = {{data}};

        chart.showLabels({{show_labels}});
        chart.donut({{is_donut}});
        chart.showLegend({{show_legend}});
        chart.donutLabelsOutside({{labels_outside}});
        {% if is_lbl_percent %}chart.labelType("percent");{% endif %}

        chart
            .x(function(d) { return d.label })
            .y(function(d) { return d.value });

         chart.width({{width}});
         chart.height({{height}});


         {% if color_category %}chart.color(d3.scale.{{color_category}}().range());{% endif %}

         var tooltips = {{tooltips}};
         chart.tooltipContent(function(key, x, y, graph) {
           if(tooltips[key] != undefined && tooltips[key][parseFloat(x)] != undefined){
             return tooltips[key][parseFloat(x)];
           }else{
             var x = String(key);
             tooltip_str = '<center><b>'+x+'</b></center>' + y.value;
             return tooltip_str;
           }
         });

         document.getElementById("{{id}}").innerHTML = '<svg style="width:{{width + left_margin + right_margin}}px;height:{{height + top_margin + bottom_margin}}px;"></svg>';

         d3.select('#{{id}} svg')
          .datum(data)
          .transition().duration(500)
          .call(chart);
});
