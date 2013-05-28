Meteor.publish('MyCurrentWattage', function() {
	return CurrentWattage.find({userId: this.userId});
});

Meteor.publish('MyWattage', function() {
	return Wattage.find({userId: this.userId});
});
