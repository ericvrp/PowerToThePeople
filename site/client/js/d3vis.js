Template.d3vis.created = function() {
	// Defer to make sure we manipulate DOM
	_.defer(function() {
		// Use this as a global variable 
		window.d3vis = {}
		Deps.autorun(function() {

			// On first run, set up the visualiation
			if (Deps.currentComputation.firstRun) {
				window.d3vis.margin = {
					top: 20,
					right: 5,
					bottom: 5,
					left: 5
				},
				window.d3vis.width = 600 - window.d3vis.margin.left - window.d3vis.margin.right,
				window.d3vis.height = 120 - window.d3vis.margin.top - window.d3vis.margin.bottom;

				window.d3vis.x = d3.scale.ordinal()
					.rangeRoundBands([0, window.d3vis.width], .1);

				window.d3vis.y = d3.scale.linear()
					.range([window.d3vis.height - 2, 0]);

				window.d3vis.color = d3.scale.category10();

				window.d3vis.svg = d3.select('#d3vis')
					.attr("width", window.d3vis.width + window.d3vis.margin.left + window.d3vis.margin.right)
					.attr("height", window.d3vis.height + window.d3vis.margin.top + window.d3vis.margin.bottom)
					.append("g")
					.attr("class", "wrapper")
					.attr("transform", "translate(" + window.d3vis.margin.left + "," + window.d3vis.margin.top + ")");
			}

			samples = Template.content.SamplesDuring24Hours(0);
			if (samples.length === 0){
				//log("no samples yet");
				return;
			}
			for (var i = 0;i < samples.length;i++)	{
				samples[i].i = i;
			}
			//log(samples.map(function(d) { return d.kWh; }));
			
	        //window.d3vis.color.domain(samples.map(function(d) { return d.kWh}));
			window.d3vis.x.domain([0, i]); //samples.map(function(d) { return d.kWh; }));
			window.d3vis.y.domain([0, d3.max(samples, function(d) { return d.kWh; })]);
			
			//log(samples.length);
			//var q = samples[0].kWh;
			//log(q);
			var bar_selector = window.d3vis.svg.selectAll(".bar")
				.data(samples, function(d) { return d.kWh; })
				.enter()
				.append("rect")
				.attr("class", "bar")
			bar_selector.transition()
				.duration(1000)
				.attr("x", function(d) { return d.i; return window.d3vis.x(d.kWh); })
				.attr("y", function(d) { return window.d3vis.y(d.kWh); })
				.attr("width", 1) //window.d3vis.x.rangeBand())
				.attr("height", function(d) { return window.d3vis.height - window.d3vis.y(d.kWh); })
				//.style("fill", function(d) { return window.d3vis.color(0); //d.kWh); })
		});
	});
}
