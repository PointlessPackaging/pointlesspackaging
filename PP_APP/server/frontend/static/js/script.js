function isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

$(document).ready(function () {
	$("#btnSubmit").click(function (event) {

<<<<<<< HEAD
		//stop submit the form, we will post it manually.
		event.preventDefault();
=======
        // var dumb_ob = JSON.parse('{ "response": { "img_post_id": 23, "packager": "DummyBrand", "infer_img": "/media/infer/Image_from_iOS.jpg", "outer_size": 30344, "inner_size": 11739, "item_size": null }}')
        // alert(dumb_ob.response.infer_img)
        // Get form
        var form = $('#fileUploadForm')[0];
>>>>>>> 68370ef... - Reorganized models and improved their naming schemes.

		// var dumb_ob = JSON.parse('{ "response": { "img_post_id": 23, "packager": "DummyBrand", "infer_img": "/media/infer/Image_from_iOS.jpg", "outerbox": 30344, "innerbox": 11739, "item": null }}')
		// alert(dumb_ob.response.infer_img)
		// Get form
		var form = $('#fileUploadForm')[0];

<<<<<<< HEAD
		// Create an FormData object
		var data = new FormData();
=======
        var user_email = document.getElementById('user_email');
        var top_input = document.getElementById('top_img');
        var side_input = document.getElementById('side_img');
        // If you want to add an extra field for the FormData
        data.append("packager", "DummyBrand");
        data.append("email", user_email.value);
        data.append("top_img", top_input.files[0]);
        data.append("side_img", side_input.files[0]);

        if (!isEmail(user_email.value)){
            $("#status").text('Please enter valid email address.');
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
                document.getElementById("imageUploadForm").reset();
                $('#top_img').next('.custom-file-label').html("Choose file...");
                $('#side_img').next('.custom-file-label').html("Choose file...");
>>>>>>> 68370ef... - Reorganized models and improved their naming schemes.

		var top_input = document.getElementById('top_img');
		var side_input = document.getElementById('side_img');
		// If you want to add an extra field for the FormData
		data.append("packager", "DummyBrand");
		data.append("top_img", top_input.files[0]);
		data.append("side_img", side_input.files[0]);
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
				$("#outerbox").text("");
				$("#innerbox").text("");
				$("#item").text("");
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
				$("#outerbox").text(data.response.outerbox)
				$("#innerbox").text(data.response.innerbox)
				$("#item").text(data.response.item)
				let elapsed = Math.floor(((new Date().getTime() - now) % (1000 * 60)) / 1000)
				$("#time_elapsed").text(elapsed)
				document.getElementById("imageUploadForm").reset();
				$('#top_img').next('.custom-file-label').html("Choose file...");
				$('#side_img').next('.custom-file-label').html("Choose file...");

			},
			error: function (e) {
				// $("#status").text(e.responseText);
				$("#status").text('Please try again.');
				console.log("ERROR : ", e);
				$("#btnSubmit").prop("disabled", false);
				$("#res_img").attr("src", "")

			}
		});
	});

	$('#top_img').on('change', function () {
		//get the file name
		var fileName = $(this).val();
		//replace the "Choose a file" label
		$(this).next('.custom-file-label').html(fileName.split(/(\\|\/)/g).pop());
	})
	$('#side_img').on('change', function () {
		//get the file name
		var fileName = $(this).val();
		//replace the "Choose a file" label
		$(this).next('.custom-file-label').html(fileName.split(/(\\|\/)/g).pop());
	})
});