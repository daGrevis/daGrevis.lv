$(function() {
    $.each($(".comment"), function(i, comment) {
        var $comment = $(comment);
        $comment.css("marginLeft", 20 * ($comment.data("depth")));
    });
});
