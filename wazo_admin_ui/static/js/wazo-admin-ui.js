$.extend(true, $.fn.dataTable.defaults, {
  lengthMenu: [10, 20],
  order: [],
  autoWidth: false,
  responsive: true,
  searching: true,
  search: {
    smart: false
  },
  columnDefs: [
    { responsivePriority: 1, targets: 0 },
    { responsivePriority: 2, targets: -1 },
    {
      targets: '_all',
      defaultContent: "-"
    },
    {
      targets: 'no-sort',
      orderable: false
    }
  ]
});

$(window).load(function() {
  setTimeout(function() {
    $.AdminLTE.layout.fix();
    $.AdminLTE.layout.fixSidebar();
  }, 250);
});

$(document).ready(function() {

  $('.selectfield').select2({
    theme: 'bootstrap',
    width: null,
  });

  $('#table-list').DataTable();

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

  $('.destination-select').on("select2:select", function(e) {
      toggle_destination.call(this);
  });
  $('.destination-select').each(function(index) {
      toggle_destination.call(this);
  });

  $('.selectfield-ajax').each(function(index) {
    let ajax_url = $(this).attr('data-listing_href');
    $('.selectfield-ajax', context).select2({
      theme: 'bootstrap',
      placeholder: 'Select...',
      width: null,
      ajax: {
        url: ajax_url,
        delay: 450,
        },
    });
  });

});


function toggle_destination(current, value) {
    let context = $(this).closest(".destination-container")
    let destination = $('.destination-'+$(this).val(), context);
    let ajax_url = destination.attr('data-destination_href');

    $('[class^=destination-]', context).addClass("hidden");
    destination.removeClass("hidden");
};


function build_table_actions(get_url, delete_url, id) {
  remove = $('<a>', {
    'href': delete_url + id,
    'class': 'btn btn-xs btn-danger',
    'onclick': "return confirm('Are you sure you want to delete this item?');"
  })
 .append($('<i>', {
    'class': 'fa fa-minus'
  }))

  view = $('<a>', {
    'href': get_url + id,
    'class': 'btn btn-xs btn-info',
  })
  .append($('<i>', {
    'class': 'fa fa-eye'
  }))

  return view.prop('outerHTML') + " " + remove.prop('outerHTML');
};


function create_table_serverside(config) {
  config.serverSide = true
  config.processing = true
  var Table = $('#table-list-serverside').DataTable(config);

  // search only on 'enter', not on typing
  $('#table-list-serverside_filter input').unbind();
  $('#table-list-serverside_filter input').bind('keypress', function(e) {
    if (e.which == 13) {
      Table.search( this.value ).draw();
    }
  });
};
