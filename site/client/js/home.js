Meteor.subscribe('MyCurrentWattage');
Meteor.subscribe('MyWattage');
	
Template.Power.watt = function() {
	var	currentWattage = CurrentWattage.findOne({userId: Meteor.userId()});
	if (!currentWattage)	return '';
	return currentWattage.watt + " Watt : " + new Date(currentWattage.createdAt);
}

Template.Energy.kWhDuring24Hours = function(daysAgo) {
	var _24hours = 3600 * 24 * 1000;	//in milliseconds
	var end      = new Date().getTime() - daysAgo * _24hours;
	var begin    = end - _24hours;
	var	samples  = Wattage.find({userId: Meteor.userId(), $and: [
		{createdAt: {$gte: begin}}, 
		{createdAt: {$lt: end}}]}).fetch(); //We could return only the kWh but that's for later
	var kWh = 0.0;
	for (n in samples) {
		kWh += samples[n].kWh;
	}
	return kWh.toFixed(1);
}

Meteor.startup(function() {
	//put things like initial Session.set(key, value) here
});
