CurrentWattage = new Meteor.Collection("CurrentWattage");
Wattage        = new Meteor.Collection("Wattage");

if (Meteor.isServer) {
	Meteor.publish('MyCurrentWattage', function() {
		return CurrentWattage.find({userId: this.userId});
	});

	Meteor.publish('MyWattage', function() {
		return Wattage.find({userId: this.userId});
	});
}

if (Meteor.isClient) {
	Meteor.subscribe('MyCurrentWattage');
	Meteor.subscribe('MyWattage');
	
	Template.Power.watt = function() {
		var	currentWattage = CurrentWattage.findOne({userId: Meteor.userId()});
		if (!currentWattage)	return '';
		return new Date(currentWattage.createdAt) + " : " + currentWattage.watt;
	}

	Template.Energy.kWhLast24Hours = function() {
		var _24hoursago = new Date().getTime() - (3600 * 24 * 1000);
		var	samples = Wattage.find({userId: Meteor.userId(), createdAt: {$gte: _24hoursago}}).fetch(); //We could return only the kWh but that's for later
		var kWh = 0.0;
		for (n in samples) {
			kWh += samples[n].kWh;
		}
		return kWh.toFixed(1);
	}
	/*
    Template.map.rendered = function () {
       // our d3 code goes here
	   this.node = this.find('#video-map');
   
	   var yScale = d3.scale.linear()
	      .domain([0, 4])
	      .range([10, 60]);

	  //var xScale = d3.scale.linear()
	  //    .domain([0, self.duration])
	  //    .range([0, $(self.timelineWrapper).width()]);

	  var xScale = d3.scale.linear()
	      .domain([0, 200])
	      .range([0, 400]);

	  if (! self.drawTimeline) {
	      self.drawTimeline = Meteor.autorun(function() {

	        var subtitles = ['Eric', 'van', 'Riet', 'Paap']; //Subtitles.find().fetch(); 

	        self.captions = d3.select(self.node)
	          .select('.caption-spans')
	          .selectAll('rect')
	          .data(subtitles, function (sub) {
	            return sub._id; 
	          });

	        drawTimeline(); 

	      });
	    }
		
	    var drawTimeline = function(){

	        // Append new captions
	        drawSubs(self.captions.enter().append('rect'));

	        // Update changed captions
	        drawSubs(self.captions.transition().duration(400));

	        // Remove captions
	        self.captions
	          .exit()
	          .transition()
	          .duration(400)
	          .style('opacity', 0)
	          .remove(); 
	    }


	    // Sets the attributes of each new or changed caption
	    var drawSubs = function (caption) {
	      caption
	        .attr('data-id', function (cap) { return cap._id; })
	        .attr('class', 'timelineEvent')
	        .attr('fill', function (cap) { 

	          // Provide colour warnings if too fast rate / second
	          var rate = getRatio(cap);
	          if (rate &lt;= 2.3)
	            return '#50ddfb'; // it's good
	          else if (rate &gt; 2.3 &amp;&amp; rate &lt; 3.1)
	            return '#fbb450'; // warning
	          else
	            return '#ea8787'; // danger
	        })
	        .attr('x', function (cap) { return xScale(cap.startTime); })
	        .attr('y', function (cap) { return '-' + yScale(getRatio(cap)); })
	        .attr('width', function (cap) { 
	          return xScale(cap.endTime) - xScale(cap.startTime)
	        })
	        .attr('height', function (cap) {
	          return yScale(getRatio(cap)); 
	        });
	    };

		Template.map.destroyed = function () {
		    this.drawTimeline.stop(); 
		  };
     }*/
 }

if (Meteor.isServer) {
	Meteor.startup(function () {
		// code to run on server at startup
	});
}
