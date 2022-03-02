
$(document).ready(function(){
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
	
    $(document).on('click', '.btn_download', function(){
        console.log($(this));
        var tbl = $(this).data('tbl');
        console.log(window.location.search)
        var sort = window.location.search;
        if (sort == ''){
            sort = "?sort=TeamNumber"
        }
        sort = sort.replace('?sort=', '')
        if(tbl){
            var data = {
                'tbl_' : tbl,
                'sort_' : sort
            }
            csv_download(data);
        }
    });



    var csv_download = function(data){
        console.log(data);
        $.ajax({
            url: $('.btn_download').data('url'),
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: data,
            cache: true,
            dataType: 'json',
            type: 'POST',
            success: function(response) {
                console.log(response)
             
                if (response.valid) {
                    fileUrl = "../static/media/" + response.url;
                    var file = new File(["aa"], fileUrl);
                    var link = document.createElement("a");
                    link.download = file.name;
                    link.href = fileUrl;
                    link.click();
                } else {
                    alert("Error saving the team data: " + response["error"]);
                }
            },
            error: function(error) {
                console.log(error)
                alert("Error saving the team data. The website has a new error or your connection is bad.");
            },
            timeout: 3000
        });
    }
});
