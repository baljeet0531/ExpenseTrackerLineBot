//get groupId
// const queryString = window.location.search;
// const urlParams = new URLSearchParams(queryString);
// const groupId = urlParams.get('groupId');
// const userId = urlParams.get('userId');
// const userName = urlParams.get('userName');

// console.log(groupId);
// console.log(userId);
// console.log(userName);

$('#welcome-btn').click(function () {
    $('#front-cover').css("display", "none");
    $('#info-page').fadeIn(500);
})

$('#detail-btn').click(function () {
    $('#main-page,#detail-page').stop();
    $('#detail-page').css("display", "block");
    $('#detail-page').animate({ 'left': '0vw' });
    $('#main-page').animate({ 'left': '-100vw' }, 500, function () { $('#main-page').css('display', 'none'); })
})

$('.back-btn').click(function () {
    $('#main-page,#detail-page').stop();
    $('#main-page').css("display", "block");
    $('#main-page').animate({ 'left': '0vw' });
    $('#detail-page').animate({ 'left': '100vw' }, 500, function () { $('#detail-page').css('display', 'none'); })
})

$('#add-btn').click(function () {
    if ($('#main-page').css("display") == "block") {
        $('#add-page').css({ 'left': '100vw', "display": "block" });
        $('#add-page').animate({ 'left': '0vw' });
        $('#main-page').animate({ 'left': '-100vw' }, 500, function () {
            $('#main-page').css('left', '0vw');
            $('#detail-page').css({ 'left': '100vw', "display": "none" });
        })
    }
    else if ($('#detail-page').css("display") == "block") {
        $('#add-page').fadeIn(500, function () {
            $('#main-page').css('left', '0vw');
            $('#detail-page').css({ 'left': '100vw', "display": "none" });
        });
    }
})

$('#close-btn').click(function () {
    $('#main-page').css('display', 'block');
    $('#add-page').fadeOut(500);
})

$('#next-btn').click(function () {
    if ($('#category-flex div').hasClass('select-cate') && $('#add-items input').val() && $('#add-price input').val()) {
        $('#add-content,#share-content').stop();
        $('#share-content').css({ 'left': '100vw', "display": "block" });
        $('#share-content').animate({ 'left': '0vw' });
        $('#add-content').animate({ 'left': '-100vw' }, 500, function () { $('#add-content').css('display', 'none'); })
        $('#save-btn-inact, #add-pg-back-btn').fadeIn(500);
        $('#next-btn').fadeOut(500);

        calculateShare();
    }
})

$('#add-pg-back-btn').click(function () {
    $('#add-content,#share-content').stop();
    $('#add-content').css("display", "block");
    $('#add-content').animate({ 'left': '0vw' });
    $('#share-content').animate({ 'left': '100vw' }, 500, function () { $('#share-content').css('display', 'none'); })
    $('#save-btn-inact, #add-pg-back-btn').fadeOut(500);
    $('#next-btn').fadeIn(500);
})


$('#category-flex div').click(function () {
    if ($(this).attr('class') == "") {
        $('#category-flex div').attr('class', "");
        $('#category-flex div').css('border-color', '#FFFFFF');
        $(this).attr('class', 'select-cate');
        $(this).css('border-color', '#515472');
    }
    else if ($(this).attr('class') == 'select-cate') {
        $(this).attr('class', "");
        $(this).css('border-color', '#FFFFFF');
    }
})

$('#share-user-flex .user-name-container').click(function () {
    var userName = $(this).children('p').html();
    if (!$(this).hasClass('selected')) {
        $(this).toggleClass('selected');
        $(this).children('p').css('color', '#000000DE');
        $(this).css('background-color', '#EADAA6');

        $(`<div class=\"edit-share-user\" id=${userName}>`).appendTo('#edit-share-user-container');
        var txt = ""

        txt += "<div id=\"edit-share-user-name\">";
        txt += "<div class=\"user-name-container\">";
        txt += `<p class=\"user-name\">${userName}</p>`;
        txt += "</div>";
        txt += "</div>";
        txt += "<div id=\"edit-share-user-price\">";
        txt += "<input type=\"number\" min=\"1\" oninput=\"validity.valid||(value='');\">";
        txt += "<p class=\"p-twd\">twd</p>";
        txt += "</div>";
        txt += "</div>"

        $(`#${userName}`).html(txt);
    }
    else if ($(this).hasClass('selected')) {
        $(this).removeClass('selected');
        $(this).children('p').css('color', '#7C7A7ADE');
        $(this).css('background-color', '#EFEEED');
        $(`#edit-share-user-container #${userName}`).remove();
    }

    calculateShare();
})

function calculateShare() {
    var totalPrice = $('#add-price input').val();
    var shareUserNum = $('#edit-share-user-container').children().length;
    var avgShare = parseInt(totalPrice / shareUserNum);
    var extraShare = totalPrice % shareUserNum;
    for (i = 1; i <= shareUserNum; i++) {
        if (i <= extraShare) {
            $(`#edit-share-user-container .edit-share-user:nth-child(${i}) input`).val(avgShare + 1);
        }
        else {
            $(`#edit-share-user-container .edit-share-user:nth-child(${i}) input`).val(avgShare);
        }
    }
}





