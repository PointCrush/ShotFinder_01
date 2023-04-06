// Загрузка списка событий
$.ajax({
    url: '/api/events/',
    type: 'GET',
    success: function(events) {
        // Добавление событий в календарь
        $('#calendar').fullCalendar('addEventSource', events);
    }
});

// Сохранение нового события
$('#add-event-form').submit(function(event) {
    event.preventDefault();
    var title = $('#title').val();
    var start_date = $('#start-date').val();
    var end_date = $('#end-date').val();
    $.ajax({
        url: '/api/add_event/',
        type: 'POST',
        data: {
            title: title,
            start_date: start_date,
            end_date: end_date
        },
        success: function(event) {
            // Добавление нового события в календарь
            $('#calendar').fullCalendar('renderEvent', event);
            $('#add-event-modal').modal('hide');
        }
    });
});

// Сохранение новой заметки
$('#add-note-form').submit(function(event) {
    event.preventDefault();
    var text = $('#text').val();
    var event_id = $('#event-id').val();
    $.ajax({
        url: '/api/add_note/' + event_id + '/',
        type: 'POST',
        data: {
            text: text
        },
        success: function(note) {
            // Обновление заметок в календаре
            var event = $('#calendar').fullCalendar('clientEvents', event_id)[0];
            event.notes.push(note);
            $('#calendar').fullCalendar('updateEvent', event);
            $('#add-note-modal').modal('hide');
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/api/events/',
        editable: true,
        selectable: true,
        select: function(info) {
            var date = info.startStr;
            // Здесь вы можете добавить свой код для отображения формы добавления события или заметки
        }
    });

    calendar.render();
});
