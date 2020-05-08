const validImageTypes = ['image/gif', 'image/jpeg', 'image/png'];
let user_email = document.getElementById('user_email');
let top_input = document.getElementById('top_img');
let side_input = document.getElementById('side_img');

let base_url = window.location.origin;
let host = window.location.host;
let pathArray = window.location.pathname.split('/');

let GV_HOST = "http://127.0.0.1:8080";
let mrcnn_data;
let find_retailer_data;
let find_materials_data;
let mrcnn_error;
let gv_req_errors = [];
// 1 - M-RCNN error, 
// 2 - FindRetailer error, 
// 4 - FindMaterials error,
// 0 - No error
// Because there is potential race conditions, the error conditions has to check
// values 1, 2, 3, 4, 5, 6, 7
let error_enum = 0;

$(document).ready(function () {
    $("#btnSubmit").click(function (event) {
        
      //stop submit the form, we will post it manually.
      event.preventDefault();

      // Create an FormData object 
      let mrcnn_in_data = new FormData();
      let gv_in_data_top = new FormData();
      let gv_in_data_side = new FormData();

      // If you want to add an extra field for the FormData
      mrcnn_in_data.append("packager", "DummyBrand");
      mrcnn_in_data.append("email", user_email.value);
      mrcnn_in_data.append("top_img", top_input.files[0]);
      mrcnn_in_data.append("side_img", side_input.files[0]);
      
      gv_in_data_top.append("side_view", side_input.files[0]);
      gv_in_data_side.append("side_view", side_input.files[0]);

      if (!isEmail(user_email.value)){
        $('.alert').hide();
        $("#status").text('Please enter valid email address.');
        toggleAlert();
        return
      }

      if (checkIfImageIsInvalid(top_input.files[0]) || checkIfImageIsInvalid(side_input.files[0])) {
        $('.alert').hide();
        $("#status").text('Please choose valid images. Supported types are: JPEG, PNG, GIF.');
        toggleAlert();
        return
      }
      // disabled the submit button
      $("#btnSubmit").prop("disabled", true);

      // clear previous errors and reset errors
      gv_req_errors.length = 0;
      error_enum = 0;

      // asynchronous calls
      $.when(
        MaskRCNNInfer(mrcnn_in_data), 
        FindRetailer(gv_in_data_side), 
        FindMaterials(gv_in_data_top)).then(
          reqsSuccess, 
          reqsFail);
    });

    $('#top_img').on('change', function () {
      if (checkIfImageIsInvalid(top_input.files[0])) {
        $('.alert').hide();
        $("#status").text('Please choose valid image from the top view. Supported types are: JPEG, PNG, GIF.');
        toggleAlert();
        return
      }
      readURL(this, $(".top-dropzone").attr("id"));
    })
    $('#side_img').on('change', function () {
      if (checkIfImageIsInvalid(side_input.files[0])) {
        $('.alert').hide();
        $("#status").text('Please choose a valid image displaying the logo. Supported types are: JPEG, PNG, GIF.');
        toggleAlert();
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
      let target = $(this.hash);
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

function isEmail(email) {
  let regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}
function checkIfImageIsInvalid(img) {
  if (img === undefined || !validImageTypes.includes(img['type'])) {
    return true;
  }
  return false;
}
// Display image before uploading
// https://stackoverflow.com/questions/4459379/preview-an-image-before-it-is-uploaded
function readURL(input, elem_id) {
  if (input.files && input.files[0]) {
    let reader = new FileReader();
    reader.onload = function (e) {
      $('#' + elem_id).attr('style', 'background: url(' + e.target.result + ');background-repeat:no-repeat;background-size:cover;color:#fff;background-attachment:scroll;background-position:center;');
    }

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}

function toggleAlert() {
  $(".alert").toggle('show');
}

function MaskRCNNInfer(data) {
  return $.ajax({
    type: "POST",
    enctype: 'multipart/form-data',
    url: "/api/upload",
    data: data,
    processData: false,
    contentType: false,
    cache: false,
    crossDomain: true,
    // timeout: 600000,
    beforeSend: function (data) {
      $(".alert").hide();
      $("#imageUploadForm").attr("style", "display:none;");
      $("#res_img").attr("style", "max-height:300px;");
      $("#res_img").attr("src", "/static/css/images/loading.gif");
    },
    success: function (data) {
      mrcnn_data = data;
    },
    error: function (e) {
      // $("#status").text(JSON.parse(e.responseText).response);
      mrcnn_error = JSON.parse(e.responseText);
      error_enum += 1;
    }
  });
}

function FindRetailer(data) {
  return $.ajax({
    type: "POST",
    enctype: 'multipart/form-data',
    url: GV_HOST+"/find_retailer",
    data: data,
    processData: false,
    contentType: false,
    cache: false,
    crossDomain: true,
    "headers": {
      "Access-Control-Allow-Origin": "*"
    },
    success: function (data) {
      find_retailer_data = data;
    },
    error: function (e) {
      gv_req_errors.push(e.responseText);
      error_enum += 2;
    }
  });
}

function FindMaterials(data) {
  return $.ajax({
    type: "POST",
    enctype: 'multipart/form-data',
    url: GV_HOST + "/find_materials",
    data: data,
    processData: false,
    contentType: false,
    cache: false,
    crossDomain: true,
    "headers": {
      "Access-Control-Allow-Origin": "*"
    },
    success: function (data) {
      find_materials_data = data;
    },
    error: function (e) {
      gv_req_errors.push(e.responseText);
      error_enum += 3;
    }
  });
}

function reqsSuccess(){
  post_id = mrcnn_data.response.post_id;
  plastic = find_materials_data.has_plastic ? 0 : 1;
  cardboard = find_materials_data.has_cardboard ? 0 : 1;
  paper = find_materials_data.has_paper ? 0 : 0.5;
  paperboard = find_materials_data.has_paperboard ? 0 : 0.5;
  outer = mrcnn_data.response.outer_size;
  inner = mrcnn_data.response.inner_size != null ? mrcnn_data.response.inner_size : 1;
  item = mrcnn_data.response.item_size != null ? mrcnn_data.response.item_size : 0.01;

  // alert(outer + " | " + inner + " | " + item + " | " + plastic + " | " + cardboard + " | " + paper + " | " + paperboard);
  // alert((item / inner).toPrecision(10) + " | " + (item / outer).toPrecision(10));
  // alert(5 * (item / inner).toPrecision(10) + " | " + 2 * (item / outer).toPrecision(10));

  score = 5 * (item / inner).toPrecision(10) + 2 * (item / outer).toPrecision(10) + plastic + cardboard + paper + paperboard;
  let update_form = new FormData();
  update_form.append("post_id", post_id);
  update_form.append("packager", find_retailer_data.retailer);
  update_form.append("materials", JSON.stringify(find_materials_data));
  update_form.append("score", score);

  $.ajax({
    type: "PUT",
    enctype: 'multipart/form-data',
    url: "/api/update",
    data: update_form,
    processData: false,
    contentType: false,
    cache: false,
    success: function (data) {
      email_val = user_email.value;
      localStorage.setItem("user_email", email_val);
      window.location.href = base_url+ "/feed/" + post_id + "/";
    },
    error: function (e) {
      pred_req_errors.push(e.responseText);
    }
  });
}

function reqsFail(errors) {
  let respText;
  if(error_enum % 2 == 1){
    respText = mrcnn_error.response;
  } else if (error_enum == 2 || error_enum == 6){
    respText = "Unable to find the retailer. Please try again.";
  } else {
    respText = "Unable to detect plastics, carboard and other materials. Please try again.";
  }
  $("#status").text(respText);
  toggleAlert();
  $("#btnSubmit").prop("disabled", false);
  $("#res_img").attr("src", "");
  $("#res_img").attr("style", "max-height:0px;");
  $("#imageUploadForm").attr("style", "display:block;");
  // $('#top-dropzone').attr('style', 'background:url(/static/img/sample_top.png) top left no-repeat;background-size:cover;');
  // $('#side-dropzone').attr('style', 'background:url(/static/img/sample_side.png) top left no-repeat;background-size:cover;');
}