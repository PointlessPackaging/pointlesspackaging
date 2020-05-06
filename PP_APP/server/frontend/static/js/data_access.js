/*
 * Function creates table from data sent to it
*/
function createTable(data) {
  var table = '';
  $.each(data, function(idx, elem) {
    table += "<tr><td>" + (idx + 1) + "</td> <td>" + elem.brand_name + "</td> <td>" + elem.score + "</td></tr>";
  });

  return table;
}

$(document).ready(function() {
  jQuery.support.cors = true;

  $.ajax({
         url : "/api/best_five",
         type : "GET",
         data : "{}",
         contentType: "application/json; charset=utf-8",
         dataType: "json",
         cache: "false",

         success : function(data) {
            var table = createTable(data);
            $("#topFiveTable").append(table);
         },

         error:function(e){
           console.log(`${e}`)
         }
  });

  $.ajax({
         url : "/api/worst_five",
         type : "GET",
         data : "{}",
         contentType: "application/json; charset=utf-8",
         dataType: "json",
         cache: "false",

         success : function(data) {
            var table = createTable(data);
            $("#bottomFiveTable").append(table);
         },

         error:function(e){
           console.log(`${e}`)
         }
    });
});
