$(document).ready(function() {
    $('[data-toggle="popover"]').popover();
    $('.select2').select2();
});

$(window).load(function() {
    setTimeout(function() {
        $.AdminLTE.layout.fix();
        $.AdminLTE.layout.fixSidebar();
    }, 250);
});
