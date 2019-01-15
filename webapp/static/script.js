(function($) {

  var updateStatusRunning = false;
  var updateStatusTimer = null;
  var updateStatus = function() {
    if (updateStatusRunning) { return; }
    updateStatusRunning = true;
    console.log("Checking jobs status");
    $.get("/query-job")
      .done(function(data) {
        $("#jobStatus").empty();
        $.each(data, function(jobId, jobStatus) {
          if (jobStatus["finished"]) { st = "finished"; }
          else if (jobStatus["running"]) { st = "running"; }
          else { st = "queued"; }
          obj = $(updateStatusTemplate[st]).clone();
          obj.html( obj.html().replace("JOBNAME", "Job #"+jobId) );
          $("#jobStatus").append( obj );
        });
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
  var updateStatusTemplate = { "running": "", "queued": "", "finished": "" };

  var main = function() {

    // Required for initing the material design
    $("body").bootstrapMaterialDesign();

    // We need to get the templates for updateStatus
    $("#jobStatus a").each(function (count, dom) {
      order = ["running", "queued", "finished"];
      updateStatusTemplate[order[count]] = dom;
    });

    // Periodically call function to update status
    updateStatusFire();

    // Click on the start job button
    $("#jobStart").click(
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
