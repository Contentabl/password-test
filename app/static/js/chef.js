var data;
var rowHeaders = {"Breakfast" : "row header", "Lunch" : "row header green", "Dinner" : "row header blue", "Dessert": "row header yellow","Snacks" : "row header purple"};

$(document).ready(function(){
	$.ajax({
       type: "GET",
       contentType: "application/json",
       dataType: "json",
       url: "/users/chefpage",
       }).done(function( msg ) {
               debug = msg;
               data = msg['data'];
               //console.log(data);
               loadDay("Sunday");
               });
    $(".Week").on('change', function() {
    	loadDay($(this).val());
	});
});

function loadDay(day){
	var currentData = data[day];
	//console.log(currentData);
	var meals = Object.keys(currentData);
	var numMeals = meals.length;
	for (var i = 0; i < numMeals; i++){
		var curMeal = meals[i];
		clearRows(curMeal);
		var curMealData = currentData[curMeal];
		var total = curMealData.length;
		for (var j = 0; j < total; j++){
			var user = curMealData[j]['user'];
			var notes = curMealData[j]['notes'];
			var name = user['name'];
			var number = curMealData[j]['num_people'];
			var diet = user['dietary_restrictions'].join(', ');
			var email = user['email'];
			var phone = user['phone'];
			var address = user['address'];
			addRow(curMeal, name, number, diet, notes, email, phone, address);
		}
	}
}

function clearRows(meal){
	$("." + meal).empty();
	var header = '"<div class="'+rowHeaders[meal]+'"><div class="cell">Name</div><div class="cell">Number of People Served</div><div class="cell">Dietary Restrictions</div>';
	header += '<div class="cell">Notes</div><div class="cell">Email Address</div><div class="cell">Phone Number</div><div class="cell">Address</div></div>';
	$("." + meal).append(header);
}

function addRow(meal, name, number, diet, notes, email, phone, address){
	var newRow = '';
	newRow = '<div class="row"><div class="cell">' + name + '</div><div class="cell">'+number+'</div><div class="cell">'+diet+'</div>';
	newRow += '<div class="cell">' + notes + '</div><div class="cell">' + email + '</div><div class="cell">' + phone + '</div>';
	newRow += '<div class="cell">' + address+ '</div></div>';
	$("." + meal).append(newRow);
}