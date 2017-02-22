$(window).load(function() {
  setTimeout(function() {
    $.AdminLTE.layout.fix();
    $.AdminLTE.layout.fixSidebar();
  }, 250);
});

$(document).ready(function() {
  $('[data-toggle="popover"]').popover();

  $('.select2').select2();

  $('#table-list').DataTable({
    lengthChange: false,
    searching: false,
    order: [],
    columnDefs: [{
      targets: 'no-sort',
      orderable: false
    }]
  });
});
