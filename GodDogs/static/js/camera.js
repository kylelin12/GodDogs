$(document).ready(function () {
	// Grab elements, create settings, etc.
	var video = document.getElementById('video');

	// Get access to the camera!
	var startCam = function () {
		if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
			// Not adding `{ audio: true }` since we only want video now
			navigator.mediaDevices.getUserMedia({
				video: true
			}).then(function (stream) {
				video.srcObject = stream
				video.play();
			});
		}
	};

	startCam();

	$("#canvas").addClass("hidden");
	$("#canvas-cpy").addClass("hidden");
	$("#filterB").prop("disabled", true);
	$("#resetFB").prop("disabled", true);
	$("#snapAgain").prop("disabled", true);
	$("#saveB").prop("disabled", true);

	// Function to snap
	var snap = function () {
		$("#canvas").removeClass("hidden");
		$("#video").addClass("hidden");
		$("#canvas")[0].getContext('2d').drawImage(video, 0, 0, 640, 480);
		resetFilter();
		$(this).prop("disabled", true);
		$("#snapAgain").prop("disabled", false);
		$("#filterB").prop("disabled", false);
		$("#saveB").prop("disabled", false);
	};

	// Trigger photo take
	$("#snap").click(snap);

	var filters = {
		0: 'brightness(2.0)',
		1: "blur(5px)",
		2: "contrast(200%)",
		3: "grayscale(100%)",
		4: "hue-rotate(90deg)",
		5: "drop-shadow(16px 16px 20px red) invert(75%)",
		6: ""
	};
	filterCounter = 0;

	var filterCounterUp = function () {
		if (filterCounter == 6) filterCounter = 0;
		else filterCounter = filterCounter + 1;
	};

	var resetFilter = function () {
		$('#canvas-cpy')[0].getContext('2d').drawImage(document.getElementById("canvas"), 0, 0);
		$('#canvas-cpy').css('filter', '');
	};

	var filterReset = function () {
		resetFilter();
		$("#resetFB").prop("disabled", true);
	};

	var filter = function () {
		console.log(filterCounter);
		$('#canvas-cpy').removeClass('hidden');
		$("#resetFB").prop("disabled", false);
		resetFilter();
		$('#canvas').addClass('hidden');
		$('#canvas-cpy').css('filter', filters[filterCounter]);
		filterCounterUp();
	};

	$("#resetFB").click(filterReset);
	$("#filterB").click(filter);

	// Take another photo

	var snapAnother = function () {
		$("#snap").prop("disabled", false);
		$("#filterB").prop("disabled", true);
		$("#saveB").prop("disabled", true);
		$(this).prop("disabled", true);
		$("#video").removeClass("hidden");
		$("#canvas").addClass("hidden");
		$('#canvas-cpy').addClass('hidden');
	};

	$("#snapAgain").click(snapAnother);

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
		image.src = document.getElementById("canvas-cpy").toDataURL("image/jpeg");
		return image.src
	};

	var sendPicData = function () {
		$.ajax({
			url: '/storePicData',
			data: {'data': convertCanvasToBase64()},
			method: "POST",
			success: function(data){
				console.log(data);
				console.log('picture processed');
			}
		});
	};	


