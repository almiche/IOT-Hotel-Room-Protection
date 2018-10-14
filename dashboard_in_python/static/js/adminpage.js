$(document).ready(function() {
  logs = {};
  currentDevice = "";
  currentToken = ""

  if(!Cookies.get('user')){
      stateSwitch('OUT');
  }
  else if (Cookies.get('user')){
    stateSwitch('IN');
  }

  function stateSwitch(state){
    switch(state){
      case 'IN':
        $("#title").text(`${Cookies.get('user')}'s Dashboard`);
        $(".signin").css('display','none');
        $(".signup").css('display','none');
        $("#signup,#signin").css('display',"none")
        $('#deviceSubmenuContainer').css('display','block');
        $('#logout').css('display','block')
      break;
      case 'OUT':
        $('.signup').css('display','none');
        $('#deviceSubmenu').css('display','none');
        $('#logout').css('display','none');
        $('#signup,#signin').css('display','block');
        $('.signin').css('display','block');
        $('#deviceSubmenuContainer').css('display','none');
      break;
      case 'SIGNUP':
        $('.signup').css('display','block');
      break;
    }
  }

  // Poll the logs
  setInterval(function() {
    var currentTime = new Date();
    $("#updateTime").text(currentTime);
    if (Cookies.get('token') != null){
      getDevices();
      getLogs();
    }
  }, 3000);

  function getLogs() {
    var data = null;

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function() {
      if (this.readyState === 4) {
        logs = JSON.parse(this.responseText);
      }
    });

    xhr.open("GET", `/users/${Cookies.get('user')}/logs?token=${Cookies.get('token')}`);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Cache-Control", "no-cache");

    xhr.send(data);
  }
  
  $("#signin").on("click",function login(){
    var data = JSON.stringify({
      "user": $("#username").val(),
      "password": $("#password").val()
    });
  
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
  
    xhr.addEventListener("readystatechange", function() {
      if (this.readyState === 4) {
        response = JSON.parse(this.responseText);
        Cookies.set('user', response.user);
        Cookies.set('token', response.token);
        getDevices();
        stateSwitch('IN');
      }
    });
  
    xhr.open("POST", "/generate-token");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Cache-Control", "no-cache");
  
    xhr.send(data);
    
  });

  $("#logout").on("click",function login(){
    var data = JSON.stringify({
      "user": Cookies.get('user'),
      "token": Cookies.get('token')
    });
  
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
  
    xhr.addEventListener("readystatechange", function() {
      if (this.readyState === 4) {
        response = JSON.parse(this.responseText);
        Cookies.remove('user');
        Cookies.remove('token');
        stateSwitch('OUT');
      }
    });
  
    xhr.open("POST", "/signout");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Cache-Control", "no-cache");
  
    xhr.send(data);
    
  });

  function getDevices() {
    var data = {};

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function() {
      if (this.readyState === 4) {
        response = JSON.parse(this.responseText);
        $("#deviceSubmenu").empty();
        response.devices.forEach(function(device) {
          $("#deviceSubmenu").append(
            `<li ><a class="device" name="${device.mac}" href="#"><strong>${
              device.device_type
            }</strong>:\n${device.mac}</a></li>`
          );
        });
      }
      $(".device").on("click", function() {
        infoOnDevice(this.name);
      });
    });

    xhr.open("GET", `/users/${Cookies.get('user')}/device?token=${Cookies.get('token')}`);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Cache-Control", "no-cache");

    xhr.send(data);
  }

  function infoOnDevice(device) {
    currentDevice = device;
    $(".history .entries").empty();
    logs[device].forEach(function(log) {
      $(
        ".history .entries"
      ).append(`<button class="accordion" name="${log.id}" style="background-color:white">${log.timestamp}</button>
                    <div class="panel">
                        <p>${log.log_dump}</p>
                    </div>`);
    });
    refreshAccordion();
    last_log = logs[device].slice(-1)[0];
    logClicked(last_log)
}

  function logClicked(log){
    dump = [];
    log.log_dump
      .slice(1, log.log_dump.length - 1)
      .split(",")
      .forEach(function(digit) {
        dump.push(parseInt(digit));
      });
    myChart.data.datasets[0].data = dump;
    myChart.options.title.text = `Acceleration data ${log.device} at ${log.timestamp}`
    myChart.update();
    $("#totalAlerts").text(logs[currentDevice].length);
  }

  function refreshAccordion() {
    var acc = document.getElementsByClassName("accordion");
    var i;

    for (i = 0; i < acc.length; i++) {
      acc[i].addEventListener("click", function() {
        /* Toggle between adding and removing the "active" class,
                to highlight the button that controls the panel */
        this.classList.toggle("active");

        /* Toggle between hiding and showing the active panel */
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
          panel.style.display = "none";
        } else {
          panel.style.display = "block";
        }
        currentAcc = this
        logs[currentDevice].forEach(function(log) {
            if (log.id == currentAcc.name){
                console.log(log)
                logClicked(log)
            }
        });
      });
    }
  }

  getDevices();
  getLogs();

  var chart = document.getElementById("graph");
  var myChart = new Chart(chart, {
    type: "line",
    data: {
      labels: [0, 100, 200, 300, 400, 500, 600],
      datasets: [
        {
          data: [],
          label: "Pi Zero",
          borderColor: "#3e95cd",
          fill: false
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: "World population per region (in millions)"
      },
      responsive: true,
      maintainAspectRatio: false
    }
  });
});
