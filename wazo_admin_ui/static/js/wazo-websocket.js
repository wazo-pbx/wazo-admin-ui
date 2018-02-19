let socket = null;
let started = false;
let events_subscribe_callback = {};

function _start() {
  let msg = {
    op: 'start'
  };
  socket.send(JSON.stringify(msg));
}

function _subscribe(event_name) {
  let msg = {
    op: 'subscribe',
    data: {
      event_name: event_name
    }
  };
  socket.send(JSON.stringify(msg));
}

function event_subscriber_callback(event_name, callback) {
  events_subscribe_callback[event_name] = callback;
}

function connect(token) {
  if (socket != null) {
    console.log('socket already connected');
    return;
  }

  socket = new WebSocket('wss://' + window.location.host + '/api/websocketd/?token=' + token);

  socket.onmessage = function(event) {
    let payload = JSON.parse(event.data);

    if (!started) {
      switch (payload.op) {
        case 'init':
          for (event_name in events_subscribe_callback) {
            _subscribe(event_name);
          }
          _start();
          break;
        case 'start':
          started = true;
          console.log('waiting for messages');
          break;
      }
    }
    else {
      for (event_name in events_subscribe_callback) {
        let func_callback = events_subscribe_callback[event_name];
        if (payload.name == event_name) {
          window[func_callback](payload);
        }
      }
    }
  };

  socket.onclose = function(event) {
    socket = null;
    console.log('websocketd closed with code ' + event.code + ' and reason "' + event.reason + '"');
  };
}

function task_listener(payload) {
  let label_info = $('.task-event-infos .label-info');
  let sub_label_info = $('.task-event-infos #sub-label-info');
  let ul_menu = $('.task-event-infos ul.menu');

  if (!payload.data.command) {
    return;
  }
  let nb_tasks = parseInt(label_info.text(), 10);
  let task_id = 'event' + payload.data.uuid;

  switch (payload.data.status) {
    case 'starting':
      label_info.text(nb_tasks + 1);
      ul_menu.append('<li id="' + task_id + '"><a>' + payload.data.command + '<a/></li>');
      break;
    case 'completed':
      label_info.text(nb_tasks - 1);
      $('#' + task_id).remove();
      break;
  }
  sub_label_info.text(label_info.text());
}

$(document).ready(function() {
  event_subscriber_callback('asterisk_reload_progress', 'task_listener');
});
