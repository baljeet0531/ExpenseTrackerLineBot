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
    $('#main-page').animate({ 'right': '100vw' }, 500, function () { $('#main-page').css('display', 'none'); })
})

$('.back-btn').click(function () {
    $('#main-page,#detail-page').stop();
    $('#main-page').css("display", "block");
    $('#main-page').animate({ 'right': '0vw' });
    $('#detail-page').animate({ 'left': '100vw' }, 500, function () { $('#detail-page').css('display', 'none'); })
})

