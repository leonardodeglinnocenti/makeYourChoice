// When .menu-button is tapped, make navbar visible

$(document).ready(function() {
    $(".menu-button").click(function() {
        $(".navbar").toggleClass("hide");
    });
});