const submitBtn = document.getElementById('submitBtn');

function submitClicked(){
  //alert("Registered a click!");
  //alert("Hello1");
  var formData = new FormData();
  var form_file = document.getElementById('file');
  formData.append('side_view', form_file.files[0]);

  $.ajax({
         url : '/find_retailer',
         type : 'POST',
         data : formData,
         processData: false,  // tell jQuery not to process the data
         contentType: false,  // tell jQuery not to set contentType
         beforeSend: function(data) {
           $("#retailer_name").text("Looking for retailer...")
         },
         success : function(data) {
             console.log(data);
             //alert(data.retailer);
             $("#retailer_name").text(data.retailer)

         },
         error:function(e){
           console.log(`${e}`)
         }
  });
}

submitBtn.addEventListener('click', submitClicked);
