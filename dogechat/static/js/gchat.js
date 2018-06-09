var list = []
var datalist = []
var chart = d3.select(".chart");
var bar = chart.selectAll("div");
var changeButton = document.getElementById("change");
var chartHTML = document.getElementById("remove");


function getdata(){
    $.ajax({
        url: "/getdata",
        type: "GET",
        success: function(result) {
            list = Object.keys(JSON.parse(result));
            datalist = Object.values(JSON.parse(result))
        },
    });
}

var interval = 1000; //1 secondSS
function sendMessage() {
    $.ajax({
        url: "/_receiveMessage", 
        type: "POST", 
        data: {
        'chatText': $("#chatText").val(),
        'username': $("#username").val()
        },
        success: function() {
            recvMessage(),
            $("#chatText").val('');
        }
    });
}

function recvMessage() {
    $.ajax({
        url: "/_sendMessages",
        type: "GET",
        success: function(result) {
            $("#panelBody").html(result);            
        },
        complete: function(result) {
            setTimeout(recvMessage, interval);
        }
    });
}

function getdata(){
    $.ajax({
        url: "/getdata",
        type: "GET",
        success: function(result) {
            list = Object.keys(JSON.parse(result));
            datalist = Object.values(JSON.parse(result))
            console.log(list)
            console.log(datalist)
            var chart = d3.select(".chart");
            var bar = chart.selectAll("div");
            var changeButton = document.getElementById("change");
            var chartHTML = document.getElementById("remove");
            var barUpdate = bar.data(datalist);
            var barEnter = barUpdate.enter().append("div");
            bar = chart.selectAll("div");
            barUpdate = bar.data(datalist);
            barUpdate.transition().duration(500).style("width", function(d) {return 120 + d * 50 + "px";}).style("height", "30px");
            barUpdate.text(function(d) {return d + " Messages Sent"});
            bar.data(list).append("b").attr("style","float:left").text(function(d){return d;});
        },
    });
}

$(document).ready(function() {
    $("#chatText").keypress(function(e) {
        if (e.keyCode == 13) {
            $("#send").click();
        }
    });
    $("button").click(sendMessage);
    getdata()
    setTimeout(recvMessage, interval);
});

var chart = d3.select(".chart");
var bar = chart.selectAll("div");
var changeButton = document.getElementById("change");
var chartHTML = document.getElementById("remove");
var barUpdate = bar.data(datalist);
var barEnter = barUpdate.enter().append("div");


//changeButton.addEventListener("click",change);


//generate(budget2015);