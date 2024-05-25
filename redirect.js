var link = "https://fbaf-103-197-221-250.ngrok-free.app/web/"

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

function urlExists(url, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open('HEAD', url, true);
    xhr.onreadystatechange = function() {
        console.log(xhr);
        if (xhr.readyState === 4) {
            callback(xhr.status >= 200 && xhr.status < 300);
        }
    };
    xhr.onerror = function() {
        callback(false);
    };
    xhr.send();
}
document.getElementById('redirect_button').addEventListener('click', function() {
    urlExists(link, function(exists) {
        if(exists) {
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
                    window.location.href = link;
                }, 5000);
        } else {
            console.log("status code 404 returned. URL does not exist. Server is not running.");
                clearTimeout(timeout);
                timeout = setTimeout(function() {
                    $("#more_info").attr('style','color: red');
                    $("#more_info").html("Server is Down.");
                    document.getElementById("redirect_button").disabled = true;
                    document.getElementById("redirect_button").innerHTML = "Cannot redirect :(";
                }, 2000);
        }
    });
});

