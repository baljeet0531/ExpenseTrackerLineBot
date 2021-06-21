//get groupID
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const groupID = urlParams.get('groupId');
// const userID = urlParams.get('userID');
// const userName = urlParams.get('userName');

console.log(groupID);
// console.log(userID);
// console.log(userName);

$(document).ready(function () {
    $.get('./group_data.json', function (json) {
        group = json[groupID];
        user_list = group["user_list"]

        $.each(user_list, function (key, val) {
            $(`<div class=\"user-name-container ${key}\">`).appendTo('#login-user-flex, #share-user-flex');
            var txt = ""
            txt += `<p class=\"user-name\">${val["user_name"]}</p>`
            txt += "</div>"

            $(`.${key}`).html(txt);
        });

    });
});

$('#login-user-flex').on("click", ".user-name-container", function () {
    if (!$(this).hasClass('login-user')) {
        $('#login-user-flex .user-name-container').removeClass('login-user');
        $('#login-user-flex .user-name-container').children('p').css('color', '#6F6F6F');
        $('#login-user-flex .user-name-container').css('background-color', '#F5F4EF');
        $(this).toggleClass('login-user');
        $(this).children('p').css('color', '#000000DE');
        $(this).css('background-color', '#EADAA6');
    }
    else if ($(this).hasClass('login-user')) {
        $(this).removeClass('login-user');
        $(this).children('p').css('color', '#6F6F6F');
        $(this).css('background-color', '#F5F4EF');
    }
})

$('#welcome-btn').click(function () {
    if ($('#login-user-flex .user-name-container').hasClass('login-user')) {
        $('#front-cover').css("display", "none");
        $('#info-page').fadeIn(500);

        $('#login-user-flex .user-name-container').hasClass('login-user')

        $('.login-user').clone().appendTo('#pay-user-flex');

        $('.acc-name').html(`${$('.login-user p').html()}'S ACCOUNTS`);
    }
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
    $('#save-btn-inact, #add-pg-back-btn, #save-btn-act').fadeOut(500);
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

$('#share-user-flex').on("click", ".user-name-container", function () {
    var userName = $(this).children('p').html();
    var userID = $(this).attr('class').split(' ')[1];
    if (!$(this).hasClass('selected')) {
        $(this).toggleClass('selected');
        $(this).children('p').css('color', '#000000DE');
        $(this).css('background-color', '#EADAA6');

        $(`<div class=\"edit-share-user ${userID}\" id=${userName}>`).appendTo('#edit-share-user-container');
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

        $('#save-btn-inact').css('display', 'none');
        $('#save-btn-act').css('display', 'block');

    }
    else if ($(this).hasClass('selected')) {
        $(this).removeClass('selected');
        $(this).children('p').css('color', '#7C7A7ADE');
        $(this).css('background-color', '#EFEEED');
        $(`#edit-share-user-container #${userName}`).remove();
    }

    if ($('#edit-share-user-container').children().length > 0) {
        $('#save-btn-inact').css('display', 'none');
        $('#save-btn-act').css('display', 'block');
    }
    else {
        $('#save-btn-inact').css('display', 'block');
        $('#save-btn-act').css('display', 'none');
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

$('#save-btn-act').click(function () {

    save_json = {
        "host": $('.login-user').attr('class').split(' ')[1],
        "category": $('.select-cate').attr('id'),
        "items": $('#add-items input').val(),
        "price": $('#add-price input').val(),
        "share": {}
    }

    $('#edit-share-user-container').children().each(function () {
        var userID = $(this).attr('class').split(' ')[1];
        save_json["share"][userID] = $(this).find('input').val();
    });

    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    today = mm + '/' + dd;

    console.log(save_json)

    $.ajax({
        url: './save_record',
        type: "POST",
        data: JSON.stringify({
            groupID: groupID,
            date: today,
            save_json: save_json
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function () {
            console.log("success")
        }
    })

    // $.post('./save_record', {
    //     date: today,
    //     save_json: JSON.stringify(save_json, null, '\t')
    // });
    // , (comment_id) => {
    //     resolve(comment_id);
    // });
})





