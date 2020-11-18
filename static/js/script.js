$(document).ready(function () {
    $('.sidenav').sidenav();
    $("select").formSelect();
    $('.tooltipped').tooltip();
    $('.tabs').tabs();
    $("#time_limit").prop("disabled", true);
    $("#time_limit_toggle").change(function() {
        if ($(this).prop("checked") == false) {
                $("#time_limit").prop("disabled", true);
        } else if ($(this).prop("checked") == true) {
                $("#time_limit").prop("disabled", false);
        } 
    })
});

$("#exercise_set_type_select").change(function() {
    $("#second_exercise").show("slow");
});

$("#exercise_set_type_select_2").change(function() {
    $("#third_exercise").show("slow");
});

$("#exercise_set_type_select_3").change(function() {
    $("#fourth_exercise").show("slow");
});

$("#exercise_set_type_select_4").change(function() {
    $("#fifth_exercise").show("slow");
});

$("#exercise_set_type_select_5").change(function() {
    $("#sixth_exercise").show("slow");
});

$("#exercise_set_type_select_6").change(function() {
    $("#seventh_exercise").show("slow");
});

$("#exercise_set_type_select_7").change(function() {
    $("#eighth_exercise").show("slow");
});

$("#exercise_set_type_select_8").change(function() {
    $("#ninth_exercise").show("slow");
});

$("#exercise_set_type_select_9").change(function() {
    $("#tenth_exercise").show("slow");
});