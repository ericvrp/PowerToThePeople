Template.raphaelgfx.created = function() {	
	var scalex = 2;
	var samplesPer24Hours = 24*60/5; //24 hour*60 min. per hour/5 min. per sample (=288)
	paperw = samplesPer24Hours * scalex,
	paperh = 300;
	
	paper  = Raphael(10,110, paperw,paperh);
	paper.rect(0,0, paperw,paperh).attr({fill: "#FFF", stroke: "#000", cursor: "pointer"}).mousemove(function(event){
		log("rect.mousemove x="+event.offsetX + " , y="+event.offsetY);
	});
	
	var path = "M" + paperw/2 + "," + paperh/2; //zoom-in from the middle
	kWh = [
		paper.path(path).attr({stroke: "#F00", "stroke-opacity": 1.0}),
		paper.path(path).attr({stroke: "#0F0", "stroke-opacity": 0.3, "stroke-dasharray": "-"}),
		paper.path(path).attr({stroke: "#00F", "stroke-opacity": 0.3, "stroke-dasharray": "."})
	];
	
	watt = paper.path("M0,"+(paperh+2)+"H"+paperw).attr({"stroke-width": 2, stroke: "#F00", "stroke-opacity": 0.5, "stroke-dasharray": "-."});
}


var	kWhMax = function(samples, max) {
	for (var i = 0;i < samples.length;i++) { 
		if (samples[i].kWh > max) {
			max = samples[i].kWh;
		}
	}
	return max;
}


var GraphDuring24Hours = function(samples, max) {
	if (samples.length === 0) {
		//log("No samples to draw a graph for yet");
		return;
	}
	
	var _24hours  = 3600 * 24 * 1000;	//in milliseconds
	var offsetx = 1,
	    offsety = -20,
	    scalex = 1.0 / _24hours * paperw;
	    scaley = 1.0 / max * paperh * 0.8; 

	var dataPath = function() {
	    var path = "";
	    for (var i = 0; i < samples.length; i++) {
			var x = offsetx + (samples[i].createdAt - samples[0].createdAt) * scalex;
			var y = offsety + paperh - samples[i].kWh * scaley;
			if (!i) {
	            path += "M" + [x, y] + "R";
	        }
			else {
	            path += "," + [x, y];
	        } 
	    }
		
		//log(path);
	    return path;
	}

	return Raphael.animation({path: dataPath()}, 500, "<>");
}


Template.raphaelgfx.mygraph = function() {

	//
	// Animate today,yesterday and last week
	//
	var	samples0 = Template.content.SamplesDuring24Hours(0);
	var max = kWhMax(samples0, 0);

	var	samples1 = Template.content.SamplesDuring24Hours(1);
	max = kWhMax(samples1, max);

	var	samples7 = Template.content.SamplesDuring24Hours(7);
	max = kWhMax(samples7, max);
	
	kWh[0].animate( GraphDuring24Hours(samples0, max) );
	kWh[1].animate( GraphDuring24Hours(samples1, max) );
	kWh[2].animate( GraphDuring24Hours(samples7, max) );
	
	//
	// Animate current wattage
	//
	var	currentWattage = CurrentWattage.findOne({userId: Meteor.userId()});
	if (currentWattage) {
		var y = paperh - currentWattage.watt / 4; //XXX fix this! The scale is all wrong. But it showns something, which is ok for now
		var anim = Raphael.animation({path: "M0," + y + "H" + paperw}, 500, "<>");
		watt.animate(anim);
	}
}
