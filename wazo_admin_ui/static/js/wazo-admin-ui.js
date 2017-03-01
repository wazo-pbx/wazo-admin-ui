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

  $('#add-form').click(function() {
    $('#view-add-form').removeClass('hidden').removeAttr('style');
  });

  $('#error-details-show').click(function(event) {
      $('#error-details-show').hide();
      $('#error-details-hide').show();
  });

  $('#error-details-hide').click(function(event) {
      $('#error-details-show').show();
      $('#error-details-hide').hide();
  });

});
