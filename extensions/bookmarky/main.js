//
// Main
//

console.log("yo");

// Stage Envs
// var API_URL = "http://api.bookmarky-stage.colfax.int/info";
// var TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpudWxsLCJyb2xlX3Blcm1zIjpbXSwib3JnX2lkIjpudWxsLCJpYXQiOjE3MjI1NTE5MDEsImV4cCI6MTcyMjcyNDcwMX0.9-iQ9-FvEXtdOgPhXUEkne0tXf_21yigNWpHV26XRPM";
// var API_KEY = "";
// var CLIENT_ID = "";

// Dev Envs
var API_URL = "http://api.bookmarky-dev.colfax.int/info";
var TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlX3Blcm1zIjpbIndyaXRlLWFsbCIsInJlYWQtYWxsIiwiZGVsZXRlLWFsbCJdLCJvcmdfaWQiOjEsImlhdCI6MTcyMjU1MTgxMSwiZXhwIjoxNzIyNTU1NDExfQ.HjqYzInv72WmmB7ZJ13kwu__b_QsYSBUtMPuZAHWK1c";
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
  get_browser_details();
});
