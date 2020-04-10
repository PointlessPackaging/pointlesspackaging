// Send GET XMLHTTPRequest()
// const xhr = new XMLHttpRequest();
// xhr.open('GET', 'http://127.0.0.1:8000/api/display_feed?page=1');
// xhr.send();
var display_page_num = 1
var display_page_count = 1

window.addEventListener("load", function () {
    function sendData() {
        const XHR = new XMLHttpRequest();

        // Bind the FormData object and the form element
        const FD = new FormData(form);

        // Define what happens on successful data submission
        XHR.addEventListener("load", function (event) {
            console.log(display_page_count)
            var result = JSON.parse(event.target.response)
            display_page_num = result.count;
            display_page_count++;
            if (display_page_count > display_page_num){
                display_page_count = 1;
            }
            document.getElementById('image_obj_top').src = result.results[0].top_img;
            document.getElementById('image_obj_side').src = result.results[0].side_img;
        });

        // Define what happens in case of error
        XHR.addEventListener("error", function (event) {
            alert('Oops! Something went wrong.');
        });

        // Set up our request
        XHR.open("GET", "http://127.0.0.1:8000/api/display_feed?page=" + display_page_count);

        // The data sent is what the user provided in the form
        XHR.send(FD);
    }

    // Access the form element...
    let form = document.getElementById("display_feed_form");

    // ...and take over its submit event.
    form.addEventListener("submit", function (event) {
        event.preventDefault();

        sendData();
    });
});