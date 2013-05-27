CurrentWattage = new Meteor.Collection("CurrentWattage");
Wattage        = new Meteor.Collection("Wattage");

if (Meteor.isClient) {
	Template.Power.watt = function() {
		var	currentWattage = CurrentWattage.findOne({userId: '<userid>'});
		if (!currentWattage)	return '';
		return new Date(currentWattage.createdAt) + " : " + currentWattage.watt;
	}

	Template.Energy.kWhLast24Hours = function() {
		var _24hoursago = new Date().getTime() - (3600 * 24 * 1000);
		var	samples = Wattage.find({userId: '<userid>', createdAt: {$gte: _24hoursago}}).fetch(); //We could return only the kWh but that's for later
		var kWh = 0.0;
		for (n in samples) {
			kWh += samples[n].kWh;
		}
		return kWh.toFixed(1);
	}
}

if (Meteor.isServer) {
	Meteor.startup(function () {
		// code to run on server at startup
	});
}
