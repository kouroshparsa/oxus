function draw_scatter_chart(id, datum){
        nv.addGraph(function() {
         var chart = nv.models.scatterChart();

         chart.margin({
          top: 30,
          right: 60,
          bottom: 20,
          left: 60
         });

         chart.xAxis
          .tickFormat(d3.format(',.02f'));
         chart.yAxis
          .tickFormat(d3.format(',.02f'));

         chart.showLegend(true);

         chart
          .showDistX(true)
          .showDistY(true)
          .color(d3.scale.category10().range());

         d3.select('#' + id + ' svg')
          .datum(datum)
          .transition().duration(500)
          .attr('width', 800)
          .attr('height', 350)
          .call(chart);
        });
}

