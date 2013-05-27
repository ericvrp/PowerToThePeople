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
}

if (Meteor.isServer) {
	Meteor.startup(function () {
		// code to run on server at startup
	});
}
