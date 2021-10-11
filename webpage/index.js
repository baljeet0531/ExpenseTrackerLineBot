//get groupID
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const groupID = urlParams.get('groupId');

$(document).ready(function () {
    loadUserList();
});

function loadUserList() {
    $.ajax({
        url: './get_group_data',
        type: "POST",
        data: JSON.stringify({
            groupID: groupID
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (group_json) {
            user_list = (group_json["data"]["user_list"]);
            $.each(user_list, function (key, val) {
                $(`<div class=\"user-name-container ${key}\">`).appendTo('#login-user-flex, #share-user-flex');
                var txt = ""
                txt += `<p class=\"user-name\">${val["user_name"]}</p>`
                txt += "</div>"

                $(`.${key}`).html(txt);
            });
        },
        error: function () {
            console.log("error");
        }
    })
}


function loadGroupHistory() {
    $.ajax({
        url: './get_group_data',
        type: "POST",
        data: JSON.stringify({
            groupID: groupID
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (group_json) {
            prependGroupHistory(group_json["data"]["history"]);
        },
        error: function () {
            console.log("error");
        }
    })

}
function prependGroupHistory(group_history) {
    $('#group-history').empty();
    login_user_id = $('.login-user').attr('class').split(' ')[1]
    $.each(group_history, function (date, dateRecord) {
        $(`<div class=\"date-record ${date}\"></div>`).prependTo('#group-history');
        $.each(dateRecord, function (index, recordInfo) {
            $(`<div class=\"record-info\" id=\"${date}_${index}\">`).prependTo(`.${date}`);

            var category = recordInfo["category"];
            var items = recordInfo["items"];
            var host = recordInfo["host"];
            var host_name = $(`.${host} p`).html();
            var price = recordInfo["price"];
            var myShare = recordInfo["share"][login_user_id];
            if (myShare == null) {
                myShare = 0;
            }

            var txt = ""
            txt += `<img class=\"category-icon\" src=\"./image/${category}.png\">`
            txt += "<div class=\"right-border\"></div>"
            txt += "<div class=\"user-name-container\">"
            txt += `<p class=\"user-name\">${host_name}</p>`
            txt += "</div>"
            txt += `<p class=\"item-name\">${items}</p>`
            txt += `<p class=\"total-cost\">${price} twd</p>`
            txt += `<p class=\"my-share\">My share: ${myShare} twd</p>`
            txt += "</div>"

            $(`#${date}_${index}`).html(txt);

            // containerWidth = parseFloat($(`#${date}_${index} .user-name-container`).css('width')) + 22;
            // itemWidth = parseFloat($(`#${date}_${index} .item-name`).css('width'));
            // if (containerWidth > itemWidth) {
            //     $(`#${date}_${index} .item-name`).css('width', containerWidth);
            // }
            // else if (containerWidth < itemWidth) {
            //     diff = (itemWidth - containerWidth) / 2;
            //     $(`#${date}_${index} .user-name-container`).css('margin-left', diff);
            //     $(`#${date}_${index} .user-name-container`).css('margin-right', diff);
            // }

        });
        $(`<p class=\"date\">${date}</p>`).prependTo(`.${date}`);
    });

}

function loadDebts() {
    $.ajax({
        url: './get_group_data',
        type: "POST",
        data: JSON.stringify({
            groupID: groupID
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (group_json) {
            appendDebts(group_json["data"]["user_list"]);
        },
        error: function () {
            console.log("error");
        }
    })
}

function appendDebts(user_list) {
    $('#paid .user-list-container').empty();
    $('#paid-container .d-list-container').empty();
    $('#payback .user-list-container').empty();
    $('#payback-container .d-list-container').empty();
    $('#acc-history').empty();

    login_user_id = $('.login-user').attr('class').split(' ')[1]
    login_user_name = user_list[login_user_id]["user_name"]
    login_user_debts = user_list[login_user_id]["debts"]
    login_user_debts_records = user_list[login_user_id]["debts_records"]

    total_debts = 0
    $.each(login_user_debts, function (user_id, price) {
        if (user_id != login_user_id) {
            total_debts += price
            if (price > 0) {
                $(`<div class=\"user-name-container ${user_id}\">`).appendTo('#paid .user-list-container');
                var txt = ""
                txt += `<p class=\"user-name\">${user_list[user_id]["user_name"]}</p>`
                txt += "</div>"

                $(`#paid .user-list-container .${user_id}`).html(txt);

                $(`<div class=\"interact-user-container ${user_id}\">`).appendTo('#paid-container .d-list-container');

                txt = ""
                txt += "<div class=\"user-name-container\">"
                txt += `<p class="user-name">${user_list[user_id]["user_name"]}</p>`
                txt += "</div>"
                txt += `<p class="total-cost">${price} twd</p>`
                txt += "<img class=\"interact-btn received-btn\" src=\"./image/received-btn.png\">"
                txt += "</div>"
                $(`#paid-container .d-list-container .${user_id}`).html(txt);
            }
            else if (price < 0) {
                $(`<div class=\"user-name-container ${user_id}\">`).appendTo('#payback .user-list-container');
                var txt = ""
                txt += `<p class=\"user-name\">${user_list[user_id]["user_name"]}</p>`
                txt += "</div>"
                $(`#payback .user-list-container .${user_id}`).html(txt);

                $(`<div class=\"interact-user-container ${user_id}\">`).appendTo('#payback-container .d-list-container');
                txt = ""
                txt += "<div class=\"user-name-container\">"
                txt += `<p class="user-name">${user_list[user_id]["user_name"]}</p>`
                txt += "</div>"
                txt += `<p class="total-cost">${price} twd</p>`
                txt += "<img class=\"interact-btn payback-btn\" src=\"./image/payback-btn.png\">"
                txt += "</div>"
                $(`#payback-container .d-list-container .${user_id}`).html(txt);
            }
        }
    });
    $('.acc-debts').html(`TOTAL DEBTS: ${total_debts}`);

    $.each(login_user_debts_records, function (index, records) {
        dateTime = records["date_time"];
        interactWith = records["interact_with"];
        method = records["method"];
        money = records["money"];


        $(`<div class="history-grid"  id=his_${index}>`).prependTo('#acc-history');
        var txt = ""
        txt += "<div>"
        txt += `<p class="time-stamp">${dateTime}</p>`
        txt += "</div>"
        txt += `<div class="user-name-container">`
        txt += `<p class="user-name">${user_list[interactWith]["user_name"]}</p>`
        txt += "</div>"
        txt += "<div>"
        if (method == "payback") {
            txt += `<p class="describe">我已還 ${money} twd</p>`;
        }
        else if (method == "received") {
            txt += `<p class="describe">我收到 ${money} twd</p>`;
        }
        txt += "</div>"
        txt += "</div>"

        $(`#his_${index}`).html(txt);
    });


}

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
        loadGroupHistory();
        loadDebts();
        $('#front-cover').css("display", "none");
        $('#info-page').fadeIn(500);

        $('#login-user-flex .user-name-container').hasClass('login-user')

        $('.login-user').clone().appendTo('#pay-user-flex');

        $('.acc-name').html(`${$('.login-user p').html()}'s Accounts`);
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
    $('.selected').click();
    $('#add-pg-back-btn').click();
    $('.select-cate').click();
    $('#add-items input').val('');
    $('#add-price input').val('');

    $('#saving-blur').css('display', 'none');
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
        txt += "<input type=\"number\" min=\"1\" max=\"999999\" oninput=\"validity.valid||(value='');\">";
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
    shareTotalPrice = 0
    totalPrice = $('#add-price input').val()
    $('#edit-share-user-container input').each(function () {
        shareTotalPrice += parseInt($(this).val());
    });
    if (shareTotalPrice == totalPrice) {
        $('#saving-blur').css('display', 'block');

        save_json = {
            "host": $('.login-user').attr('class').split(' ')[1],
            "category": $('.select-cate').attr('id'),
            "items": $('#add-items input').val(),
            "price": parseInt($('#add-price input').val()),
            "share": {}
        }

        $('#edit-share-user-container').children().each(function () {
            var userID = $(this).attr('class').split(' ')[1];
            save_json["share"][userID] = parseInt($(this).find('input').val());
        });

        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        today = mm + '-' + dd;

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
            success: function (group_json) {
                $('#close-btn').click();
                console.log("success")
                console.log(group_json);
                group_history = group_json["data"]["history"];
                user_list = group_json["data"]["user_list"];

                prependGroupHistory(group_history);
                appendDebts(user_list);
            },
            error: function () {
                console.log("error");
            }
        })
    }
})
$('#payback-container').on('click', '.payback-btn', function () {
    receiveName = $(this).siblings('.user-name-container').children('p').html();
    receiveMoney = $(this).siblings('.total-cost').html().split(" ")[0].slice(1);
    receiveUserID = $(this).parent('.interact-user-container').attr('class').split(' ')[1];
    $('#payback-describe-container .user-name-container').toggleClass(`${receiveUserID}`);
    $('#payback-describe-container .user-name').html(receiveName);
    $('#payback-describe-container input').val(receiveMoney);

    $('.transparent-blur').fadeIn(500);
    $('#payback-describe-container').css('display', 'flex');
})

$('#paid-container').on('click', '.received-btn', function () {
    paybackName = $(this).siblings('.user-name-container').children('p').html();
    paybackMoney = $(this).siblings('.total-cost').html().split(" ")[0];

    $('#share-container input').val(`${paybackName}記得還我${paybackMoney}元喔~`);

    $('.transparent-blur').fadeIn(500);
    $('#share-container').css('display', 'block');
})

$('.cancel-btn').click(function () {
    $('.transparent-blur,#payback-describe-container, #share-container').fadeOut(500);
    setTimeout(function () {
        $('#payback-describe-container .user-name').html('');
        $('.confirm-popoutinput').val('');
        $('#payback-describe-container .user-name-container').attr('class', 'user-name-container');
    }, 400)
})

$('.confirm-btn').click(function () {
    if ($('#payback-describe-container').css('display') != 'none') {
        receiveName = $('#payback-describe-container .user-name').html();
        receiveMoney = $('#payback-describe-container input').val();
        receiveUser = $('#payback-describe-container .user-name-container').attr('class').split(' ')[1];
        paybackUser = $('.login-user').attr('class').split(' ')[1];
        $('#saving-blur').css('display', 'block');

        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var hh = String(today.getHours()).padStart(2, '0');
        var min = String(today.getMinutes()).padStart(2, '0');
        dateTime = mm + '-' + dd + ' ' + hh + ':' + min;

        $.ajax({
            url: './save_debts',
            type: "POST",
            data: JSON.stringify({
                groupID: groupID,
                date_time: dateTime,
                payback_user: paybackUser,
                received_user: receiveUser,
                money: receiveMoney
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (user_list_json) {
                receiveName = $('#payback-describe-container .user-name').html();
                receiveMoney = parseInt($('#payback-describe-container input').val());
                $('#share-container input').val(`${receiveName}我還你${receiveMoney}元了喔~`);
                $('#payback-describe-container').fadeOut(500);
                $('#share-container').fadeIn(500);
                $('#saving-blur').css('display', 'none');

                console.log("success")
                appendDebts(user_list_json["data"]);
            },
            error: function () {
                console.log("error");
            }
        })
    }
    else if ($('#share-container').css('display') != 'none') {
        shareText = $('#share-container input').val();

        window.open(`https://line.me/R/share?text=${encodeURIComponent(shareText)}`)
        $('.cancel-btn').click();
    }
})

$('.transparent-bg').click(function () {
    $('.cancel-btn').click();
})


