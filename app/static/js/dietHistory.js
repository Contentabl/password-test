var data;
$(document).ready(function(){
	$.ajax({
        type: "GET",
       contentType: "application/json",
       dataType: "json",
       url: "/users/dietview",
       }).done(function( msg ) {
               debug = msg;
               data = msg["data"];
               displayData(data);
               });
});

function displayData(data){
  var numUsers = data.length;
  for (var i = 0; i < data.length; i++){
    var user = data[i];
    var name = user["name"];
    var email = user["email"];
    var history = user["history"];
    var numChanges = history.length;
    for (var j = 0; j < numChanges; j++){
      var diets = "";
      var dietHistory = history[j]["diet"];
      var numRestricts = dietHistory.length;
      for (var k = 0; k < numRestricts; k++){
        if (k < numRestricts - 1){
          diets += dietHistory[k] + ", ";
        }
        else{
          diets += dietHistory[k];
        }
      }
      addRow(name, email, diets, history[j]["date"]);
    }
  }
}

function addRow(name, email, restriction, date){
  var newRow = '';
  newRow = '<div class="row"><div class="cell">' + name + '</div><div class="cell">'+email+'</div><div class="cell">'+restriction+'</div>';
  newRow += '<div class="cell">' + date + '</div></div>';
  $(".History").append(newRow);
}