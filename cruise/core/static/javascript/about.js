document.addEventListener("DOMContentLoaded", function() {
    const boxes = document.querySelectorAll('.about-box');

    const options = {
        root: null, // Use the viewport as the container
        rootMargin: '0px',
        threshold: 0.1 // Trigger when 10% of the element is visible
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show'); // Add class to show the box
                observer.unobserve(entry.target); // Stop observing once it has been shown
            }
        });
    }, options);

    boxes.forEach(box => {
        observer.observe(box); // Observe each box
    });
});
