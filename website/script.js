function respondNav() {

  WindowWidth = $(window).width();

  if (WindowWidth <= 440) {
    $(".navbar-links").hide();
    $(".navbar ul").css("display", "block");
    $(".navbar ul").css("float", "none");
    $(".navbar ul").css("background-color", "rgb(30 32 40)");
    $(".navbar-links li").css("padding", "1rem");
    $(".navbar ul").css("transform", "translate(0, 0)");
    $(".toggle-button").show();
  } else {
    $(".navbar ul").css("display", "flex");
    $(".navbar ul").css("float", "right");
    $(".navbar-links li").css("padding", "0.5rem");
    $(".navbar").css("padding", "1rem");
    $(".GPTBot").css("padding", "0");
    $(".navbar-links li").css("border-bottom", "0");
    $(".navbar-links").css("border-top", "0");
    $(".navbar ul").css("background-color", "rgb(39 41 52)");
    $(".navbar ul").css("transform", "translate(0, -1.8rem)");
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
  $(".navbar ul li").css("display", "block");
  $(".navbar ul li").css("text-align", "right");
  $(".navbar").css("padding", "0");
  $(".navbar-links li").css("border-bottom", "2px solid #777");
  $(".navbar-links").css("border-top", "2px solid #777");
  $(".GPTBot").css("padding", "1rem");
  $(".navbar-links").slideToggle("fast");
});

var typed = new Typed(".typed", {
  strings: ["What should I do today?", "What happened on June 4, 1989?", "What is the derivative of sin(x)?", "How to bake a cake?",
    "What country has the highest life expectancy?", "How many moons does Jupiter have?", "Where is mount Everest located?",
    "Which American president is on the $5 bill?", "Tell me a bad joke.", "Give me a good workout routine.", "What is a group of pandas called?",
    "What came first, the chicken or the egg?", "What movie should I watch?", "Prove that lim(2x+3) = -3", "What is a nibble?", "What are the top 10 movies of all time?",
    "How to rotate a quaternion?", "What are the first 8 digits of pi?", "Prove the Caley Hamilton theory.", "Write a song about dogs."],
  typeSpeed: 70,
  backSpeed: 10,
  shuffle: true,
  loop: true
})



