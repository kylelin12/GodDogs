// Grab elements, create settings, etc.
var video = document.getElementById('video');

// Get access to the camera!
var startCam = function() {
	if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
		// Not adding `{ audio: true }` since we only want video now
		navigator.mediaDevices.getUserMedia({
			video: true
		}).then(function (stream) {
			video.src = window.URL.createObjectURL(stream);
			video.play();
		});
	}
};

startCam();

// Elements for taking the snapshot
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var video = document.getElementById('video');

// Trigger photo take
document.getElementById("snap").addEventListener("click", function () {
	context.drawImage(video, 0, 0, 640, 480);
});

var filterB = document.getElementById('filterB');

filters = {0: 'brightness(2.0)', 1: "blur(5px)", 2: "contract(200%)", 3: "grayscale(100%)", 4: "hue-rotate(90deg)", 5: "drop-shadow(16px 16px 20px red) invert(75%)", 6: ""};
filterCounter = 0;

var filterCounterUp = function() {
	if (filterCounter == 6) filterCounter = 0;
	else filterCounter = filterCounter + 1;
};

var filter = function() {
	console.log(filterCounter);
	canvas.style.filter = filters[filterCounter];
	filterCounterUp();
};

filterB.addEventListener('click', filter);

var convertCanvasToBase64 = function(){
	var image = new Image();
	image.src = canvas.toDataURL("image/jpeg");
	return image.src
}
