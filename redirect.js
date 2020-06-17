
var link = "http://cf68f917a1155.in.ngrok.io"

//var link = "http://www.google.com"
document.getElementById("redirect_button").onclick = function () {
    const url = "https://www.google.com/";
    $.ajax({
        url: url,
        dataType: 'jsonp',
        statusCode: {
            200: function () {
                console.log("status code 200 returned");
            },
            404: function () {
                console.log("status code 404 returned");
            }
        },
        error: function () {
            console.log("Error function : Error");
        }
    });
}

// document.getElementById("redirect_button").onclick = function () {
//     location.href = link;
// };


// function UrlExists(url, cb){
//     jQuery.ajax({
//         url:      url,
//         dataType: 'text',
//         type:     'GET',
//         complete:  function(xhr){
//             if(typeof cb === 'function')
//                cb.apply(this, [xhr.status]);
//         }
//     });
// }

// UrlExists('-- Insert Url Here --', function(status) {
//     if(status === 200) {
//         -- Execute code if successful --
//     } else if(status === 404) {
//         -- Execute code if not successful --
//     }else{
//        -- Execute code if status doesn't match above --
//     }
// });