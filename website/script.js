function respondNav() {

  WindowWidth = $(window).width();

  if (WindowWidth <= 469) {
    $(".navbar-links").hide();
    $("ul").css("display", "block");
    $("ul").css("float", "none");
    $("ul").css("background-color", "rgb(30 32 40)");
    $(".navbar-links li").css("padding", "1rem");
    $("ul").css("transform", "translate(0, 0)");
    $(".toggle-button").show();
  } else {
    $("ul").css("display", "flex");
    $("ul").css("float", "right");
    $(".navbar-links li").css("padding", "0.5rem");
    $(".navbar").css("padding", "1rem");
    $(".GPTBot").css("padding", "0");
    $(".navbar-links li").css("border-bottom", "0");
    $(".navbar-links").css("border-top", "0");
    $("ul").css("background-color", "rgb(39 41 52)");
    $("ul").css("transform", "translate(0, -1.8rem)");
    $(".navbar-links").show();
    $(".toggle-button").hide();
  }
}

$(document).ready(function () {
  respondNav();
})

$(window).resize(function () {
  respondNav();
})

$(".toggle-button").click(function () {
  $("ul li").css("display", "block");
  $("ul li").css("text-align", "right");
  $(".navbar").css("padding", "0");
  $(".navbar-links li").css("border-bottom", "2px solid #777");
  $(".navbar-links").css("border-top", "2px solid #777");
  $(".GPTBot").css("padding", "1rem");
  $(".navbar-links").slideToggle("fast");
});
