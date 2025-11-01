document.addEventListener("DOMContentLoaded", function () {
    // Video Control Logic
    let videos = document.querySelectorAll("video");
    let index = 0;

    function playNextVideo() {
        videos[index].classList.remove("active"); // Remove active class from current video
        videos[index].pause(); // Pause current video
        videos[index].currentTime = 0; // Reset current video time

        index = (index + 1) % videos.length; // Move to the next video in loop

        videos[index].classList.add("active"); // Add active class to next video
        videos[index].play(); // Play next video
    }

    videos.forEach((video) => {
        video.addEventListener("ended", playNextVideo); // Switch video when one ends
    });

    // Start playing the first video on page load
    if (videos.length > 0) {
        videos[index].classList.add("active");
        videos[index].play(); 
    }

});
