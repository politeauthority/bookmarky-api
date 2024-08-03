document.body.style.border = "5px solid red";
browser.browserAction.onClicked.addListener(handleClick);


function handleClick(){
    console.log("Here's Bookmarky yo!");
}
