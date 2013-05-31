Template.raphaelgfx.created = function() {	
	var scalex = 2.0;
	var samplesPer24Hours = 24*60/5; //24 hour*60 min. per hour/5 min. per sample (=288)
	paperw = samplesPer24Hours * scalex,
	paperh = 300;
	
	paper  = Raphael(10,110, paperw,paperh);
	paper.rect(0,0, paperw,paperh).attr({"stroke-width": 1, stroke: "#FF0", stroke: 1});

	var path = "M" + paperw/2 + "," + paperh/2 + "R";
	for (var i = 0;i < samplesPer24Hours;i++) {
		path += "," + [paperw/2, paperh/2];
	}
	paperpath = paper.path(path).attr({"stroke-width": 1});
}


Template.raphaelgfx.mygraph = function() {
	//log("Get samples");
	
	var	samples = Template.content.SamplesDuring24Hours(0);
	if (samples.length === 0) {
		//log("No samples to draw a graph for yet");
		return;
	}
	
	var _24hours  = 3600 * 24 * 1000;	//in milliseconds
	var offsetx = 1,
	    offsety = -20,
	    scalex = 1.0 / _24hours * paperw;
	    scaley = 0.0;
	for (var i = 0;i < samples.length;i++) { 
		if (samples[i].kWh > scaley) {
			scaley = samples[i].kWh;
		}
	}
	scaley = 1.0 / scaley * paperh * 0.75 * Math.random();
	//log("scalex=" + scalex + " , scaley=" + scaley);

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
	
	//log("Now drawing");

    //paperpath.attr({path: dataPath(), stroke: Raphael.getColor(1)});

	var anim = Raphael.animation({path: dataPath(), stroke: Raphael.getColor(1)}, 500, "<>");
	paperpath.animate(anim);
}
