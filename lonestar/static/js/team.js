
$(function() {
	$("select[id^='pace'],select[id^='shirt'],select[id^='sock'],#teamType,#teamClass").each(function() {
		console.log($(this).attr("val"))
		$(this).val($(this).attr("val"));
	});
});

function cancelChanges() {
	window.location.assign("/team");
}
function checkvalue(val){
	if(!val){
		return '';
	}else{
		return val;
	}
}

function getFormValues() {
	var form = {};
	form.teamName = $("#teamName").val();
	form.teamSong = $("#teamSong").val();
	form.teamType = $("#teamType").val();
	form.teamClass = $("#teamClass").val();
	form.teamUntimed = $("#teamUntimed").prop("checked") == true ? 1 : 0;
	var runners = [];
	$("div.team-member").each(function() {
		var runner = {};
		var id = $(this).attr("runnerid");
		console.log(id, 'this is runner id');
		runner.recid = id;
		console.log($("#pace"+id).val())
		runner.pace = checkvalue($("#pace"+id).val());
		runner.shirt = checkvalue($("#shirt"+id).val());
		runner.sock = checkvalue($("#sock"+id).val());
		runner.phone = checkvalue($("#phone"+id).val());
		runner.email = checkvalue($("#email"+id).val());
	
		runners.push(runner);
	});
	form.runners = runners;
	return form;
}

function removeRunner(runnerid) {
	$("div.team-member[runnerid="+runnerid+"]").remove();
}
function runnerInfoJsonToStringFn(runners){
	var phones =  []; emails =  [];paces =  [];recids =  [];shirts =  [];socks = [];
	for (let i = 0; i < runners.length; i++) {
		const ele = runners[i];
		phones.push(ele.phone);
		emails.push(ele.email);
		paces.push(ele.pace);
		recids.push(ele.recid);
		shirts.push(ele.shirt);
		socks.push(ele.sock);
		
	}
		
	
	var data_ = {}

	data_['phone'] = phones.join('&#&');
	data_['email'] = emails.join('&#&');
	data_['pace'] = paces.join('&#&');
	data_['recid'] = recids.join('&#&');
	data_['shirt'] = shirts.join('&#&');
	data_['sock'] = socks.join('&#&');
	return data_;
}
function saveChanges(teambib,teamid) {
	var form = getFormValues();
	form.teamid = teamid;
	form.teambib = teambib;
	console.log(form)
	runnerinfo = runnerInfoJsonToStringFn(form.runners)
    var data = { method: "updateTeam", teamName: form.teamName, teamid: form.teamid,  teambib: form.teambib, teamClass: form.teamClass, teamType: form.teamType, teamSong: form.teamSong, teamUntimed: form.teamUntimed, r_id:runnerinfo.recid, r_pace: runnerinfo.pace, r_shirt: runnerinfo.shirt, r_sock: runnerinfo.sock, r_phone: runnerinfo.phone,r_email: runnerinfo.email };

	var csrftoken = $("[name=csrfmiddlewaretoken]").val();
	console.log($("[name=update_team]").data('url'), 'this is request url.');
	console.log(data);

	$.ajax({
		url: $("[name=update_team]").data('url'),
		headers: {
			"X-CSRFToken": csrftoken
		},
		data: data,
		cache: true,
		dataType: 'json',
		success: function(data) {
			console.log(data)
			var results = data.ret;
			if (results["success"] == true) {
				window.location.assign("/team?teambib="+teambib);
			} else {
				alert("Error saving the team data: " + results["ErrorMessage"]);
			}
		},
		error: function(error) {
			console.log(error)
			alert("Error saving the team data. The website has a new error or your connection is bad.");
		},
		timeout: 3000
	});




    // $.post("/dbapi", data
	// , function (results, textStatus, jqXHR) {
	//     if (results["success"] == true) {
	//     	window.location.assign("team?num="+teambib);
	//     } else {
	//         alert("Error saving the team data: " + results["ErrorMessage"]);
	//     }
	// }
	// , "json")
	// .fail(function () {
	//     alert("Error saving the team data. The website has a new error or your connection is bad.");
	// });
}