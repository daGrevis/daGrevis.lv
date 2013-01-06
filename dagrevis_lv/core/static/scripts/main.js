$(function() {
    // Lets fake font size for tags.
    var $tags = $("#tags")
    if ($tags.length) {
        var ems = [1, 1.2, 1.4, 1.6, 1.8, 2]
        $lis = $tags.find("li")
        $.each($lis, function(i, el) {
            el_index = Math.floor(Math.random() * ems.length)
            $(el).css("font-size", ems[el_index] + "em")
        })
    }
})
