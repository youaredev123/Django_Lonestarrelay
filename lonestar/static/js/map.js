var leg = "", xch = "", map = null;
$(function() {
	leg = $("#mapshell").attr("leg");
	xch = $("#mapshell").attr("xch");

	map = new google.maps.Map(document.getElementById("coursemap"), {
		center:new google.maps.LatLng(29.604506,-96.262207),
		zoom:9,
		mapTypeId:google.maps.MapTypeId.HYBRID
	});
	var routeLayer = new google.maps.KmlLayer({
		url: 'https://www.google.com/maps/ms?msa=0&msid=208385123618179864865.0004abc20606c5a9f5000&ie=UTF8&output=kml&v=1',
		map: map
	});

	addLegAndXchLinks();
	google.maps.event.addListenerOnce(map, 'idle', function(){
	    applyNewMap(leg, xch);
	});

});

// https://www.google.com/maps/ms?msa=0&msid=208385123618179864865.0004abc20606c5a9f5000&num=200&start=33&t=p&ll=29.604506,-96.262207&spn=1.432794,2.859192&z=9&output=embed
// https://www.google.com/maps/ms?msa=0&msid=208385123618179864865.0004abc20606c5a9f5000&ie=UTF8&t=h&ll=29.612715,-97.147636&spn=0.089544,0.178356&z=13&output=embed
var leginfo = [
	{ leg: "Prologue", miles: "1.15", category: "1", diffrank: "NA", mapll: "29.502488,-97.448484", mapzoom: "17", desc: "Enjoy The Prologue With Your Team!!" },
	{ leg: "1", miles: "4.26", category: "3", diffrank: "15", mapll: "29.502889,-97.417402", mapzoom: "14", desc: "Gonzales = 100% Texas!" },
	{ leg: "2", miles: "5.15", category: "3", diffrank: "17", mapll: "29.485482,-97.348309", mapzoom: "14", desc: "Onward to Houston! Only 170 miles to go!" },
	{ leg: "3", miles: "4.86", category: "3", diffrank: "18", mapll: "29.488994,-97.278786", mapzoom: "14", desc: "Dirt!" },
	{ leg: "4", miles: "4.08", category: "2", diffrank: "26", mapll: "29.4766966,-97.256865", mapzoom: "14", desc: "More Dirt!" },
	{ leg: "5", miles: "3.92", category: "1", diffrank: "33", mapll: "29.446745,-97.193073", mapzoom: "14", desc: "Shiner!" },
	{ leg: "6", miles: "4.10", category: "2", diffrank: "27", mapll: "29.462528,-97.183438", mapzoom: "13", desc: "Carboloaded" },
	{ leg: "7", miles: "3.71", category: "1", diffrank: "31", mapll: "29.496989,-97.187990", mapzoom: "13", desc: "Curvy Countryside Backroads!" },
	{ leg: "8", miles: "5.18", category: "3", diffrank: "16", mapll: "29.5627,-97.18437", mapzoom: "13", desc: "Old Moulton!" },
	{ leg: "9", miles: "4.68", category: "2", diffrank: "21", mapll: "29.6151,-97.15227", mapzoom: "13", desc: "Running in 3 Counties!" },
	{ leg: "10", miles: "3.97", category: "1", diffrank: "32", mapll: "29.66195,-97.11725", mapzoom: "13", desc: "Back to civilization – Fantastic Flatonia!" },
	{ leg: "11", miles: "4.31", category: "2", diffrank: "23", mapll: "29.68492,-97.05116", mapzoom: "13", desc: "Paying Penance to St. Mary's in Praha!" },
	{ leg: "12", miles: "5.80", category: "3", diffrank: "13", mapll: "29.68387,-96.96052", mapzoom: "13", desc: "Classic Country Roads!" },
	{ leg: "13", miles: "6.38", category: "4", diffrank: "5", mapll: "29.68775,-96.87469", mapzoom: "14", desc: "Schurely Schulenburg!" },
	{ leg: "14", miles: "3.83", category: "1", diffrank: "29", mapll: "29.70025,-96.8096", mapzoom: "13", desc: "At a crossroads!" },
	{ leg: "15", miles: "4.22", category: "1", diffrank: "30", mapll: "29.69729,-96.7365", mapzoom: "13", desc: "Jammin' Weimar" },
	{ leg: "16", miles: "4.69", category: "2", diffrank: "25", mapll: "29.69297,-96.66183", mapzoom: "13", desc: "Borden! Not boredom" },
	{ leg: "17", miles: "7.11", category: "4", diffrank: "1", mapll: "29.69804,-96.57377", mapzoom: "14", desc: "Near where the Texian Army camped on the way to San Jacinto!!" },
	{ leg: "18", miles: "4.35", category: "1", diffrank: "28", mapll: "29.66597,-96.52896", mapzoom: "13", desc: "Through C-bus to Snappy's" },
	{ leg: "19", miles: "3.70", category: "1", diffrank: "34", mapll: "29.60674,-96.49068", mapzoom: "13", desc: "Columbus airport!" },
	{ leg: "20", miles: "6.82", category: "4", diffrank: "3", mapll: "29.58405,-96.40811", mapzoom: "13", desc: "Lit Silo!" },
	{ leg: "21", miles: "6.82", category: "4", diffrank: "7", mapll: "29.58913,-96.33808", mapzoom: "14", desc: "Over The Bridge!" },
	{ leg: "22", miles: "2.84", category: "1", diffrank: "35", mapll: "29.59764,-96.2598", mapzoom: "13", desc: "Through Eagle Lake!" },
	{ leg: "23", miles: "6.52", category: "4", diffrank: "8", mapll: "29.62017,-96.16401", mapzoom: "13", desc: "Giant Grain Elevator!" },
	{ leg: "24", miles: "5.05", category: "2", diffrank: "19", mapll: "29.62838,-96.09191", mapzoom: "14", desc: "Starry Night!" },
	{ leg: "25", miles: "6.09", category: "3", diffrank: "11", mapll: "29.61883,-96.01896", mapzoom: "13", desc: "Saturday Detention in Wallis!" },
	{ leg: "26", miles: "6.40", category: "4", diffrank: "6", mapll: "29.64763,-95.9745", mapzoom: "13", desc: "Over the might Brazos!" },
	{ leg: "27", miles: "2.77", category: "1", diffrank: "36", mapll: "29.68507,-95.9357", mapzoom: "14", desc: "Simonton!" },
	{ leg: "28", miles: "5.02", category: "2", diffrank: "20", mapll: "29.69849,-95.87253", mapzoom: "14", desc: "Fulshear, not Half!" },
	{ leg: "29", miles: "6.10", category: "3", diffrank: "10", mapll: "29.704,-95.83185", mapzoom: "15", desc: "3AM Suburbia" },
	{ leg: "30", miles: "4.82", category: "2", diffrank: "24", mapll: "29.71683,-95.78636", mapzoom: "14", desc: "Good Times Running Co!" },
	{ leg: "31", miles: "5.32", category: "3", diffrank: "14", mapll: "29.73844,-95.72456", mapzoom: "14", desc: "George Bush Park!" },
	{ leg: "32", miles: "6.79", category: "4", diffrank: "4", mapll: "29.7599,-95.66688", mapzoom: "13", desc: "North, East, South" },
	{ leg: "33", miles: "6.61", category: "4", diffrank: "2", mapll: "29.76348,-95.60405", mapzoom: "14", desc: "Terry Hershey’s Kiss!" },
	{ leg: "34", miles: "4.85", category: "2", diffrank: "22", mapll: "29.75111,-95.53092", mapzoom: "14", desc: "Briar Forest!" },
	{ leg: "35", miles: "5.31", category: "3", diffrank: "12", mapll: "29.76303,-95.46501", mapzoom: "14", desc: "Great Uptown to Memorial Park!" },
	{ leg: "36", miles: "5.80", category: "4", diffrank: "9", mapll: "29.76586,-95.3984", mapzoom: "14", desc: "Finishing in H-town!" },
	{ leg: "Epilogue", miles: "0.05", category: "1", diffrank: "NA", mapll: "29.75414,-95.36644", mapzoom: "16", desc: "Finish it out with your team!" }
];

var xchinfo = [
	{ xch: "End of Prologue", ll: "29.503619, – 97.444307", mapll: "29.503638,-97.44398", mapzoom: "19" },
	{ xch: "1", ll: "29.497892, -97.382637", mapll: "29.497787,-97.382686", mapzoom: "20" },
	{ xch: "2", ll: "29.475565, -97.307766", mapll: "29.473901,-97.307689", mapzoom: "17" },
	{ xch: "3", ll: "29.48651, -97.26951", mapll: "29.48651,-97.26951", mapzoom: "18" },
	{ xch: "4", ll: "29.46001, -97.22472", mapll: "29.46001,-97.22472", mapzoom: "17" },
	{ xch: "5", ll: "29.4309, -97.17125", mapll: "29.4309,-97.17125", mapzoom: "18" },
	{ xch: "6", ll: "29.48384, -97.19054", mapll: "29.48384,-97.19054", mapzoom: "17" },
	{ xch: "7", ll: "29.52661, -97.18093", mapll: "29.52661,-97.18093", mapzoom: "18" },
	{ xch: "8", ll: "29.58766, -97.17649", mapll: "29.58766,-97.17649", mapzoom: "19" },
	{ xch: "9", ll: "29.63681, -97.13134", mapll: "29.63681,-97.13134", mapzoom: "17" },
	{ xch: "10", ll: "29.68678, -97.10769", mapll: "29.68678,-97.10769", mapzoom: "17" },
	{ xch: "11", ll: "29.68123, -97.00882", mapll: "29.68123,-97.00882", mapzoom: "16" },
	{ xch: "12", ll: "29.67989, -96.90602", mapll: "29.67989,-96.90602", mapzoom: "18" },
	{ xch: "13", ll: "29.69486, -96.84726", mapll: "29.69486,-96.84726", mapzoom: "18" },
	{ xch: "14", ll: "29.70268, -96.77935", mapll: "29.70268,-96.77935", mapzoom: "18" },
	{ xch: "15", ll: "29.69167, -96.70377", mapll: "29.69167,-96.70377", mapzoom: "18" },
	{ xch: "16", ll: "29.69587, -96.62506", mapll: "29.69587,-96.62506", mapzoom: "18" },
	{ xch: "17", ll: "29.68857, -96.53731", mapll: "29.68857,-96.53731", mapzoom: "18" },
	{ xch: "18", ll: "29.64191, -96.51493", mapll: "29.64191,-96.51493", mapzoom: "17" },
	{ xch: "19", ll: "29.57093, -96.45568", mapll: "29.57093,-96.45568", mapzoom: "18" },
	{ xch: "20", ll: "29.58855, -96.37000", mapll: "29.58855,-96.37000", mapzoom: "18" },
	{ xch: "21", ll: "29.58996, -96.31378", mapll: "29.58996,-96.31378", mapzoom: "18" },
	{ xch: "22", ll: "29.61002, -96.20767", mapll: "29.61002,-96.20767", mapzoom: "18" },
	{ xch: "23", ll: "29.62724, -96.12733", mapll: "29.62724,-96.12733", mapzoom: "19" },
	{ xch: "24", ll: "29.63058, -96.06293", mapll: "29.63058,-96.06293", mapzoom: "18" },
	{ xch: "25", ll: "29.61009, -95.97019", mapll: "29.61009,-95.97019", mapzoom: "17" },
	{ xch: "26", ll: "29.67947, -95.97707", mapll: "29.67947,-95.97707", mapzoom: "18" },
	{ xch: "27", ll: "29.69014, -95.89984", mapll: "29.69014,-95.89984", mapzoom: "18" },
	{ xch: "28", ll: "29.70633, -95.84969", mapll: "29.70633,-95.84969", mapzoom: "18" },
	{ xch: "29", ll: "29.70237, -95.81463", mapll: "29.70237,-95.81463", mapzoom: "19" },
	{ xch: "30", ll: "29.73472, -95.76310", mapll: "29.73472,-95.76310", mapzoom: "19" },
	{ xch: "31", ll: "29.73507, -95.68706", mapll: "29.73507,-95.68706", mapzoom: "18" },
	{ xch: "32", ll: "29.76899, -95.64238", mapll: "29.76899,-95.64238", mapzoom: "17" },
	{ xch: "33", ll: "29.74808, -95.57223", mapll: "29.74808,-95.57223", mapzoom: "17" },
	{ xch: "34", ll: "29.75019, -95.49745", mapll: "29.75019,-95.49745", mapzoom: "18" },
	{ xch: "35", ll: "29.77626, -95.43390", mapll: "29.77626,-95.43390", mapzoom: "17" },
	{ xch: "Finish!", ll: "29.75414, -95.36644", mapll: "29.75414,-95.36644", mapzoom: "17" }
];

function addLegAndXchLinks() {
	var html = "";
	for (var i = 0; i < leginfo.length; ++i) {
		html += ((i == 0 ? "" : "&nbsp;&nbsp;") + '<a href="javascript:applyNewMap(' + i + ','+' '+');">' + leginfo[i].leg + '</a>');
	}
	$("#leglinkshell").html(html);
	html = "";
	for (var i = 0; i < xchinfo.length; ++i) {
		var pos = i -1;
		html += ((i == 0 ? "" : "&nbsp;&nbsp;") + '<a href="javascript:applyNewMap('+"''," + pos + ');">' + xchinfo[i].xch + '</a>');
	}
	$("#xchlinkshell").html(html);
}

function applyNewMap(leg, xch) {
	// map title
	var extra = "";
	if (leg != "") extra = " - " + (isNaN(leginfo[leg].leg) ? "" : "Leg ") + leginfo[leg].leg;
	else if (xch != "") extra = " - " + (isNaN(xchinfo[xch].xch) ? "" : "Exchange ") + xchinfo[xch].xch;
	$("#maptitle").html("Interactive Course Map" + extra);

	// detail description
	var desc = "~200 Glorious Miles!";
	if (leg != "") desc = leginfo[leg].desc;
	else if (xch != "") desc = (isNaN(xchinfo[xch].xch) ? "" : "Exchange ") + xchinfo[xch].xch + " Location: " + xchinfo[xch].ll;
	$("#mapdetail").html(desc);

	// leg details
	if (leg == "") $("#legdetls").hide();
	else {
		$("#legdetls").show();
		$("#mileage").html(""+leginfo[leg].miles+" Miles");
		$("#category").html("Category " + leginfo[leg].category);
		$("#diffrank").html("Difficulty Ranking: " + leginfo[leg].diffrank + " of 40");
	}

	// display profile
	
	if (leg == "") $("#profileshell").hide();
	else {
		$("#profileshell").show()
		.html("<img src='/static/images/TIRElevationProfiles/ElevationProfile-TIRLeg"+leginfo[leg].leg+".jpg' style='width:1040px;'/>");
	}

	// map center and zoom info
	var latlng = "29.604506,-96.262207";
	if (leg != "") latlng = leginfo[leg].mapll;
	else if (xch != "") latlng = xchinfo[xch].mapll;
	var ll = latlng.split(",");
	map.panTo(new google.maps.LatLng(ll[0], ll[1]));

	var curZoom = map.getZoom(), newZoom = 9;
	if (leg != "") newZoom = 1 * leginfo[leg].mapzoom;
	else if (xch != "") newZoom = 1 * xchinfo[xch].mapzoom;
	if (curZoom != newZoom) map.setZoom(newZoom);
}
