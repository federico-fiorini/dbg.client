var arDrone = require('../node_modules/ar-drone');
var client  = arDrone.createClient();

const destDegree = parseFloat(process.argv[2]);
const CLOCKWISE = 0;
const COUNTERCLOCKWISE = 1;
const directionLabel = {CLOCKWISE: 'clockwise', COUNTERCLOCKWISE: 'counterClockwise'};

var getRotation = function getRotation(fromDegree, toDegree) {

	// Base case
	if (fromDegree == toDegree) return [null, 0];

	// Base case departing from degree 0
	if (fromDegree == 0) {
		if (toDegree > 0)
			return [CLOCKWISE, toDegree];
		else
			return [COUNTERCLOCKWISE, Math.abs(toDegree)];
	}

	// Current degree and destination degree have the same sign
	if (((toDegree > 0) & (fromDegree > 0)) || ((toDegree < 0) & (fromDegree < 0))) {
		var degree = Math.abs(toDegree) - Math.abs(fromDegree);
		if (toDegree > fromDegree)
			return [CLOCKWISE, degree];
		else
			return [COUNTERCLOCKWISE, degree];
	}

	// If different sign
	var through0 = Math.abs(toDegree) + Math.abs(fromDegree);
	var through180 = (180 - Math.abs(toDegree)) + (180 - Math.abs(fromDegree));

	if (through0 < through180) {
		if (fromDegree < 0)	return [CLOCKWISE, through0];
		else return [COUNTERCLOCKWISE, through0];
	} else {
		if (fromDegree > 0)	return [CLOCKWISE, through180];
		else return [COUNTERCLOCKWISE, through180];
	}	
};


var sendAway = function sendAway(navData) {
    if(navData.demo) {
    	var currDegree = navData.demo.clockwiseDegrees;
    	console.log('clockwiseDegrees:' + currDegree , new Date() / 1000);
    	var rotation = getRotation(parseFloat(currDegree), destDegree);

    	var direction = rotation[0];
    	var degrees = rotation[1];
    	var speed = 0.5 * degrees / 90;
    	console.log(direction + ' for ' + degrees + ' degrees at speed ' + speed , new Date() / 1000);

    	if (direction == CLOCKWISE) {
			console.log("Clockwise" , new Date() / 1000);
			this.clockwise(speed);
		} else {
			console.log("CounterClockwise" , new Date() / 1000);
			this.counterClockwise(speed);
		}
    }
};

// client.takeoff();
// console.log('took off');

// console.log('calculate degree' , new Date() / 1000);
// client.after(5000, function() {
// 	this.once('navdata', sendAway);
// })
// .after(2000, function() {
// 	console.log('stop and land' , new Date() / 1000);
// 	this.stop();
// 	this.land();
// })
// .after(1000, function() {
// 	console.log('exit' , new Date() / 1000);
// 	process.exit();
// });



client.after(500, function() {
	this.stop();
	this.land();
})
	.after(2000, function() {
	process.exit();
});
// client.after(1000, function() {
// 	process.exit();
// });


// client.on('navdata', function(navData) {
// 	if(navData.demo) {
// 		console.log(navData);
// 	}
// })