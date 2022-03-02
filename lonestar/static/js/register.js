var Masking = function () {
    return {
        initMasking: function () {
	        $("#phone").mask('(999) 999-9999', {placeholder:'X'});
        }
    };
}();
var paydata = {};


$(function() {
	$("#discountRow,#regRow").hide();
	Masking.initMasking();
	$(".songinfo").popover({
		content:'Team Name and Team Song needs to be finalized by March 5. Otherwise we choose for you.',
		placement:'right',
		trigger:'hover'
	});
	$(".typeinfo").popover({
		content:'Team Type and Classification needs to be finalized by March 5, but we will work with teams as much as we possibly can.',
		placement:'right',
		trigger:'hover'
	});
	console.log($('#isevent').val(), ' this is event info')
	if( !$('#isevent').val()){
		alert("TexasIndepandcyrealy Event is no exist.");
		window.location.href = "/";
		return;
	} 
	// updateFee();
});


$(document).ready(function(){

	
	if ( $('#is_full').val() != 'False'){
		console.log($('#is_full').val())
		alert('Team is already maxed out at 12 runners.')
	}
	$(document).on('change', "#email", function(){
		// active_Team_Runner();
		$("#paypal-button").click();
		var email = $(this).val();
		if (email != ''){
			console.log($("#checkemail").data('url'))
			email_check({ email_: email});
			
		}
		
	});
	function email_check(data){
		console.log(data)
		$.ajax({
            url: $("#checkemail").data('url'),
            headers: {
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            },
            data: data,
            cache: true,
			dataType: 'json',
			type: 'POST',
            success: function(res, status) {
			
				console.log(res);
				if(res.data!='OK'){
					alert(res.data);
					$("#email").val('')
				}
            },
            error: function(res) {
				console.warn(res)
                
            },
            timeout: 3000
		});
	
	}


});
	


function getFormValues() {
	var form = {};
	form.first = $("#firstName").val();
	form.last = $("#lastName").val();
	form.email = $("#email").val();
	form.phone = $("#phone").val();
	form.street = $("#street").val();
	form.city = $("#city").val();
	form.usstate = $("#state").val(); 
	form.zip = $("#zip").val();
	form.referredbyentity = $("#referredbyentity").val();
	form.referredbyperson = $("#referredbyperson").val();
	form.dob = $("#dob").val();
	form.tenkpace = $("#10kpace").val();
	form.gender = $("#gender").val();
	form.shirtsize = $("#shirtsize").val();
	form.socksize = $("#socksize").val();
	form.pw = $("#pw").val();

	form.joinCode = $("#teamInfo").attr("joincode");
	form.teamName = $("#teamName").val();
	form.teamSong = $("#teamSong").val();
	form.teamType = $("input[name='teamTypeOptions']:checked").val();
    form.teamClass = $("input[name='teamClassOptions']:checked").val();
    form.isUntimed = $("#isUntimed").prop("checked");
    var promos = [];
    $(".promoitem").each(function() {
    	var promo = {};
    	promo.ID = $(this).find("input[id^='promoid']").attr("rowid");
    	promo.Num = $(this).find("input[id^='promoid']").val();
    	var sizeEle = $(this).find("input[id^='promoOpts']");
    	promo.Size = sizeEle == null ? "" : sizeEle.val();
    	promos.push(promo);
    });
    form.promos = promos;
    form.hasReleased = $("#release").prop("checked");
    form.payStyle = $("input[name='payStyleOptions']:checked").val();
	form.discount = $("#discountCode").attr("appliedCode");
	
    form.fee = $("#currentFee").attr("fee");
    return form;
}


function saveAndPay() {
	var form = getFormValues();
	var formIsValid = validateForm(form);
	console.log(form, formIsValid);
	var newCode_ = $("#discountCode").val();
    var curCode_ = $("#discountCode").attr("appliedCode");
	if (formIsValid) {
		//please make promos data
		ID = [];
		Num = [];
		Size = [];

		for (const i in form.promos) {
			if (form.promos.hasOwnProperty(i)) {
				ID.push(form.promos[i].ID);
				Num.push(form.promos[i].Num)
				Size.push(form.promos[i].Size)
			}
		}
		p_ID = ID.join(',');
		p_Num = Num.join(',');
		p_Size = Size.join(',');
		
		var data = { method: "saveAndPay", 'first': form.first, 'last': form.last, 'email': form.email, 'phone': form.phone, 'discount': curCode_, 'street': form.street, 'city': form.city, 'usstate': form.usstate, 'zip': form.zip, 'dob': form.dob, 'tenkpace': form.tenkpace, 'gender': form.gender, 'pw': form.pw, 'teamName': form.teamName, 'teamSong': form.teamSong, 'teamType': form.teamType, 'teamClass': form.teamClass, 'fee':form.fee, 'hasReleased': form.hasReleased, 'payStyle': form.payStyle, 'isUntimed': form.isUntimed, 'newCode': newCode_, 'joinCode': form.joinCode, 'referredbyentity': form.referredbyentity, 'referredbyperson': form.referredbyperson, promoItemsId: p_ID, promoItemsNum :  p_Num, promoItemsSize : p_Size, shirtsize: form.shirtsize, 'socksize' : form.socksize };
		console.log(data);
		console.log($("[name=save_payurl]").data('url'))
        $.ajax({
            url: $("[name=save_payurl]").data('url'),
            headers: {
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            },
            data: data,
            cache: true,
            dataType: 'json',
            success: function(res, status) {
				console.log(res);
				var results = res.ret;
                if (results["success"] == true) {
					if (results["fee"] && results["fee"] > 0) {
						paydata['amount'] = results["fee"];
						paydata['item_number'] = results["item"];
						paydata['invoice'] =results["runnerid"];
						paydata['teamid'] = results["teamid"];
						paydata['teampay'] = results["teampay"];
						paydata['newteam'] = results["newteam"];
						paydata['orderid'] = results["orderid"];
						$("input[name=amount]").val(results["fee"]);
						$("input[name=item_number]").val(results["item"]);
						$("input[name=invoice]").val(results["runnerid"]);
						$("input[name=custom]").val(results["teamid"] + "," + results["teampay"] + "," + results["newteam"] + "," + (results["orderid"] || 0));
						$("#paypal-button").click();
					} else {
						// free entry or team paid already
						window.location.assign("/team");
						paydata = {};
					}
				} else {
					alert("Error saving the registration info: " + results["ErrorMessage"]);
					paydata = {};
				}
            },
            error: function(res) {
				console.log(res)
				paydata = {};
                alert("Error saving registration info. Please try again.");
            },
            timeout: 3000
		});

	} else {
		alert("Please fill out the required fields that have been marked in red.");
	}
}

function updateFee() {
	
    var teamClass = $("input[name='teamClassOptions']:checked").val();
    if (teamClass == null){
		 teamClass = "Open";
	}
    var payStyle = $("input[name='payStyleOptions']:checked").val();
    var newDiscountCode = $("#discountCode").val();
    var curDiscountCode = $("#discountCode").attr("appliedCode");
	var joinCode = $("#teamInfo").attr("joincode");
	var form = getFormValues();

	console.log(form);
	var ID = [];
	var Num = [];
	var Size = [];

	for (const i in form.promos) {
		if (form.promos.hasOwnProperty(i)) {
			ID.push(form.promos[i].ID);
			Num.push(form.promos[i].Num)
			Size.push(form.promos[i].Size)
		}
	}
	var p_ID = ID.join(',');
	var p_Num = Num.join(',');
	var p_Size = Size.join(',');

    var data = { method: "calcFee", teamClass: teamClass, payStyle: payStyle, newCode: newDiscountCode, curCode: curDiscountCode , promoItemsId: p_ID, promoItemsNum : p_Num, promoItemsSize: p_Size, joinCode: joinCode };
	console.log(data)
	var csrftoken = $("[name=csrfmiddlewaretoken]").val();
	var calcfeeurl = $("[name=calcfeeurl]").data('url');
	
	$.ajax({
		url: calcfeeurl,
		headers: {
			"X-CSRFToken": csrftoken
		},
		data: data,
		cache: true,
		dataType: 'json',
		type: 'POST',
		success: function(data, status) {
			console.log(data);
			var results = data.ret;
			if (results == false){
				alert("Registration for teams is currently closed.");
				window.location = '/';
				return 
			}
			if (results["success"] == true) {
				
				if (results["codeApplied"]) {
					$("#discountRow,#regRow").show();
					$("#regPrice").html((results["fee"] + results["promoCost"]).formatMoney(2));
					$("#discount").html((results["fee"] - results["newFee"]).formatMoney(2));
					$("#currentFee").html((results["newFee"] + results["promoCost"]).formatMoney(2));
					$("#currentFee").attr("fee", results["newFee"] + results["promoCost"]);
					$("#discountCode").attr("appliedCode", results["codeApplied"]);
				} else {
					$("#discountRow,#regRow").hide();
					$("#discountCode").attr("appliedCode", "");
					$("#discountCode").val('');
					$("#currentFee").html((results["fee"] + results["promoCost"]).formatMoney(2));
					$("#currentFee").attr("fee", results["fee"] + results["promoCost"]);
				}
			} else {
				if (results["ErrorMessage"] == "The fee was not found for this scenario.") {
					alert("Registration for teams is currently closed.");
				} else {
					alert("Unable to update the fee. Please try again(1).");
				}
			}
		},
		error: function(res) {
			console.log(res);
			alert("Unable to update the fee. Please try again(2).");
		},
		timeout: 3000
	});

}

function validateForm(form) {
	var valid = true;
	$(".has-error").removeClass("has-error");
	if (form.first == "") { $("#firstName").parent().addClass("has-error"); valid = false; }
	if (form.last == "") { $("#lastName").parent().addClass("has-error"); valid = false; }
	if (form.email == "") { $("#email").parent().addClass("has-error"); valid = false; }
	if (form.phone == "") { $("#email").parent().addClass("has-error"); valid = false; }
	if (form.street == "") { $("#street").parent().addClass("has-error"); valid = false; }
	if (form.city == "") { $("#city").parent().addClass("has-error"); valid = false; }
	if (form.usstate == "") { $("#state").parent().addClass("has-error"); valid = false; }
	if (form.zip == "") { $("#zip").parent().addClass("has-error"); valid = false; }
	if (form.dob == "") { $("#dob").parent().addClass("has-error"); valid = false; }
	if (form.tenkpace == "") { $("#10kpace").parent().addClass("has-error"); valid = false; }
	if (form.gender == "") { $("#gender").parent().addClass("has-error"); valid = false; }
	if (form.pw == "") { $("#pw").parent().addClass("has-error"); valid = false; }
	if (form.teamName == "") { $("#teamName").parent().addClass("has-error"); valid = false; }
    if (!form.hasReleased) { $("#release").parent().addClass("has-error"); valid = false; }
    if (form.payStyle == "") { $("input[name='payStyleOptions']:checked").parent().addClass("has-error"); valid = false; }
    return valid;
}



function active_Team_Runner(){
	var paydata = {
		amount: 50,
		item_number: 10,
		invoice: 58,
		teamid: 26,
		teampay: 0,
		newteam : 1,
		orderid: 1
	}
	console.log(paydata);

	if (paydata == {} )return;

	
	var csrftoken = $("[name=csrfmiddlewaretoken]").val();
	var active_url = $("[name=active_url]").data('url');
	console.log(active_url)
	$.ajax({
		url: active_url,
		headers: {
			"X-CSRFToken": csrftoken
		},
		data: paydata,
		cache: true,
		dataType: 'json',
		type: 'POST',
		success: function(data, status) {
			console.log(data);
			if (data.valid){
				alert('Please check mail.')
			}else{
				alert('Server Error')
			}
		
		},
		error: function(res) {
			console.log(res);
			alert('Internet error')
		},
		timeout: 3000
	});
}