$(document).ready(function() {
    var options = {
        events: calendarData,
        height: 700
    };
    console.log(options);
    $("#calendar").fullCalendar(options);
});