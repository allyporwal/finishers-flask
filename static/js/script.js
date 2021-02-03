let exercises;

// fetches data from exercises collection in MongoDB in JSON 
// format and loads to the autofill fields - attribution in 
// README

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


// Load all other Materialize components and fade Flash messages out

$(document).ready(function () {
    $('.sidenav').sidenav();
    $('select').formSelect();
    $('.tooltipped').tooltip();
    $('.tabs').tabs();
    $('#flashed-messages').fadeIn('slow', function(){
               $('#flashed-messages').delay(5000).fadeOut(); 
        });
});

// Dynamic field loading on forms

$('[id^=exercise_set_type_select_]').on('change', function() {
    $(this).parent().parent().parent().next('.exercise-row').show('slow');
})