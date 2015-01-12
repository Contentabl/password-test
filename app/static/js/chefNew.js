var data;
var dietHeader = "row header blue";
var userHeader = "row header orange";

$(document).ready(function(){
	$.ajax({
       type: "GET",
       contentType: "application/json",
       dataType: "json",
       url: "/users/chefdata",
       }).done(function( msg ) {
               debug = msg;
               data = msg['data'];
               loadSelections();
               });
    $(".userSelect").on('change', function() {
    	loadUser(parseInt($(this).val()));
	});
});

function loadSelections(){
	var numUsers = data.length;
	for (var i = 0; i < numUsers; i++){
		$(".userSelect").append($("<option></option>")
	         .attr("value",i)
	         .text(data[i]["name"]));
	}
	loadUser(0);
}

function loadUser(userIndex){
	clearRows();
	var user = data[userIndex];
	var restrictions = user["dietary_restrictions"];
	var diet = "";
	var numR = restrictions.length;
	for (var i = 0; i < numR; i++){
		if (i == numR - 1){
			diet += restrictions[i];
		}
		else{
			diet += restrictions[i] + ", ";
		}
	}
	addUserInfo(user["name"], user["num_people"], diet, user["notes"], user["email"], user["phone"], user["address"]);

	loadMeals(userIndex);
}

function loadMeals(userIndex){
	var user = data[userIndex];
	var daysList = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
	var meals = ["Breakfast", "Lunch", "Dinner", "Snacks", "Dessert"];
	var numMeals = meals.length;
	var numDays = 7;
	for (var i = 0; i < numMeals; i++){
		var curMeal = Array();
		curMeal["name"] = meals[i];
		for (var j = 0; j < numDays; j++){
			curMeal[j] = user[daysList[j]][i];
		}
		addMealsRow(curMeal);
	}
}

function addMealsRow(mealInfo){
	var row = '<div class="row"><div class="cell">'+mealInfo["name"]+'</div>';
	var numDays = mealInfo.length;
	for (var i = 0; i < numDays; i++){
		row += getCell(mealInfo[i]);
	}
	row += '</div';
	$(".dietInfo").append(row);
}

function getCell(selected){
	var style = "";
	if (selected){
		style = 'style=background-color:green';
	}
	else{
		style = 'style=background-color:red'
	}
	return '<div class="cell" ' + style + ' ></div>'
}

function clearRows(){
	$(".dietInfo").empty();
	var header = '<div class="'+dietHeader+'"><div class="cell"></div><div class="cell">Sunday</div><div class="cell">Monday</div><div class="cell">Tuesday</div>';
	header += '<div class="cell">Wednesday</div><div class="cell">Thursday</div><div class="cell">Friday</div><div class="cell">Saturday</div></div>';
	$(".dietInfo").append(header);

	$(".userInfo").empty();
	var header = '<div class="'+userHeader+'"><div class="cell">Name</div><div class="cell">Number of People Served</div><div class="cell">Dietary Restrictions</div>';
	header += '<div class="cell">Notes</div><div class="cell">Email Address</div><div class="cell">Phone Number</div><div class="cell">Address</div></div>';
	$(".userInfo").append(header);
}

function addUserInfo(name, number, diet, notes, email, phone, address){
	var newRow = '';
	newRow = '<div class="row"><div class="cell">' + name + '</div><div class="cell">'+number+'</div><div class="cell">'+diet+'</div>';
	newRow += '<div class="cell">' + notes + '</div><div class="cell">' + email + '</div><div class="cell">' + phone + '</div>';
	newRow += '<div class="cell">' + address+ '</div></div>';
	$(".userInfo").append(newRow);
}