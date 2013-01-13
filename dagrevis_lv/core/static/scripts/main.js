$(function() {
    // Fake font-size for tags.
    var $tags = $("#tags")
    if ($tags.length) {
        var sizes = [1, 1.2, 1.4, 1.6, 1.8, 2]
        $li_els = $tags.find("li")
        $.each($li_els, function(i, el) {
            var size_index = Math.floor(Math.random() * sizes.length)
            $(el).css("font-size", sizes[size_index] + "em")
        })
    }
})
