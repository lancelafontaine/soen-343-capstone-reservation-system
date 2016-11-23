(function() {

/*
Dependencies
*/

$ = jQuery = require('jquery');
require('fullcalendar');
moment = require('moment');
require('./library/bootstrap.min.js');
var bootbox = require('bootbox');

/*
Init page
*/
var currentRoom;
var session;
var waitingList;
var reservedList;
var rooms;


$(document).ready(function(){
  getUserSessionInfo();
  //display latest user info
  displayUserInfo();
  //set sidebar backgoround
  setSideBarConcordia();
  //set login page animation
  loginPageAnimation();
  // binding login event on to login button
  $("#login-button").click(function(){
    authenticateUser();
  });
  // binding login event on to login button
  $("#logout-button").click(function(){
    logoutUser();
  });
  // binding event to user's reservations
  $("#reservation-list, #waiting-list").delegate('.cancel-reserved','click',function(){
    cancelReservation();
  });
  $("#reservation-list, #waiting-list").delegate('.modify-reserved','click',function(){
    var selectCurrent = $( event.target ).closest( "tr" ).text();
    var oldRoomNumber = selectCurrent.substring(0,5);
    var oldTimeSlot = selectCurrent.substring(6,selectCurrent.length);

    // check if reservation is on waiting list
    var isOnWaitingList = false;
    for (var j=0; j < waitingList.length; j++){
      if (oldTimeSlot == waitingList[j][2]) {
        if (oldRoomNumber == waitingList[j][1]){
          isOnWaitingList = true;
        }
      }
    }
    if (!isOnWaitingList && moment(oldTimeSlot).isBefore(moment())) {
      bootbox.alert({
        title: "Error",
        message: "<div style='width:100%;text-align:center;'><i class='fa fa-close fa-4x' style='color:red;'></i></div><br/><span style='font-size:22px;'>" +
            "Can't modify booked reservations from the past!" +
            "</span>",
          size: 'small',
          backdrop: true,
          closeButton: false
      });
      return;
    }

    function prompt1() {
      var newRoomNumber;
      bootbox.prompt({
        title: "Please enter the room in format ex: H-905",
        backdrop: true,
        closeButton: false,
        callback: function(result){
          newRoomNumber = result;
          if (newRoomNumber) {
            if(rooms.indexOf(newRoomNumber) == -1){
              prompt1();
            } else {
              prompt2(newRoomNumber);
            }
          }
        }
      });
    }
    function prompt2(newRoomNumber) {
      var newTimeSlot;
      bootbox.prompt({
        title: "Please enter the time in format ex: 2016-11-24 15:00:00",
        backdrop: true,
        closeButton: false,
        callback: function(result){
          newTimeSlot = result;
          if (newTimeSlot){
            if(!/\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2}/.test(newTimeSlot)){
              prompt2(newRoomNumber);
            } else{
              modifyReservation(oldRoomNumber,newRoomNumber,oldTimeSlot,newTimeSlot);
            }
          }
        }
      });
    }

    prompt1();

  });
  //select room
  $("#room-list").on('click','li',function (){
    if (currentRoom != $(this).attr('id')) {
      $(currentRoom).removeClass("active");
      currentRoom = "#" + $(this).attr('id');
      $(this).addClass("active");
      showBookingByRoom();
    }
  });
  //calendar code
  $('#calendar').fullCalendar({
    header: {
      left: "",
      center: "title",
      right: ""
    },
    firstDay: 1,
    contentHeight: "auto",
    defaultView: "agendaWeek",
    defaultTimedEventDuration: "01:00:00",
    //TODO: disable previous date in calendar view
    selectable: true,
    allDaySlot: false,
    minTime: "08:00:00",
    maxTime: "21:00:00",
    slotDuration: "01:00:00",
    slotEventOverlap: false,
    eventColor: "#FF4A55",
    editable: true,
    droppable: true,
    events: [],
    select: function(start, end, jsEvent, view){
      var room = $(currentRoom).text();
      var startDate = moment(start).format("YYYY-MM-DD HH:mm:ss");
      if (moment(startDate).isBefore(moment())) {
        bootbox.alert({
          message: "<div style='width:100%;text-align:center;'><i class='fa fa-close fa-4x' style='color:red;'></i></div><br/><span style='font-size:22px;'>" +
              "Can't book reservations in the past!" +
              "</span>",
            size: 'small',
            backdrop: true,
            closeButton: false
        });
      } else {
        makeReservation(room, startDate);
      }
    },
    eventClick: function(calEvent, jsEvent, view) {
      eventUsername = calEvent.title;
      if (eventUsername == session.username){
        bootbox.alert({
          message: "<div style='width:100%;text-align:center;'><i class='fa fa-close fa-4x' style='color:red;'></i></div><br/><span style='font-size:22px;'>" +
              "You are already registered for that timeslot!" +
              "</span>",
            size: 'small',
            backdrop: true,
            closeButton: false
        });
      } else if (moment(calEvent.start).isBefore(moment())) {
        bootbox.alert({
          message: "<div style='width:100%;text-align:center;'><i class='fa fa-close fa-4x' style='color:red;'></i></div><br/><span style='font-size:22px;'>" +
              "Can't book reservations in the past!" +
              "</span>",
            size: 'small',
            backdrop: true,
            closeButton: false
        });
      } else {
        var room = $(currentRoom).text();
        var startDate = moment(calEvent.start).format("YYYY-MM-DD HH:mm:ss");
        makeReservation(room, startDate);
      }
    }
  });
});

/*
Free functions
*/

function setSideBarConcordia(){
  $sidebar = $('.sidebar');
  image_src = $sidebar.data('image');
  if(image_src !== undefined){
    sidebar_container = '<div class="sidebar-background" style="background-image: url(' + image_src + ') "/>'
    $sidebar.append(sidebar_container);
  }
}

function loginPageAnimation(){
  $('input').blur(function() {
    var $this = $(this);
    if ($this.val()) $this.addClass('used');
    else $this.removeClass('used');
  });
  var $ripples = $('.ripples');
  $ripples.on('click.Ripples', function(e) {
    var $this = $(this);
    var $offset = $this.parent().offset();
    var $circle = $this.find('.ripplesCircle');
    var x = e.pageX - $offset.left;
    var y = e.pageY - $offset.top;
    $circle.css({
      top: y + 'px',
      left: x + 'px'
    });
    $this.addClass('is-active');
  });
  $ripples.on('animationend webkitAnimationEnd mozAnimationEnd oanimationend MSAnimationEnd', function(e) {
    $(this).removeClass('is-active');
  });
}

function authenticateUser(){
  // Retrieving username and password from login page
  var username = $("#username").val();
  var password = $("#password").val();
  if( username.length == 0 || password.length == 0 ){
    $("#login-error-msg").html("<font color='red'><b> ERROR: One of the fields above is empty. </b></font>");
  }
  var requestData = "username=" + username + "&password=" + password;
  $.ajax({
    method: 'POST',
    url: 'http://localhost:8000/login/',
    data: requestData,
    dataType: "json",
    xhrFields: {
      withCredentials: true
    },
    success: function(data, status){
      if(data.loggedIn == true){
        window.top.location = '/home.html';
      } else {
        var errorMsg = data.loginError;
        $("#login-error-msg").html("<font color='red'><b> ERROR: " + errorMsg + "</b></font>");
      }
    }
  });
}

function logoutUser(){
  $.ajax({
    method: 'POST',
    url: 'http://localhost:8000/logout/',
    data: '',
    xhrFields: {
      withCredentials: true
    },
    success: function(data){
      window.top.location = '/';
    }
  });
}

function getRoomList() {
	$.ajax({
    method: 'GET',
    url: 'http://localhost:8000/getRooms/',
    cache: false,
    success: function(res){
      rooms = res.rooms;
      for (var i=0; i < res.rooms.length; i++) {
        $("#room-list").append("<li id='room-"+i+"'><a><p>" + res.rooms[i] + "</p></a></li>");
        if (!currentRoom){
          currentRoom = "#room-" + i;
          $("#room-"+i).addClass("active");
          showBookingByRoom();
        }
      }
    }
  });
}

function showBookingByRoom() {
  $('#calendar').fullCalendar('removeEvents');
  var currentRoomReservation = [];
  var beginOfWeek = $('#calendar').fullCalendar('getDate').startOf('week').format().split("T");
  $.ajax({
    method: 'GET',
    url: "http://localhost:8000/getReservations/?roomNumber="
    + $(currentRoom).text()
    + "&startTimeslot="
    + beginOfWeek[0]
    + "%20"
    + beginOfWeek[1],
    cache: false,
    success: function(res){
      for (var i=0; i < res.reservations.length; i++) {
        var reservation = res.reservations[i][1].split(" ");
        var user = res.reservations[i][0];
        var date = reservation[0].split("-");
        var year = date[0];
        var month = date[1];
        var day = date[2];
        var time = reservation[1].split(":");
        var hours = time[0];
        var minutes = time[1];
        var seconds = time[2];
        var eventStart = new Date(year, month-1, day, hours, minutes, seconds);

        var backgroundColor = '#663399';

        // Check if any of these are on the users waiting list
        for (var j=0; j < waitingList.length; j++){
          if (res.reservations[i][1] == waitingList[j][2] ) {
            if ($(currentRoom).text() == waitingList[j][1]){
              backgroundColor = '#f982e8';
            }
          }
        }
        // Greyed-out timeslot are ones that before the current time.
        if (moment(res.reservations[i][1]).isBefore(moment())) {
            backgroundColor = '#adadad';
        }

        var slot = {
          title: user,
          start: eventStart,
          backgroundColor: backgroundColor
        };
      $('#calendar').fullCalendar("renderEvent", slot, true);
      }
    }
  });
}

function getUserSessionInfo() {
  $.ajax({
    method: 'GET',
    url: 'http://localhost:8000/getSessionInfo',
    cache: false,
    xhrFields: {
      withCredentials: true
    },
    success: function(res){
      session = res;
      currentURL = window.location.href;
      if (!session['is-logged-in']&& /home/.test(currentURL)) {
        window.top.location = '/index.html';
      }
    }
  });
}

function displayUserInfo() {
  getReservationList();
  getWaitingList();
}

function clearUserInfo() {
  $("#reservation-list").remove("*");
  $("#waiting-list").remove("*");
}

function getReservationList() {
  $.ajax({
    url: 'http://localhost:8000/getReservedList',
    cache: false,
    xhrFields: {
      withCredentials: true
    },
    success: function(res){
      reservedList = res.reservedList;
      filteredReservedList = [];

      // Filter through reservations that occurred before this week
      for (var i = 0; i < reservedList.length; i++) {
        if (moment(reservedList[i][2]).isBefore(moment().startOf('isoWeek'))) {
          continue;
        } else {
          filteredReservedList.push(reservedList[i]);
        }
      }
      appendBookingList(filteredReservedList, "reservation-list");
    }
  });
}

function getWaitingList() {
  $.ajax({
    url: 'http://localhost:8000/getWaitingList',
    cache: false,
    xhrFields: {
      withCredentials: true
    },
    success: function(res){
      waitingList = res.waitingList;
      filteredWaitingList = [];

      // Filter through reservations that occurred before this week
      for (var i = 0; i < waitingList.length; i++) {
        if (moment(waitingList[i][2]).isBefore(moment().startOf('isoWeek'))) {
          continue;
        } else {
          filteredWaitingList.push(waitingList[i]);
        }
      }
      appendBookingList(filteredWaitingList, "waiting-list");

      //get all rooms available from back-end
      getRoomList();
    }
  });
}

function makeReservation(room, timeslot){
  //building the request
  var requestData = "roomNumber=" + room + "&" + "timeslot=" + timeslot;
  //ajax call
  $.ajax({
    method: 'POST',
    url: 'http://localhost:8000/makeReservation/',
    data: requestData,
    dataType: "json",
    xhrFields: {
      withCredentials: true
    },
    success: function(data, status){
      if( data.madeReservation == false ){
        var reservationErrorMsg = data.reservationError;
        $("#reservation-error-msg").html("<font color='red'><b>ERROR: " + reservationErrorMsg + " </b></font>");
      } else {
        location.reload();
      }
    }
  });
}

function cancelReservation() {
  //Select the current reservation list
  var selectCurrent = $( event.target ).closest( "tr" ).text();
  var roomNumber = selectCurrent.substring(0,5);
  var timeslot = selectCurrent.substring(6,selectCurrent.length);
  var requestData = "roomNumber=" + roomNumber + "&timeslot=" + timeslot;

  // check if reservation is on waiting list
  var isOnWaitingList = false;
  for (var j=0; j < waitingList.length; j++){
    if (timeslot == waitingList[j][2]) {
      if (roomNumber == waitingList[j][1]){
        isOnWaitingList = true;
      }
    }
  }

  if (!isOnWaitingList && moment(timeslot).isBefore(moment())) {
    bootbox.alert({
      message: "<div style='width:100%;text-align:center;'><i class='fa fa-close fa-4x' style='color:red;'></i></div><br/><span style='font-size:22px;'>" +
          "Can't remove booked reservations from the past!" +
          "</span>",
        size: 'small',
        backdrop: true,
        closeButton: false
    });
  } else {
    $.ajax({
      method: 'POST',
      url: 'http://localhost:8000/cancelReservation/',
      data: requestData,
      dataType : "json",
      cache: false,
      xhrFields: {
        withCredentials: true
      },
      success: function(res){
      }
    });
    location.reload();
  }
}

//This function will modify the reservation
function modifyReservation(oldRoomNumber,newRoomNumber,oldTimeslot,newTimeslot) {
  var requestData = "oldRoomNumber=" + oldRoomNumber + "&newRoomNumber=" + newRoomNumber  + "&oldTimeslot=" + oldTimeslot + "&newTimeslot=" + newTimeslot ;

  $.ajax({
    method: 'POST',
    url: 'http://localhost:8000/modifyReservation/',
    data: requestData,
    dataType : "json",
    cache: false,
    xhrFields: {
      withCredentials: true
    },
    success: function(res){
    }
  });
  location.reload();
}

/*
Helpers
*/

function appendBookingList(booking, listType) {
	for (var i = 0; i < booking.length; i++) {
    $("#"+listType).append("<tr id='" + listType + "-" + i + "'><td>" + booking[i][1] + "@" + booking[i][2]
      + "</td><td class='td-actions text-right'><button type='button' rel='tooltip' title='Modify' class='btn modify-reserved'><i class='fa fa-pencil'></i></button>"
      + "<button type='button' rel='tooltip' title='Cancel' class='btn cancel-reserved'>"
      + "<i class='fa fa-times'></i></button></td></tr>"
    );
  }
}

})();

