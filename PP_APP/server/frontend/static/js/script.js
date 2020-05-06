const validImageTypes = ['image/gif', 'image/jpeg', 'image/png'];
let user_email = document.getElementById('user_email');
let top_input = document.getElementById('top_img');
let side_input = document.getElementById('side_img');

function isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}
function checkIfImageIsInvalid(img){
  if (img === undefined || !validImageTypes.includes(img['type'])) {
    return true;
  }
  return false;
}
// Display image before uploading
// https://stackoverflow.com/questions/4459379/preview-an-image-before-it-is-uploaded
function readURL(input, elem_id) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $('#' + elem_id).attr('style', 'background-image: url(' + e.target.result + ');background-repeat:no-repeat;background-size:cover;color:#fff;background-attachment:scroll;background-position:center;');
    }

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}
$(document).ready(function () {
    $("#btnSubmit").click(function (event) {

        //stop submit the form, we will post it manually.
        event.preventDefault();

        // Get form
        var form = $('#fileUploadForm')[0];

        // Create an FormData object
        var data = new FormData();

        // If you want to add an extra field for the FormData
        data.append("packager", "DummyBrand");
        data.append("email", user_email.value);
        data.append("top_img", top_input.files[0]);
        data.append("side_img", side_input.files[0]);

        if (!isEmail(user_email.value)){
            $("#status").text('Please enter valid email address.');
            return
        }

        if (checkIfImageIsInvalid(top_input.files[0]) || checkIfImageIsInvalid(side_input.files[0])) {
          $("#status").text('Please choose valid images. Supported types are: JPEG, PNG, GIF.');
          return
        }
        // disabled the submit button
        $("#btnSubmit").prop("disabled", true);
        let now = 0
        $.ajax({
            type: "POST",
            enctype: 'multipart/form-data',
            url: "/api/upload",
            data: data,
            processData: false,
            contentType: false,
            cache: false,
            // timeout: 600000,
            beforeSend: function (data) {
                $("#status").text('Inferring...Please wait.');
                $("#res_img").attr("src", "/static/css/images/loading.gif")
                $("#post_infer").css("display", "none")
                $("#outer_size").text("");
                $("#inner_size").text("");
                $("#item_size").text("");
                $("#time_elapsed").text("")
                now = new Date().getTime();
            },
            success: function (data) {
                $("#status").text("");
                console.log("SUCCESS : ", data);
                $("#btnSubmit").prop("disabled", false);
                $("#res_img").attr("src", data.response.infer_img)
                $("#post_infer").css("display", "block")
                $("#score").text('6.5/10')
                $("#outer_size").text(data.response.outer_size)
                $("#inner_size").text(data.response.inner_size)
                $("#item_size").text(data.response.item_size)
                let elapsed = Math.floor(((new Date().getTime() - now) % (1000 * 60)) / 1000)
                $("#time_elapsed").text(elapsed)
                email_val = user_email.value
                // store EMAIL locally so the user doesn't to retype in the email on refresh
                localStorage.setItem("user_email", email_val);
                document.getElementById("imageUploadForm").reset();
                user_email.setAttribute('value', email_val);


                $('#top-dropzone').attr('style', 'background:linear-gradient(to bottom, rgba(22, 22, 22, 0.5) 0%, rgba(22, 22, 22, 0.8) 80%, #0000008a 100%), url(/static/img/sample_top.jpg) top left no-repeat;background-size:cover;');
                $('#side-dropzone').attr('style', 'background:linear-gradient(to bottom, rgba(22, 22, 22, 0.5) 0%, rgba(22, 22, 22, 0.8) 80%, #0000008a 100%), url(/static/img/sample_side.jpg) top left no-repeat;background-size:cover;');

            },
            error: function (e) {
              $("#status").text(JSON.parse(e.responseText).response);
                // $("#status").text('Please try again.');
                $("#btnSubmit").prop("disabled", false);
                $("#res_img").attr("src", "")
                email_val = user_email.value
                localStorage.setItem("user_email", email_val);
                document.getElementById("imageUploadForm").reset();
                user_email.setAttribute('value', email_val)
                $('#top-dropzone').attr('style', 'background:linear-gradient(to bottom, rgba(22, 22, 22, 0.5) 0%, rgba(22, 22, 22, 0.8) 80%, #0000008a 100%), url(/static/img/sample_top.jpg) top left no-repeat;background-size:cover;');
                $('#side-dropzone').attr('style', 'background:linear-gradient(to bottom, rgba(22, 22, 22, 0.5) 0%, rgba(22, 22, 22, 0.8) 80%, #0000008a 100%), url(/static/img/sample_side.jpg) top left no-repeat;background-size:cover;');
            }
        });

    });

    $('#top_img').on('change', function () {
      if (checkIfImageIsInvalid(top_input.files[0])) {
        $("#status").text('Please choose valid images. Supported types are: JPEG, PNG, GIF.');
        return
      }
      readURL(this, $(".top-dropzone").attr("id"));
    })
    $('#side_img').on('change', function () {
      if (checkIfImageIsInvalid(side_input.files[0])) {
        $("#status").text('Please choose valid images. Supported types are: JPEG, PNG, GIF.');
        return
      }
      readURL(this, $(".side-dropzone").attr("id"));
    })

});

// NEW THEME UPDATES BELOW

what_page = document.getElementById("page_name").value;
(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 70)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 100
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
      $("#mainNav").addClass("mainNav-bg");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
      $("#mainNav").removeClass("mainNav-bg");
    }
  };
  // Collapse now if page is not at top
  if (what_page == 'home'){
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);
  }
  if (what_page=='rate'){
    $("#user_email").val(localStorage.getItem("user_email"));
  }

})(jQuery); // End of use strict
