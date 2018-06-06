$(document).ready(function () {
    var getJSONUrl = function (url) {
        var resp;
        var xmlHttp;

        resp = '';
        xmlHttp = new XMLHttpRequest();

        if (xmlHttp != null) {
            xmlHttp.open('GET', url, false);
            xmlHttp.send(null);
            resp = xmlHttp.responseText;
        }
        return resp;
    };

    var randomDogJson = JSON.parse(getJSONUrl("https://dog.ceo/api/breeds/image/random"))["message"];

    console.log(randomDogJson);

    $('#profile-img').attr('src', randomDogJson);
});