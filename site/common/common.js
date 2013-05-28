// Code that is ron both the client and the server.

CurrentWattage = new Meteor.Collection("CurrentWattage");
Wattage        = new Meteor.Collection("Wattage");

log = function(s) {
	console.log(s);
}
