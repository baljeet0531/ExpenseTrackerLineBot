//get config.ini

var fs = require("fs");

function parseINIString(data) {
    var regex = {
        section: /^\s*\[\s*([^\]]*)\s*\]\s*$/,
        param: /^\s*([^=]+?)\s*=\s*(.*?)\s*$/,
        comment: /^\s*;.*$/
    };
    var value = {};
    var lines = data.split(/[\r\n]+/);
    var section = null;
    lines.forEach(function (line) {
        if (regex.comment.test(line)) {
            return;
        } else if (regex.param.test(line)) {
            var match = line.match(regex.param);
            if (section) {
                value[section][match[1]] = match[2];
            } else {
                value[match[1]] = match[2];
            }
        } else if (regex.section.test(line)) {
            var match = line.match(regex.section);
            value[match[1]] = {};
            section = match[1];
        } else if (line.length == 0 && section) {
            section = null;
        };
    });
    return value;
}

try {
    var data = fs.readFileSync('../config.ini', 'utf8');

    var javascript_ini = parseINIString(data);
    console.log(javascript_ini['line-bot']);

}
catch (e) {
    console.log(e);
}


//get groupId
const queryString = window.location.search;
const urlParams = URLSearchParams(queryString);
const groupId = urlParams.get('groupId');

//get  
const line = require('@line/bot-sdk');
const client = new line.Client({
    channelAccessToken: line_bot_api_access_token
});

client.getGroupMemberIds(groupId)
    .then((ids) => {
        ids.forEach((id) => console.log(id));
    })
    .catch((err) => {
        // error handling
    });