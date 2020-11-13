$(document).ready(function () {
  $("select").formSelect();
});

$("#first_exercise_select").change(function() {
    $("#second_exercise").show("slow");
});

$("#second_exercise_select").change(function() {
    $("#third_exercise").show("slow");
});

$("#third_exercise_select").change(function() {
    $("#fourth_exercise").show("slow");
});
