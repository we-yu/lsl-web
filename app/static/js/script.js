$(function () {
    $('img[name="stamp"]').on('click', function () {
        let $url = $(this).attr('src')

        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val($url).select();
        document.execCommand("copy");
        $temp.remove();
        // alert($url);
    });


    //.accordion1の中のp要素がクリックされたら
	$('.accordion').click(function(){

		//クリックされた.accordion1の中のp要素に隣接するul要素が開いたり閉じたりする。
		$(this).next('ul').slideToggle();

	});

})
