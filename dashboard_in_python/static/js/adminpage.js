$(document).ready(function() {
  logs = {};
  currentDevice = "";

  // Poll the logs
  setInterval(function() {
    var currentTime = new Date();
    $("#updateTime").text(currentTime);
    getDevices();
    getLogs();
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

    xhr.open("GET", "http://35.238.172.4/api/v1.0/users/mike/logs");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Cache-Control", "no-cache");

    xhr.send(data);
  }

  function getDevices() {
    var data = null;

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function() {
      if (this.readyState === 4) {
        devices = JSON.parse(this.responseText);
        $("#deviceSubmenu").empty();
        devices.forEach(function(device) {
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

    xhr.open("GET", "http://35.238.172.4/api/v1.0/users/tim/device");
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
