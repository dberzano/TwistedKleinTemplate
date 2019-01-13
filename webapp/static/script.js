(function($) {

  var updateStatusRunning = false;
  var updateStatusTimer = null;
  var updateStatus = function() {
    if (updateStatusRunning) { return; }
    updateStatusRunning = true;
    console.log("Checking jobs status");
    $.get("/query-job")
      .done(function(data) {
        destHtml = "";
        $.each(data, function(jobId, jobStatus) {
          if (jobStatus["finished"]) { st = "finished"; }
          else if (jobStatus["running"]) { st = "running"; }
          else { st = "queued"; }
          destHtml += "<li><b>#" + jobId + ":</b> " + st + "</li>";
        });
        $("#jobStatus").html(destHtml);
      })
      .always(function(data) {
        updateStatusRunning = false;
      })
  };
  var updateStatusFire = function() {
    window.clearInterval(updateStatusTimer);
    updateStatus();
    updateStatusTimer = window.setInterval(updateStatus, 4000);
  };

  var main = function() {
    // Periodically call function to update status
    updateStatusFire();

    // Click on the start job button
    $("#startJob").click(
      function() {
        $.get("/start-job")
          .done(function(data) {
            jobId = parseInt(data["jobId"]);
            console.log("Started job with id " + jobId);
            updateStatusFire();
          });
      });
  };

  // Call entry point
  $(document).ready(main);

})(jQuery);
