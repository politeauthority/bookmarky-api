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
var API_URL = "http://api.bookmarky-dev.alix.lol";
var TOKEN = "";
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


function add_boomark(url, name){
  browser.tabs.query({active: true, currentWindow: true}, (tabs) => {
    // Get the URL and title of the current active tab
    var url = tabs[0].url;
    var title = tabs[0].title;

    // Log the URL and title to the console (you can replace this with your desired logic)
    console.log('Current URL: ', url);
    console.log('Page Title: ', title);
  });
  var data = {
    "url": url,
    "name": name
  }
  $.ajax({
    type: "POST",
    url: API_URL + "/bookmark",
    headers: {
        "Token": TOKEN,
        "Content-Type": "application/json"
    },
      data: JSON.stringify(data),
    success: success,
    dataType: "json"
    });
}

function success(data){
  console.log("success!");
  console.log(data);
}


function getCurrentTabInfo() {
  return new Promise((resolve, reject) => {
      // Get the currently active tab
      browser.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          // Get the URL and title of the current active tab
          const url = tabs[0].url;
          const title = tabs[0].title;
          
          // Resolve the Promise with the URL and title
          resolve({ url, title });
      });
  });
}

$(document).ready(function(){
  $("#url").text("updated");
  console.log("hello");

  getCurrentTabInfo().then(({ url, title }) => {
    // Log the URL and title to the console
    console.log("Current URL: ", url);
    console.log("Page Title: ", title);
    add_boomark(url, title);
    // Now you can use the 'url' and 'title' variables for further processing in your plugin logic
  }).catch((error) => {
      console.error("Error getting current tab info:", error);
  });


  // get_browser_details();
  console.log(url);
  console.log("goodbye");
});
