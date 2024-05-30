var link = "https://9e1f-103-197-221-248.ngrok-free.app\web\"

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
    fetch(link)
        .then(response => {
            if (!response.ok) {
                if (response.status === 404) {
                    console.log("status code 404 returned. URL does not exist. Server is not running.");
                    clearTimeout(timeout);
                    timeout = setTimeout(function() {
                            $("#more_info").attr('style','color: red');
                            $("#more_info").html("Server is Down.");
                            document.getElementById("redirect_button").disabled = true;
                            document.getElementById("redirect_button").innerHTML = "Cannot redirect :(";
                        }, 2000);
                } else {
                    console.log("Some other error occured. The Check to see if the website is up or not gave: "+response.status+" status code");
                }
            }
            const contentType = response.headers.get('Content-Type');
            console.log(contentType);
            
            if (contentType.includes('application/json') || contentType.includes('application/javascript') || contentType.includes('text/html')) {
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
                throw new Error(`Unexpected content type:`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            console.log("status code 404 returned. URL does not exist. Server is not running.");
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                    $("#more_info").attr('style','color: red');
                    $("#more_info").html("Server is Down.");
                    document.getElementById("redirect_button").disabled = true;
                    document.getElementById("redirect_button").innerHTML = "Cannot redirect :(";
            }, 2000);
        });
};
