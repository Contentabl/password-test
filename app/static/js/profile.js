/**
 * Created by Amanpreet on 12/31/14.
 */

var orderButton;
var allDays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
var daysList = ['mondayList', 'tuesdayList', 'wednesdayList', 'thursdayList', 'fridayList', 'saturdayList', 'sundayList'];
var mealsList = ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Dessert'];
var userInfo;
var orderInfo;
var nameBox;
var emailBox;
var phoneBox;
var streetBox;
var stateBox;
var zipBox;
var dietOptions;

$(window).load(function(){
    nameBox = $(".nameBox");
    emailBox = $(".emailBox");
    phoneBox = $(".phoneBox");
    streetBox = $(".streetBox");
    stateBox = $(".stateBox");
    zipBox = $(".zipBox");
    // get user info
    $.ajax({
        type: "GET",
       contentType: "application/json",
       dataType: "json",
       url: "/users/info/ ",
       }).done(function( msg ) {
               debug = msg;
               userInfo = msg;
               var info = msg["info"];
               nameBox.attr("placeholder", info["name"]);
               $(".name _placeHolder").html(info["name"]);
               if (info["name"] != null && info["name"] != "")
                    $(".name _placeHolder").html(info["name"]);
               if (info["email"] != null && info["email"] != "")
                    $(".email _placeHolder").html(info["email"]); 
               if (info["phone"] != null && info["phone"] != "")
                    $(".email _placeHolder").html(info["phone"]);
                var address = info["address"].split(",");
                if (address.length == 3){
                    $(".street _placeHolder").html(address[0]);
                    $(".state _placeHolder").html(address[1]);
                    $(".zip _placeHolder").html(address[2]);
                }
               //console.log(msg)
               });

    // get order info
    $.ajax({
        type: "GET",
       contentType: "application/json",
       dataType: "json",
       url: "/users/orderinfo/ ",
       }).done(function( msg ) {
               debug = msg;
               orderInfo = msg["data"];
               var numDays = allDays.length;
               var numMeals = mealsList.length;

               for (var i = 0; i < numDays; i++){
                    for (var j = 0; j < numMeals; j++){
                        if (orderInfo[allDays[i]][j]){
                            $("." + allDays[i] + " ." + mealsList[j]).prop("checked", true);
                        }
                    }
               }
               var numPeople = msg["num_people"];
               //console.log(numPeople);
               if (numPeople == 0 || numPeople == null)
                    $(".num1").prop("checked", true);
               else
                    $(".num" + numPeople).prop("checked", true);

               //console.log(msg)
               });
    
});

$(document).ready(function(){
    
});

function topOrderClicked(){
    $(".page").hide();
    $(".topLevel").show();
}
function profileClicked(){
    $(".page").show();
    $(".topLevel").hide();
}

function customSelect(){
    $("#customOptionBtn").prop("checked", true);
}
function full(){
    var meals = ['Breakfast', 'Lunch', 'Dinner', 'Snacks'];
    clearList();
    selectLoop(daysList, meals, true);

}
function seven(){
    var meals = ['Breakfast', 'Lunch', 'Dinner'];
    clearList();
    selectLoop(daysList, meals, true);
}
function five(){
    var meals = ['Breakfast', 'Lunch', 'Dinner', 'Snacks'];
    var days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
    clearList();
    selectLoop(days, meals, true);
}
function fiveNoS(){
    var meals = ['Breakfast', 'Lunch', 'Dinner'];
    var days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
    clearList();
    selectLoop(days, meals, true);
}
function fiveNoB(){
    var meals = ['Lunch', 'Dinner'];
    var days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
    clearList();
    selectLoop(days, meals, true);
}
function fiveOnlyD(){
    var meals = ['Dinner'];
    var days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
    clearList();
    selectLoop(days, meals, true);
}
function three(){
    var meals = ['Dinner'];
    var days = ['Monday', 'Wednesday', 'Friday'];
    clearList();
    selectLoop(days, meals, true);
}
function selectLoop(days, meals, state){
    numDays = days.length;
    numMeals = meals.length;
    for (var i = 0; i < numDays; i++){
        for (var j = 0; j < numMeals; j++){
            var selector = "." + days[i] + " ." + meals[j];
            $(selector).prop( "checked", state);
        }
    }
}
function clearList(){
    selectLoop(daysList, mealsList, false);
}
function submitOrders(){
    numDays = daysList.length;
    numMeals = mealsList.length;
    var days = allDays;
    result = {};
    for (var i = 0; i < numDays; i++){
        result[days[i]] = new Array();
        for (var j = 0; j < numMeals; j++){
            if ($('.' + daysList[i] + ' input[class="' + mealsList[j] + ' mealOption"]:checked').length > 0){
                result[days[i]].push(true);
            }
            else{
                result[days[i]].push(false);
            }
        }
    }
    result['numPeople'] = new Array();
    result['numPeople'].push($('input[name=numPeople]:checked').val());
    console.log("submit");
    console.log(result)
    $.ajax({
        type: "POST",
       contentType: "application/json",
       dataType: "json",
       url: "/users/order/",
       data: JSON.stringify({order: result})
       }).done(function( msg ) {
               debug = msg;
               console.log(msg)
               });

}
function updateProfile(){

    var street = streetBox.val();
    var state = stateBox.val();
    var zip = zipBox.val(); 
    var notes = $(".notesBox").val();   
    var name = nameBox.val();
    var email = emailBox.val();
    var phone = phoneBox.val();

    var address = street + ", " + state + ", " + zip;
    var data = {};

    if (name != "")
        data["name"] = name;
    if (email != "")
        data["email"] = email;
    if (phone != "")
        data["phone"] = phone;
    if (street != "" && state != "" && zip != "")
        data["address"] = address;

    $.ajax({
        type: "POST",
       contentType: "application/json",
       dataType: "json",
       url: "/users/profile/update/",
       data: JSON.stringify(data)
       }).done(function( msg ) {
               debug = msg;
               console.log(msg)
               });

    var diets = Array();
    $("input[name=option1]:checked").each(function() {
        var diet = $(this).val();
        diets.push(diet);
    });
    console.log(diets);
    $.ajax({
        type: "POST",
       contentType: "application/json",
       dataType: "json",
       url: "/users/diet/update/",
       data: JSON.stringify({diet: diets})
       }).done(function( msg ) {
               debug = msg;
               console.log(msg)
               });
    
}