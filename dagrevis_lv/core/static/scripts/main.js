;(function() {
    "use strict"

    function in_viewport($el) {
        return (($el.offset().top + $el.height() <= $(window).scrollTop() + $(window).height()) && ($el.offset().top >= $(window).scrollTop()))
    }

    ;(function() {
        // Shakes icon for retweeting article when the icon is in the viewport.
        var has_shaked = false
        $(document).scroll(function() {
            var $icon_retweet = $(".icon-retweet")
            if (! has_shaked && in_viewport($icon_retweet)) {
                has_shaked = true
                setTimeout(function() {
                    $icon_retweet.effect("shake", {times: 4, distance: 6}, 400)
                }, 2000)
            }
        })
    }())
}())
