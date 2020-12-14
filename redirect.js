var link = "https://3d229f42cefd.in.ngrok.io"

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
  }

  var timeout;
  var timeout1;
  var timeout2;
document.getElementById("redirect_button").onclick = function () {
    var flag;
    $("#more_info").html("Checking server status. Hang on..");
    $.ajax({
        url: link,
        dataType: 'jsonp',
        statusCode: {
            200: function () {   
                console.log("status code 200 returned. URL exist. Server is running."); 
                clearTimeout(timeout);
                timeout = setTimeout(function() {
                    $("#more_info").html("Server is up and running.");
                }, 2000);

                clearTimeout(timeout);
                timeout = setTimeout(function() {
                    $("#more_info").html("Checking reverse proxy tunnel status.");
                }, 2000);

                clearTimeout(timeout1);
                timeout1 = setTimeout(function() {
                    $("#more_info").html("Done redirecting.");
                }, 4000);

                clearTimeout(timeout2);
                timeout2 = setTimeout(function() {
                    location.href = link;
                }, 5000);
            },
            404: function () {
                console.log("status code 404 returned. URL does not exist. Server is not running.");
                clearTimeout(timeout);
                timeout = setTimeout(function() {
                    $("#more_info").attr('style','color: red');
                    $("#more_info").html("Server is Down.");
                    document.getElementById("redirect_button").disabled = true;
                    document.getElementById("redirect_button").innerHTML = "Cannot redirect :(";
                }, 2000);
            }
        }
    });
}
