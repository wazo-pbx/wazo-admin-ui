$.fn.dataTable.ext.buttons.delete_selected = {
  className: 'btn delete-selected-rows disabled',
  text: '<i class="fa fa-remove"></i>',
  titleAttr: $('#table-data-tooltip').attr('data-delete_tooltip'),
  action: function (e, dt, node, config) {
    if (confirm('Are you sure you want to delete these items?')) {
      dt.rows({selected: true}).every(function(rowIdx, tableLoop, rowLoop) {
        let row = this;
        let delete_url;
        let data_uuid = row.nodes().to$().attr('data-uuid');
        let data_id = row.nodes().to$().attr('data-id');
        if (data_uuid) {
          delete_url = $('#table-data-tooltip').attr('data-delete_url') + data_uuid;
        } else {
          delete_url = $('#table-data-tooltip').attr('data-delete_url') + data_id;
        }
        $.ajax({
          url: delete_url,
          success: function(response) {
            row.remove().draw();
            $('.delete-selected-rows').addClass('disabled');
          }
        });
      });
    }
  }
};

$.fn.dataTable.ext.buttons.edit_selected = {
  className: 'btn edit-selected-rows disabled',
  text: '<i class="fa fa-edit"></i>',
  titleAttr: $('#table-data-tooltip').attr('data-get_tooltip'),
  action: function (e, dt, node, config) {
    dt.rows({selected: true}).every(function(rowIdx, tableLoop, rowLoop) {
      let row = this;
      let data_uuid = row.nodes().to$().attr('data-uuid');
      let data_id = row.nodes().to$().attr('data-id');
      if (data_uuid) {
        window.location.href = $('#table-data-tooltip').attr('data-get_url') + data_uuid;
      } else {
        window.location.href = $('#table-data-tooltip').attr('data-get_url') + data_id;
      }
    });
  }
};

$.fn.dataTable.ext.buttons.add_entry = {
  className: 'btn add-entry-rows',
  text: '<i class="fa fa-plus"></i>',
  titleAttr: $('#table-data-tooltip').attr('data-add_tooltip'),
  action: function (e, dt, node, config) {
    let add_url = $('#table-data-tooltip').attr('data-add_url');
    if (add_url) {
      window.location.href = add_url;
    }
  }
};

$.extend(true, $.fn.dataTable.defaults, {
  lengthMenu: [[20, 50, 100, -1], [20, 50, 100, "All"]],
  pageLength: 20,
  order: [],
  autoWidth: false,
  responsive: true,
  searching: true,
  select: {
    style: 'os'
  },
  search: {
    smart: false
  },
  stateSave: true,
  columnDefs: [
    {
      targets:   0,
      responsivePriority: 1
    },
    {
      targets: -1,
      responsivePriority: 2
    },
    {
      targets: '_all',
      defaultContent: "-"
    },
    {
      targets: 'no-sort',
      orderable: false
    }
  ],
  dom: "<'row'<'col-sm-6'B><'col-sm-6'f>>" +
       "<'row'<'col-sm-12'tr>>" +
       "<'row'<'col-sm-5'il><'col-sm-7'p>>",
  buttons: [
    'selectAll',
    'selectNone',
    'add_entry',
    'edit_selected',
    'delete_selected',
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
    $('body').layout('fix');
    $('body').layout('fixSidebar');
  }, 250);
  init_datatable_buttons();
  build_column_actions();
});

$(document).ready(function() {
  $('#table-list').DataTable();

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

$(document).on('select.dt deselect.dt', function (e, dt, type, indexes) {
  let selected = dt.rows({ selected: true }).count();
  if (selected > 0) {
    $('.delete-selected-rows').removeClass('disabled');
    $('.edit-selected-rows').removeClass('disabled');
  }
  else if (selected < 1) {
    $('.delete-selected-rows').addClass('disabled');
    $('.edit-selected-rows').addClass('disabled');
  }
  if (selected > 1) {
    $('.edit-selected-rows').addClass('disabled');
  }
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
    let ul = $select2.next('.select2-container').first('ul.select2-selection__rendered');
    ul.sortable({
        placeholder : 'ui-state-highlight',
        forcePlaceholderSize: true,
        items       : 'li:not(.select2-search__field)',
        tolerance   : 'pointer',
        stop: function() {
            $($(ul).find('.select2-selection__choice').get().reverse()).each(function() {
                let id = $(this).data('data').id;
                let option = $select2.find('option[value="' + id + '"]')[0];
                $select2.prepend(option);
            });
        }
    });
}


function init_datatable_buttons() {
  $('.add-entry-rows').attr('data-toggle', 'modal');
  $('.add-entry-rows').attr('data-target', '#view-add-form');
  $('.add-entry-rows').click(function() {
    $('#view-add-form').removeClass('hidden').removeAttr('style');
    $('form').validator('update');
  });

  let clicks = 0, delay = 400;
  $('.dataTable').on('mousedown','tbody tr', function(event) {
    event.preventDefault();
    clicks++;

    let get_url;
    let data_uuid = $(this).attr('data-uuid');
    let data_id = $(this).attr('data-id');
    if (data_uuid) {
      get_url = $('#table-data-tooltip').attr('data-get_url') + data_uuid;
    } else if(data_id)  {
      get_url = $('#table-data-tooltip').attr('data-get_url') + data_id;
    }

    setTimeout(function() {
        clicks = 0;
    }, delay);

    if (clicks === 2 && get_url) {
        window.location.href = get_url;
        clicks = 0;
        return;
    } else {
        // mousedown event handler should be here
    }
  });
}


function get_delete_button(delete_url) {
  let delete_button = $('<a>', {
    'href': delete_url,
    'class': 'btn btn-xs btn-default delete-entry',
    'title': $('#table-data-tooltip').attr('data-delete_tooltip'),
    'onclick': "return confirm('Are you sure you want to delete this item?');"
  }).append($('<i>', {
      'class': 'fa fa-times'
  }));

  return delete_button.prop('outerHTML');
}


function build_column_actions() {
  $('#table-data-tooltip').append("<th width='10'></th>");
  $('.dataTable tbody tr').each(function() {
    let delete_url;
    let data_uuid = $(this).attr('data-uuid');
    let data_id = $(this).attr('data-id');
    if (data_uuid) {
      delete_url = $('#table-data-tooltip').attr('data-delete_url') + data_uuid;
    } else if(data_id) {
      delete_url = $('#table-data-tooltip').attr('data-delete_url') + data_id;
    }
    if (delete_url) {
      $(this).append('<td>' + get_delete_button(delete_url) + '</td>');
    }
  });
}


function create_table_serverside(config, actions_column=true) {
  let list_url = $('#table-list-serverside').attr('data-list_url');

  config.serverSide = true;
  config.processing = true;
  config.ajax = list_url;
  config.createdRow = function(row, data, dataIndex) {
    $(row).attr('data-uuid', data.uuid);
    $(row).attr('data-id', data.id);
  };
  if (actions_column) {
    config.columns.push({
      render: function(data, type, row) {
        let delete_url;
        if (row.uuid) {
          delete_url = $('#table-data-tooltip').attr('data-delete_url') + row.uuid;
        } else if(row.id)  {
          delete_url = $('#table-data-tooltip').attr('data-delete_url') + row.id;
        }
        return get_delete_button(delete_url);
      }
    });
  }

  let Table = $('#table-list-serverside').DataTable(config);
  // search only on 'enter', not on typing
  $('#table-list-serverside_filter input').unbind();
  $('#table-list-serverside_filter input').bind('keypress', function(e) {
    if (e.which == 13) {
      Table.search( this.value ).draw();
    }
  });
  return Table;
}
