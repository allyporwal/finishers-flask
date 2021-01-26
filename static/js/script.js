let exercises;

fetch('/autofill')
  .then(response => response.json())
  .then(data => exercises = data)
  .then(function () {
        let exerciseObject = Object.assign({}, ...exercises);
        $(document).ready(function () {
            $('input.autocomplete').autocomplete({
            data: exerciseObject,
            });
        });
    })


$(document).ready(function () {
    $('.sidenav').sidenav();
    $("select").formSelect();
    $('.tooltipped').tooltip();
    $('.tabs').tabs();
});

$("#exercise_set_type_select_1").change(function() {
    $("#exercise_2").show("slow");
});

$("#exercise_set_type_select_2").change(function() {
    $("#exercise_3").show("slow");
});

$("#exercise_set_type_select_3").change(function() {
    $("#exercise_4").show("slow");
});

$("#exercise_set_type_select_4").change(function() {
    $("#exercise_5").show("slow");
});

$("#exercise_set_type_select_5").change(function() {
    $("#exercise_6").show("slow");
});

$("#exercise_set_type_select_6").change(function() {
    $("#exercise_7").show("slow");
});

$("#exercise_set_type_select_7").change(function() {
    $("#exercise_8").show("slow");
});

$("#exercise_set_type_select_8").change(function() {
    $("#exercise_9").show("slow");
});

$("#exercise_set_type_select_9").change(function() {
    $("#exercise_10").show("slow");
});