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

$(document).ready(function(){
  $(".hello").text("updated");
  console.log($(".hello"));
  console.log("hello");
});

var data = {
  "name": "test",
  "url": "https://www.google.com/"
}



function get_info(){
    $.ajax({
        type: "POST",
        url: API_URL,
        headers: {
            "Token": TOKEN
        },
        //   data: data,
        success: success,
        dataType: "json"
        });
}


function success(){
    console.log("succeeded");
}

get_info();