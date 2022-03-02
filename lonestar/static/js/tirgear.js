
$(function() {
	updateFee();
});

function getFormValues() {
	var form = {};
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
    return form;
}


function updateFee() {
    var fee = 0;
    $(".promoitem > input[rowid]").each(function() {
    	var num = $(this).val();
    	if (num == "" || (1*num) == 0) return true;
    	fee += (1 * num * $(this).attr("dollars"));
    });
	$("#currentFee").html(fee.formatMoney(2));
    $("#currentFee").attr("fee", fee);
}

function formHasAnOrder(form) {
	var hasAnOrder = false;
	for (var i = 0; i < form.promos.length; ++i) {
		var promo = form.promos[i];
		if (promo.Num != "" && (1*promo.Num) > 0) hasAnOrder = true;
	}
	return hasAnOrder;
}


function updateOrderfn(data){
	console.log(data)
	$.ajax({
		headers: { "X-CSRFToken": csrftoken },
		url: $("[name=update_order]").data('url'),
		type: 'POST',
		data: data,
		success: function(data) {
			
			if(data['statusCode'] == 1){
				console.log('Paypal Success');
			
			}else{
				alert("Processing about payment was failed.");
			}
		},
		error: function(data) {
			false;
		}
	});
}