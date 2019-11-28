$(function () {
    $('img[name="stamp"]').on('click', function () {
        let $url = $(this).attr('src')

        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val($url).select();
        document.execCommand("copy");
        $temp.remove();

        // alert($url);
    })
})
