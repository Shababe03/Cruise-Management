// Navigation Menu Toggle
const menuBtn = document.getElementById("menu-btn");
const navLinks = document.getElementById("nav-links");
const menuBtnIcon = menuBtn.querySelector("i");

menuBtn.addEventListener("click", () => {
  navLinks.classList.toggle("open");

  const isOpen = navLinks.classList.contains("open");
  menuBtnIcon.setAttribute("class", isOpen ? "ri-close-line" : "ri-menu-line");
});

// Add a scroll event listener to change the navbar style
window.addEventListener('scroll', () => {
  const body = document.body;
  const scrollPosition = window.scrollY; // Current scroll position

  if (scrollPosition > 50) {
      body.classList.add('scrolled');
  } else {
      body.classList.remove('scrolled');
  }
});

// Close Menu on Click (for mobile)
navLinks.addEventListener("click", () => {
  navLinks.classList.remove("open");
  menuBtnIcon.setAttribute("class", "ri-menu-line");
});

// Scroll Reveal Animations (Using ScrollReveal.js)
const scrollRevealOption = {
  origin: "bottom",
  distance: "50px",
  duration: 1000,
};

// Reveal elements
ScrollReveal().reveal(".hero__content h1", { ...scrollRevealOption, delay: 200 });
ScrollReveal().reveal(".hero__content p", { ...scrollRevealOption, delay: 400 });
ScrollReveal().reveal(".hero__btns", { ...scrollRevealOption, delay: 600 });
ScrollReveal().reveal(".hero__image img", { ...scrollRevealOption, origin: "right", delay: 800 });
ScrollReveal().reveal(".service__card", { ...scrollRevealOption, interval: 300 });
ScrollReveal().reveal(".destination__card", { ...scrollRevealOption, interval: 300 });
ScrollReveal().reveal(".cta-banner h2", { ...scrollRevealOption });
ScrollReveal().reveal(".cta-banner .btn-primary", { ...scrollRevealOption, delay: 200 });

//Slide carousel

// Define the number of cards to show at once
const cardsToShow = 3;

// Initialize slide positions
let currentDestinationSlide = 0;
let currentServiceSlide = 0;

// Update carousel position function
function updateCarouselPosition(wrapper, currentSlide, totalSlides) {
    const offset = -(currentSlide * 100 / cardsToShow);
    wrapper.style.transform = `translateX(${offset}%)`;
}

// Move destination slide function
function moveDestinationSlide(direction) {
    const destinationWrapper = document.querySelector('.carousel-wrapper.destination');
    const totalDestinationSlides = document.querySelectorAll('.carousel-wrapper.destination .carousel-slide').length;

    // Adjust current slide index
    currentDestinationSlide += direction * cardsToShow;

    // Clamp the position
    if (currentDestinationSlide < 0) {
        currentDestinationSlide = 0;
    } else if (currentDestinationSlide > totalDestinationSlides - cardsToShow) {
        currentDestinationSlide = totalDestinationSlides - cardsToShow;
    }

    // Update position
    updateCarouselPosition(destinationWrapper, currentDestinationSlide, totalDestinationSlides);
}

// Move service slide function
function moveServiceSlide(direction) {
    const serviceWrapper = document.querySelector('.carousel-wrapper.service');
    const totalServiceSlides = document.querySelectorAll('.carousel-wrapper.service .carousel-slide').length;

    // Adjust current slide index
    currentServiceSlide += direction * cardsToShow;

    // Clamp the position
    if (currentServiceSlide < 0) {
        currentServiceSlide = 0;
    } else if (currentServiceSlide > totalServiceSlides - cardsToShow) {
        currentServiceSlide = totalServiceSlides - cardsToShow;
    }

    // Update position
    updateCarouselPosition(serviceWrapper, currentServiceSlide, totalServiceSlides);
}

// Initialize carousels at starting positions
function initializeCarousels() {
    currentDestinationSlide = 0;
    currentServiceSlide = 0;

    // Set initial positions for each carousel
    document.querySelector('.carousel-wrapper.destination').style.transform = 'translateX(0%)';
    document.querySelector('.carousel-wrapper.service').style.transform = 'translateX(0%)';
}

// Add event listeners for buttons after DOM loads
document.addEventListener("DOMContentLoaded", () => {
    initializeCarousels();

    // Destination carousel button event listeners
    document.querySelector('.carousel-button.prev.destination').addEventListener('click', () => moveDestinationSlide(-1));
    document.querySelector('.carousel-button.next.destination').addEventListener('click', () => moveDestinationSlide(1));

    // Service carousel button event listeners
    document.querySelector('.carousel-button.prev.service').addEventListener('click', () => moveServiceSlide(-1));
    document.querySelector('.carousel-button.next.service').addEventListener('click', () => moveServiceSlide(1));
});


