

Template.content.userId = Meteor.userId; //XXX This is kind of nonesense. We should be able to test for Meteor.userId directly in a handlebar template!

Template.content.watt = function() {
	var	currentWattage = CurrentWattage.findOne({userId: Meteor.userId()});
	if (!currentWattage)	return '';
	return currentWattage.watt + " Watt : " + new Date(currentWattage.createdAt);
}

Template.content.SamplesDuring24Hours = function(daysAgo) {
	var _24hours  = 3600 * 24 * 1000;	//in milliseconds
	var	_5minutes = 5 * 60 * 1000;
	var end       = new Date().getTime() - daysAgo * _24hours + _5minutes;
	end           = parseInt(end / _5minutes) * _5minutes;
	var begin     = end - _24hours;
	//XXX note: the following query uses different begin&end each time so no cacheing will occur. Probably better to increment begin&end is 5 minute intervals?!?
	return Wattage.find({userId: Meteor.userId(), $and: [
		{createdAt: {$gte: begin}}, 
		{createdAt: {$lt: end}}]},
		{sort: {createdAt: 1}}).fetch(); //XXX future optimization: get just the kWh 
}

Template.content.kWhDuring24Hours = function(daysAgo) {
	var	samples  = Template.content.SamplesDuring24Hours(daysAgo);
	var kWh = 0.0;
	for (n in samples) {
		kWh += samples[n].kWh;
	}
	return kWh.toFixed(1);
}

Meteor.startup(function() {
	//put things like initial Session.set(key, value) here

	Meteor.subscribe('MyCurrentWattage');
	Meteor.subscribe('MyWattage');
	//Meteor.subscribe('AllPlayers');

	Accounts.config({
		sendVerificationEmail: true //XXX untested
	});
});

