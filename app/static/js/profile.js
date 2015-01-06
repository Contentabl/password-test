/**
 * Created by Amanpreet on 12/31/14.
 */

var orderButton;
var daysList = ['mondayList', 'tuesdayList', 'wednesdayList', 'thursdayList', 'fridayList', 'saturdayList', 'sundayList'];
var mealsList = ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Salad', 'Desert'];

$(document).ready(function(){
    orderButton = $(".btn.orderButton");
    orderButton.click(function(){
        orderClicked();
    });
});

function orderClicked(){
    $(".topLevel").show();

}
function customSelect(){
    for (day in daysList){
        for (meal in mealsList){
            var selector = "." + day + " ." + meal;
            console.log(selector);
            $(selector).prop( "checked", false );
        }
    }
}
function full(){

}
function seven(){

}
function five(){

}
function fiveNoS(){

}
function fiveNoB(){

}
function fiveOnlyD(){

}
function three(){

}