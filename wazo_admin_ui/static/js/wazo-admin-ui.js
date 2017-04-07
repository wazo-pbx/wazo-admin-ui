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

  init_destination_select.call(this);
  init_select2.call(this);

  $('.add-row-entry').click(function(e) {
    e.preventDefault();
    let context = $(this).closest('.row')[0];
    let row = $(".row-template", context).clone();
    let element_total = $('.dynamic-table', context).find("tr").length;  // including template

    // Update name/id
    row.find(":input").not(":button").each(function() {
      id = $(this).attr('id').replace(/(.*)-template-(.*)/m, '$1-' + element_total + '-$2');
      $(this).attr('name', id).attr('id', id);
    });

    let last_tr = $('.dynamic-table', context).find("tr").last()
    row.removeClass("row-template hidden");
    row.insertAfter(last_tr);
    init_destination_select.call(row);
    init_select2.call(row);

    $('.delete-row-entry', context).click(function(e) {
      e.preventDefault();
      $(this).closest("tr").remove();
    });
  });

  // Update name/id of template row
  $('.row-template :input').not(":button").each(function() {
    let template_id = $(this).attr('id').replace(/(.*)-\d{1,4}-(.*)/m, '$1-template-$2');
    $(this).attr('name', template_id).attr('id', template_id);
  });

  $('.delete-row-entry').click(function(e) {
    e.preventDefault();
    $(this).closest("tr").remove();
  });
});


function init_destination_select() {
  $('.destination-select', this).on("select2:select", function(e) {
      toggle_destination.call(this);
  });
  $('.destination-select', this).each(function(index) {
      toggle_destination.call(this);
  });

};


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


function init_select2() {
  $('.selectfield', this).each(function(index) {
    if ($(this).parents('.row-template').length) {
      return;
    }
    let config = {
      theme: 'bootstrap',
      width: null,
    };

    let ajax_url = $(this).attr('data-listing_href');
    if (ajax_url) {
      config['placeholder'] = 'Select...';
      config['ajax'] = {
          url: ajax_url,
          delay: 450,
      };

      if($(this).attr('multiple')) {
          config['allowClear'] = true;
      }
    } else {
      config['minimumResultsForSearch'] = 5;
    }

    $(this).select2(config);
    select2_sortable($(this));
  });
};


// https://github.com/select2/select2/issues/3004
function select2_sortable($select2){
    var ul = $select2.next('.select2-container').first('ul.select2-selection__rendered');
    ul.sortable({
        placeholder : 'ui-state-highlight',
        forcePlaceholderSize: true,
        items       : 'li:not(.select2-search__field)',
        tolerance   : 'pointer',
        stop: function() {
            $($(ul).find('.select2-selection__choice').get().reverse()).each(function() {
                var id = $(this).data('data').id;
                var option = $select2.find('option[value="' + id + '"]')[0];
                $select2.prepend(option);
            });
        }
    });
}


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
