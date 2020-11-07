$(function () {
    // When sticker clicked, copy that image url to clipboard
    $('img[name="stamp"]').on('click', function () {
        let $url = $(this).attr('src')

        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val($url).select();
        document.execCommand("copy");
        $temp.remove();
        // alert($url);
    });

    // Succeeded to load new sticker

    //.accordion1の中のp要素がクリックされたら
    $('.accordion').click(function(){
        //クリックされた.accordion1の中のp要素に隣接するul要素が開いたり閉じたりする。
        $(this).next('ul').slideToggle();
    });

    // $("#howtobtn").click(function(){
    //     $("howtoimg").toggleClass("hidden");
    // });

    // Sample code. <id="button01"> component calls Alert.
    // $("#button01").click(function(){
    //     alert("Button clicked k");
    //     window.parent.document.getElementById("leftFrame").contentWindow.location.reload();
    // });
    // <!-- <input name="btn01" id="button01" type="button" value="ボタン1"/>
    // </br> -->
})
