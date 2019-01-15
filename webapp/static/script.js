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

        // Reformat data, and order by date
        dataAry = [];
        $.each(data, function(jobId, jobStatus) {
          jobStatus["id"] = jobId;
          dataAry.push(jobStatus);
        });
        dataAry.sort(function(a, b) {
          return b["tqueued"]-a["tqueued"];
        });

        $.each(dataAry, function(index, jobStatus) {
          if (jobStatus["finished"]) { st = "finished"; }
          else if (jobStatus["running"]) { st = "running"; }
          else { st = "queued"; }

          // Job start, end, duration
          momentFmt = "lll";

          jobQueued = "";
          jobStarted = "";
          jobFinished = "";
          jobDuration = "";
          t0 = null;
          t1 = null;
          if (jobStatus["tqueued"]) {
            tq = moment(1000*jobStatus["tqueued"])
            jobQueued = tq.format(momentFmt);
          }
          if (jobStatus["tstarted"]) {
            t0 = moment(1000*jobStatus["tstarted"])
            jobStarted = t0.format(momentFmt);
          }
          if (jobStatus["tfinished"]) {
            t1 = moment(1000*jobStatus["tfinished"])
            jobFinished = t1.format(momentFmt);
          }
          if (!t1) t1 = moment();
          if (t0) {
            td = t1.diff(t0);
            jobDuration = moment.utc(td).format("HH:mm:ss");
          }

          obj = $(updateStatusTemplate[st]).clone();
          obj.html(obj.html()
                     .replace("JOBNAME", "#"+jobStatus["id"])
                     .replace("JOBQUEUED", jobQueued)
                     .replace("JOBSTARTED", jobStarted)
                     .replace("JOBFINISHED", jobFinished)
                     .replace("JOBDURATION", jobDuration));
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
  var updateStatusTemplate = {};

  var main = function() {

    // Required for initing the material design
    $("body").bootstrapMaterialDesign();

    // We need to get the templates for updateStatus
    updateStatusTemplate["running"] = $("#jobStatus .template-running");
    updateStatusTemplate["queued"] = $("#jobStatus .template-queued");
    updateStatusTemplate["finished"] = $("#jobStatus .template-finished");

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
