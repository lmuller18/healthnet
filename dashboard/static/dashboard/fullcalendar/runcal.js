$(document).ready(function() {
    var options = {
        defaultView: view,
        events: calendarData
    };
    if (options.events[0] != undefined){
        if (view == "agendaDay"){
            options.defaultDate = moment(options.events[0].start);
            options.scrollTime = moment(options.events[0].start).subtract(1, "hour").format("HH:MM:SS");
    }
    }
    console.log(options);
    $("#calendar").fullCalendar(options);
});