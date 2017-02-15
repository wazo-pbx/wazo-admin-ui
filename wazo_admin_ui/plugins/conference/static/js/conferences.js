$(document).ready(function() {
    $('#table-conferences').DataTable({
        'lengthChange': false,
        'searching': false
    });

    $('#add-conference').click(function() {
        $('#view-add-conference').removeClass('hidden').removeAttr('style');
    });
});

