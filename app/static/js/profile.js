/**
 * Created by Amanpreet on 12/31/14.
 */

var orderButton;
var allDays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
var allDaysIndexed = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
var daysList = ['mondayList', 'tuesdayList', 'wednesdayList', 'thursdayList', 'fridayList', 'saturdayList', 'sundayList'];
var mealsList = ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Dessert'];
var noAddress;
var street;
var zip;
var state;
var userInfo;
var orderInfo;
var nameBox;
var emailBox;
var phoneBox;
var streetBox;
var stateBox;
var zipBox;
var notesBox;
var dietOptions;

$(window).load(function(){
    nameBox = $(".nameBox");
    emailBox = $(".emailBox");
    phoneBox = $(".phoneBox");
    streetBox = $(".streetBox");
    stateBox = $(".stateBox");
    zipBox = $(".zipBox");
    notesBox = $(".notesBox");
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
                setBoxes(info);
                var diets = info['dietary_restrictions'];
                selectDietRestrictions(diets);

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

function selectDietRestrictions(diets){
    var numDiets = diets.length;
    for(var i = 0; i < numDiets; i++){
        $("." + diets[i]).prop("checked", true);
    }
}
function setBoxes(info){
    if (info["name"] != null && info["name"] != ""){
        nameBox.attr("value", info["name"]);
        nameBox.attr("style", "background-color: #D3D3D3");
        nameBox.attr("placeholder", "Name");
        nameBox.keyup(function () {
            nameBox.attr("style", "background-color: #FFFFFF"); 
        });
    }
    else
        nameBox.attr("placeholder", "Name");
   if (info["email"] != null && info["email"] != ""){
        emailBox.attr("value", info["email"]); 
        emailBox.attr("style", "background-color: #D3D3D3");
        emailBox.attr("placeholder", "Email Address");
        emailBox.keyup(function () {
            emailBox.attr("style", "background-color: #FFFFFF"); 
        });
    }
    else
        emailBox.attr("placeholder", "Email Address");
   if (info["phone"] != null && info["phone"] != ""){
        phoneBox.attr("value", info["phone"]);
        phoneBox.attr("style", "background-color: #D3D3D3");
        phoneBox.attr("placeholder", "Phone Number");
        phoneBox.keyup(function () {
            phoneBox.attr("style", "background-color: #FFFFFF"); 
        });
    }
    else
        phoneBox.attr("placeholder", "Phone Number");

    var address = info["address"].split(", ");
    if (address.length == 3){
        streetBox.attr("value", address[0]);
        stateBox.attr("value", address[1]);
        zipBox.attr("value", address[2]);
        street = address[0];
        state = address[1];
        zip = address[2];
        streetBox.attr("placeholder", "Street Address");
        stateBox.attr("placeholder", "City and State");
        zipBox.attr("placeholder", "Zip Code");
        streetBox.attr("style", "background-color: #D3D3D3");
        stateBox.attr("style", "background-color: #D3D3D3");
        zipBox.attr("style", "background-color: #D3D3D3");
        streetBox.keyup(function () {
            streetBox.attr("style", "background-color: #FFFFFF"); 
        });
        stateBox.keyup(function () {
            stateBox.attr("style", "background-color: #FFFFFF"); 
        });
        zipBox.keyup(function () {
            zipBox.attr("style", "background-color: #FFFFFF"); 
        });
        noAddress = false;
    }
    else{
        noAddress = true;
        streetBox.attr("placeholder", "Street Address");
        stateBox.attr("placeholder", "City and State");
        zipBox.attr("placeholder", "Zip Code");
    }

    var notes = info['notes'];
    if (notes != null && notes != ""){
        notesBox.attr("value", notes);
        notesBox.attr("style", "background-color: #D3D3D3");
        notesBox.attr("placeHolder", "Additional Comments:");
        notesBox.keyup(function () {
            notesBox.attr("style", "background-color: #FFFFFF"); 
        });
    }
    else{
        notesBox.attr("placeHolder", "Additional Comments:");
    }
}
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
    var days = allDaysIndexed;
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
    //console.log("submit");
    //console.log(result)
    $.ajax({
        type: "POST",
       contentType: "application/json",
       dataType: "json",
       url: "/users/order/",
       data: JSON.stringify({order: result})
       }).done(function( msg ) {
               if (msg['status'] == 2){
                    alert(msg['message']); 
                }

               
               });

}
function updateProfile(){

    var newStreet = streetBox.val();
    var newState = stateBox.val();
    var newZip = zipBox.val(); 
    var notes = notesBox.val();
    var name = nameBox.val();
    var email = emailBox.val();
    var phone = phoneBox.val();
    var data = {};

    if (name != "")
        data["name"] = name;
    if (email != "")
        data["email"] = email;
    if (phone != "")
        data["phone"] = phone;
    if ((newStreet == "" || newState == "" || newZip == "") && noAddress == true){
        alert("Please fill in all address fields!");
        return;
    }
    if (newStreet == ""){
        newStreet = street;
    }
    if (newState == ""){
        newState = state;
    }
    if (newZip == ""){
        newZip = zip;
    }
    var address = newStreet + ", " + newState + ", " + newZip;
    data["address"] = address;

    if (notes != "")
        data["notes"] = notes;
    //console.log(data);
    $.ajax({
        type: "POST",
       contentType: "application/json",
       dataType: "json",
       url: "/users/profile/update/",
       data: JSON.stringify(data)
       }).done(function( msg ) {
               debug = msg;
               setBoxes(data);
               //console.log(msg)
               });

    var diets = Array();
    $("input[name=option1]:checked").each(function() {
        var diet = $(this).val();
        diets.push(diet);
    });
    $.ajax({
        type: "POST",
       contentType: "application/json",
       dataType: "json",
       url: "/users/diet/update/",
       data: JSON.stringify({diet: diets})
       }).done(function( msg ) {
               debug = msg;
               selectDietRestrictions(diets);
               //console.log(msg)
               });
    
}

function logout(){
    window.location.href = "/users/logout/";
}