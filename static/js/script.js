let exercises;

// fetches data from exercises collection in MongoDB in JSON 
// format and loads to the autofill fields
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

// Dynamic field loading on create finisher function

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

// Dynamic field loading on clone finisher page

$("#edited_exercise_set_type_select_1").change(function() {
    $("#edited_exercise_2").show("slow");
});

$("#edited_exercise_set_type_select_2").change(function() {
    $("#edited_exercise_3").show("slow");
});

$("#edited_exercise_set_type_select_3").change(function() {
    $("#edited_exercise_4").show("slow");
});

$("#edited_exercise_set_type_select_4").change(function() {
    $("#edited_exercise_5").show("slow");
});

$("#edited_exercise_set_type_select_5").change(function() {
    $("#edited_exercise_6").show("slow");
});

$("#edited_exercise_set_type_select_6").change(function() {
    $("#edited_exercise_7").show("slow");
});

$("#edited_exercise_set_type_select_7").change(function() {
    $("#edited_exercise_8").show("slow");
});

$("#edited_exercise_set_type_select_8").change(function() {
    $("#edited_exercise_9").show("slow");
});

$("#edited_exercise_set_type_select_9").change(function() {
    $("#edited_exercise_10").show("slow");
});

// Dynamic field loading on modify finisher page

$("#modified_exercise_set_type_select_1").change(function() {
    $("#modified_exercise_2").show("slow");
});

$("#modified_exercise_set_type_select_2").change(function() {
    $("#modified_exercise_3").show("slow");
});

$("#modified_exercise_set_type_select_3").change(function() {
    $("#modified_exercise_4").show("slow");
});

$("#modified_exercise_set_type_select_4").change(function() {
    $("#modified_exercise_5").show("slow");
});

$("#modified_exercise_set_type_select_5").change(function() {
    $("#modified_exercise_6").show("slow");
});

$("#modified_exercise_set_type_select_6").change(function() {
    $("#modified_exercise_7").show("slow");
});

$("#modified_exercise_set_type_select_7").change(function() {
    $("#modified_exercise_8").show("slow");
});

$("#modified_exercise_set_type_select_8").change(function() {
    $("#modified_exercise_9").show("slow");
});

$("#modified_exercise_set_type_select_9").change(function() {
    $("#modified_exercise_10").show("slow");
});