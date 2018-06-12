$(document).ready(function () {
	// Variables
	let width = 720,
		height = 0,
		filter = 'none',
		streaming = false;
	
	// Video element
	var video = document.getElementById('video');
	// Canvas element
	var canvas = document.getElementById('canvas');
	// Duplicate canvas element
	var canvas2 = document.getElementById('canvas2');
	// Snap photo button
	var snapB = document.getElementById('snap');
	// Filters
	var filters = document.getElementById('filters');
	// Photo reel
	var photos = document.getElementById('photos')
	// Save photo button
	var saveB = document.getElementById('saveB');

	// Camera start
	navigator.mediaDevices.getUserMedia({video: true, audio: false})
	.then(function(stream) {
		// Source link for video
		video.srcObject = stream;
		// Play
		video.play();
	})
	.catch(function(error) {
		console.log(`VIDEO STREAM ERROR: ${error}`)
	});

	video.addEventListener('canplay', function(e) {
		if (!streaming) {
			// Set dimensions
			height = video.videoHeight / (video.videoWidth / width);

			video.setAttribute('width', width);
			video.setAttribute('height', height)
			canvas.setAttribute('width', width);
			canvas.setAttribute('height', height);
			canvas2.setAttribute('width', width);
			canvas2.setAttribute('height', height);

			streaming = true;
		}
	}, false);

	snapB.addEventListener('click', function(e) {
		takePhoto();

		e.preventDefault();
	}, false);

	var takePhoto = function() {
		const context = canvas.getContext('2d');
		if (width && height) {
			// Set canvas properties
			canvas.width = width;
			canvas.height = height;

			// Draw the video onto the canvas after applying the filter
			context.filter = filter;
			context.drawImage(video, 0, 0, width, height);

			// Canvas to image
			const imgUrl = canvas.toDataURL('image/png');

			// Create img element
			const img = document.createElement('img');

			// Set img source
			img.setAttribute('src', imgUrl);

			// Append to photos
			photos.appendChild(img);
		}
	};

	filters.addEventListener('change', function(e) {
		filter = e.target.value;
		video.style.filter = filter;

		e.preventDefault();
	});

	var convertCanvasToBase64 = function () {
		var image = new Image();
		image.src = $('#canvas').toDataURL("image/jpeg");
		return image.src
	};

	var sendPicData = function () {
		$.ajax({
			url: '{{url_for("storePicData")}}',
			data: convertCanvasToBase64(),
			method: "POST"
		});
	};

});


var convertCanvasToBase64 = function () {
	var image = new Image();
	image.src = document.getElementById("canvas").toDataURL("image/jpeg");
	return image.src
};

var sendPicData = function () {
	$.ajax({
		url: '/storePicData',
		data: {'data': convertCanvasToBase64(),'targetUserArray':composeUserDict},
		method: "POST",
		success: function(data){
			console.log(data);
			console.log('picture processed');
		}
	});
};

//https://ourcodeworld.com/articles/read/380/how-to-convert-a-binary-string-into-a-readable-string-and-vice-versa-with-javascript
var binToStr = function(str){
	str = str.replace(/\s+/g,'');
	str = str.match(/.{1,8}/g).join(" ");
	var newBinary = str.split(" ");
	var binaryCode = [];
	for (i=0;i < newBinary.length;i++){
		binaryCode.push(String.fromCharCode(parseInt(newBinary[i],2)));
	}
	return binaryCode.join("");
};

var blobDat;

var recievePicData = function(){
	$.ajax({
		url:"/retrievePicData",
		method:"GET",
		success: function(data){
			console.log(data);
		}
	});
};


var composeUserDict = function(){
	checkboxList = document.getElementById("checkListOfUsers");
	arr = [];
	for (var i=0; i < checkboxList.length-1;i+=1){
		var checkBoxInput = checkboxList[i];
		if (checkBoxInput.checked == true){
			arr.push(checkboxList[i].value);
		}
	}
	return arr;
};

var sendButton = document.getElementById("sendToFriends");
sendButton.addEventListener("click",sendPicData);




