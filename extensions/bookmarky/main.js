//
// Main
//

console.log("Starting Main");

// Stage Envs
// var API_URL = "http://api.bookmarky-stage.colfax.int/info";
// var TOKEN = "";
// var API_KEY = "";
// var CLIENT_ID = "";

// Dev Envs
var API_URL = "http://api.bookmarky-dev.alix.lol/info";
var API_KEY = "";
var CLIENT_ID = "";

function get_info(){
  $.ajax({
    type: "GET",
    url: API_URL,
    headers: {
        "Token": TOKEN
    },
    //   data: data,
    success: success,
    dataType: "json"
    });
}


function get_token(){
  /// Get an access token from the Bookmarky api
  $.ajax({
    type: "POST",
    url: API_URL + "/auth",
    headers: {
        "X-Api-Key": API_KEY,
        "Client-ID": API_KEY,
    },
    //   data: data,
    success: success,
    dataType: "json"
    });
}

function success(data){
  console.log("success!");
  console.log(data);
}

function get_browser_details(){
  browser.tabs.query({active: true, currentWindow: true}, (tabs) => {
    // Get the URL and title of the current active tab
    var url = tabs[0].url;
    var title = tabs[0].title;
    
    // Log the URL and title to the console (you can replace this with your desired logic)
    console.log('Current URL: ', url);
    console.log('Page Title: ', title);
  });
}

$(document).ready(function(){
  $("#url").text("updated");
  console.log("hello");
  // get_browser_details();
  get_info();
  console.log("goodbye");
});
