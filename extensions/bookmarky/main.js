//
// Main
//

console.log("Starting Main");

// Stage Envs
// var API_URL = "http://api.bookmarky-stage.colfax.int";
// var TOKEN = "";
// var API_KEY = "";
// var CLIENT_ID = "";

// Dev Envs
var API_URL = "http://api.bookmarky-dev.alix.lol";
var API_KEY = "";
var CLIENT_ID = "";


function fetch_new_token(){
  $.ajax({
    type: "POST",
    url: API_URL + "/auth",
    headers: {
        "X-Api-Key": API_KEY,
        "Client-Id": CLIENT_ID,
        "Content-Type": "application/json"
    },
    success: succes_login,
    dataType: "json"
    });
}
function succes_login(data){
  console.log("succesfully got a new token!");
  console.log(data.token);
  $("#result").text(data.token);
  storeToken(data.token)
}


function storeToken(token) {
  browser.storage.local.set({ 'token': token })
      .then(() => {
          console.log('Token stored successfully');
      })
      .catch(error => {
          console.error('Error storing token:', error);
      });
}

function getToken() {
  return browser.storage.local.get('token')
      .then(result => {
          console.log("Got Token from Storage!" + result.token)
          return result.token;
      })
      .catch(error => {
          console.error('Error retrieving token:', error);
          return null;
      });
}




function add_boomark(token, url, name){

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
        "Token": token,
        "Content-Type": "application/json"
    },
      data: JSON.stringify(data),
    success: success,
    dataType: "json"
    });
}

function success(data){
  console.log("success!");
  $("#url").text("updated");
  console.log(data);
  console.log(data.object.url);
  $("#name").text(data.object.name);
  $("#url").text(data.object.url);

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
  fetch_new_token();
  getToken()
  .then(token => {
      if (token) {
          console.log('Retrieved token from storage:', token);
          getCurrentTabInfo().then(({ url, title }) => {
            // Log the URL and title to the console
            console.log("Current URL: ", url);
            console.log("Page Title: ", title);
            add_boomark(token, url, title);
            // Now you can use the 'url' and 'title' variables for further processing in your plugin logic
          }).catch((error) => {
              console.error("Error getting current tab info:", error);
          });
        
          // Use the token for further operations
      } else {
          console.log('Token not found in storage');
      }
  });

  // get_browser_details();
  // console.log(url);

  console.log("goodbye");
});
