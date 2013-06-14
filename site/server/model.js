Players.allow({
	insert: function() { return true; },
	update: function() { return true; },
	remove: function() { return true; }
});

Meteor.publish('AllPlayers', function() {
	return Players.find();
});

Meteor.publish('MyCurrentWattage', function() {
	return CurrentWattage.find({userId: this.userId});
});

Meteor.publish('MyWattage', function() {
	return Wattage.find({userId: this.userId});
});

Meteor.startup(function() {
	//one time only server code goes here
    if (Players.find().count() === 0) {
      var names = ["Ada Lovelace",
                   "Grace Hopper",
                   "Marie Curie",
                   "Carl Friedrich Gauss",
                   "Nikola Tesla",
                   "Claude Shannon"];
      for (var i = 0; i < names.length; i++)
        Players.insert({name: names[i], score: Math.floor(Math.random()*10)*5});
    }
});

