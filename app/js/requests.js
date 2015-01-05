/**
 * Created by Amanpreet on 1/2/15.
 */

//request for logging in
$.ajax({
    type: "POST",
    contentType: "application/json",
    dataType: "json",
    url: "/users/login/",
    data: JSON.stringify({email : 'myemail', password : 'pass'})
}).done(function( msg ) {
    debug = msg;
    console.log(msg)
});

//request for signing up
$.ajax({
       type: "POST",
       contentType: "application/json",
       dataType: "json",
       url: "/users/signup/",
       data: JSON.stringify({name : 'myname', email : 'myemail', password : 'pass'})
       }).done(function( msg ) {
               debug = msg;
               console.log(msg)
               });

//request for updating profile
$.ajax({
       type: "POST",
       contentType: "application/json",
       dataType: "json",
       url: "/users/profile/update/",
       data: JSON.stringify({name : 'myname', email : 'myemail', address: 'address', phone: 'myphone', dietary_restrictions: 'food i cant eat'})
       }).done(function( msg ) {
               debug = msg;
               console.log(msg)
               });

//request for logging out
$.ajax({
       type: "POST",
       contentType: "application/json",
       dataType: "json",
       url: "/users/logout",
       data: ""
       }).done(function( msg ) {
               debug = msg;
               console.log(msg)
               });

//request to get chef page info
$.ajax({
       type: "GET",
       contentType: "application/json",
       dataType: "json",
       url: "/users/chefpage",
       data: JSON.stringify({name : 'myname', email : 'myemail', address: 'address', phone: 'myphone', dietary_restrictions: 'food i cant eat'})
       }).done(function( msg ) {
               debug = msg;
               console.log(msg)
               });