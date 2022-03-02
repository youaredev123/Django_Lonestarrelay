
$(document).ready(function() {
     
      $('.navTrigger').on('click', function () {
            console.log("234234jlkl")
            $(this).toggleClass('active');
            console.log("Clicked menu");
            $("#mainListDiv").toggleClass("show_list");
            $("#mainListDiv").fadeIn();

      });

      $(window).scroll(function() {
      
      });
});
