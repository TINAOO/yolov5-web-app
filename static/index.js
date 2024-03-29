window.onload = () => {
  $("#sendbutton").click(() => {
    $("#loader").css("visibility", "visible");
    $("#link1").css("visibility", "hidden");
    $("#link2").css("visibility", "hidden");
    $("#row").css("visibility", "hidden");

    imagebox = $("#imagebox");
    link = $("#link");
    input = $("#imageinput")[0];
    if (input.files && input.files[0]) {
      let formData = new FormData();
      formData.append("video", input.files[0]);
      $.ajax({
        url: "/detect", 
        type: "POST",
        data: formData, // get data from app.py in the format of [video_name : particle_count]
        cache: false,
        processData: false,
        contentType: false,
        error: function (data) {
          console.log("upload error", data);
          console.log(data.getAllResponseHeaders());
          $("#link").css("visibility", "hidden");
        },
        success: function (data) { // data we got from app.py in the format of [video_name : particle_count]
          $("#loader").css("visibility", "hidden");
          vid_name = data.split(":")[0] // parse vid name from data
          num_particles = data.split(":")[1] // parse particle count from data
          $("#link1").css("visibility", "visible");
          $("#link2").css("visibility", "visible");
          $("#row").css("visibility", "visible");
          $("#download").attr("href", "static/" + vid_name); // download link for processed video
          $("#download-txt").attr("href", "static/" + vid_name.split(".")[0]+".txt"); // download link for text result
          $("#row").html("number of particles: "+num_particles) // pass number of particles to ---> index.html
        },
      });
    }
  });
}


