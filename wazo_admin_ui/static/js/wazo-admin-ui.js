$.extend(true, $.fn.dataTable.defaults, {
  lengthMenu: [[20, 50, 100, -1], [20, 50, 100, "All"]],
  pageLength: 20,
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
  ],
  initComplete: function(oSettings, json) {
    $('select[name^=table-list]').select2({
      theme: 'bootstrap',
      tags: true
    });
  },
});

$.fn.validator.Constructor.INPUT_SELECTOR = ':input:not([type="hidden"], [type="submit"], [type="reset"], button, .hidden :input)';

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
    $('form').validator('update');
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
  $(':input[type=password]:not(.row-template :input, [data-toggle=password])').password();

  $('.add-row-entry').click(function(e) {
    e.preventDefault();
    let context = $(this).closest('.row')[0];
    let template_row = $(".row-template", context)
    let row = template_row.clone();
    let element_total = $('.dynamic-table', context).find("tr").length;  // including template

    template_row.trigger("row:cloned", row);

    // Update name/id
    row.find(":input[id]").not(":button").each(function() {
      id = $(this).attr('id').replace(/-template-/, '-' + element_total + '-');
      $(this).attr('name', id).attr('id', id);
    });

    let last_tr = $('.dynamic-table', context).find("tr").last()
    row.removeClass("row-template hidden");
    row.insertAfter(last_tr);
    init_destination_select.call(row);
    init_select2.call(row);
    $(':input[type=password]', row).password();

    $('form').validator('update');
    $('form').validator('validate');

    $('.delete-row-entry', context).click(function(e) {
      e.preventDefault();
      $(this).closest("tr").remove();
      $('form').validator('update');
    });
  });

  // Update name/id of template row
  $('.row-template :input[id]').not(":button").each(function() {
    let template_id = $(this).attr('id').replace(/-\d{1,4}-/, '-template-');
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
}


function toggle_destination(current, value) {
  let context = $(this).closest(".destination-container")
  let destination = $('.destination-'+$(this).val(), context);

  let sub_dst_container = $('.destination-container div[class^=destination-]', context);
  $('[class^=destination-]', context).not('.destination-container').not(sub_dst_container).addClass("hidden");
  destination.removeClass("hidden");
  $('form').validator('update');
}


function build_table_actions(get_url, delete_url, id, tooltips) {
  remove = $('<a>', {
    'href': delete_url + id,
    'class': 'btn btn-xs btn-danger',
    'title': tooltips.delete,
    'onclick': "return confirm('Are you sure you want to delete this item?');"
  })
 .append($('<i>', {
    'class': 'fa fa-minus'
  }))

  view = $('<a>', {
    'href': get_url + id,
    'class': 'btn btn-xs btn-info',
    'title': tooltips.get,
  })
  .append($('<i>', {
    'class': 'fa fa-eye'
  }))

  return view.prop('outerHTML') + " " + remove.prop('outerHTML');
}


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
    let allow_custom_values = this.hasAttribute('data-allow_custom_values');
    if (allow_custom_values || ajax_url === ""){
      config['tags'] = true;
    }

    if (ajax_url) {
      config['placeholder'] = 'Select...';
      config['ajax'] = {
          url: ajax_url,
          delay: 450,
      };
      let ajax_data = $(this).attr('data-ajax_data');
      if (ajax_data) {
        config['ajax']['data'] = new Function("term", ajax_data);
      }

    } else {
      if (! config.tags) {
        config['minimumResultsForSearch'] = 5;
      }
    }

    let allow_clear = this.hasAttribute('data-allow_clear');
    if($(this).attr('multiple') || allow_clear) {
      config['allowClear'] = true;
    }

    $(this).select2(config);

    if($(this).attr('multiple')) {
      select2_sortable($(this));
    }
  });
}


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
  let list_url = $('#table-list-serverside').attr('data-list_url');
  let get_url = $('.list-table-action').attr('data-get_url');
  let delete_url = $('.list-table-action').attr('data-delete_url');
  let tooltips = {'get': $('.list-table-action').attr('data-get_tooltip'),
                  'delete': $('.list-table-action').attr('data-delete_tooltip')}

  config.serverSide = true;
  config.processing = true;
  config.ajax = list_url;
  if (get_url || delete_url) {
    config.columns.push({
      render: function(data, type, row) {
        return build_table_actions(get_url, delete_url, row.uuid, tooltips);
      }
    });
  }

  var Table = $('#table-list-serverside').DataTable(config);

  // search only on 'enter', not on typing
  $('#table-list-serverside_filter input').unbind();
  $('#table-list-serverside_filter input').bind('keypress', function(e) {
    if (e.which == 13) {
      Table.search( this.value ).draw();
    }
  });
}
