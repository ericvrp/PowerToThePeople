// Code that is ron both the client and the server.

CurrentWattage = new Meteor.Collection("CurrentWattage");
Wattage        = new Meteor.Collection("Wattage");
Players        = new Meteor.Collection("Players"); //used by the d3 demo code

log = function(s) {
	console.log(s);
}