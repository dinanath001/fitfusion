  // Scroll animation for sections
  document.addEventListener("scroll", function() {
    const sections = document.querySelectorAll(".section");
    sections.forEach(section => {
        const position = section.getBoundingClientRect().top;
        if (position < window.innerHeight - 100) {
            section.classList.add("visible");
        }
    });
});