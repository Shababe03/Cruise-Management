// General Modal Functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex'; // Use 'flex' to allow centering
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.animation = 'fadeOut 0.3s ease-in-out';
        setTimeout(() => {
            modal.style.display = 'none'; // Close modal after fade-out
            modal.style.animation = ''; // Reset animation
        }, 300);
    }
}

function switchModal(currentModalId, targetModalId) {
    closeModal(currentModalId);
    openModal(targetModalId);
}

function toggleModal(closeModalId, openModalId) {
    document.getElementById(closeModalId).style.display = 'none';
    document.getElementById(openModalId).style.display = 'block';
}

// Event listener for close buttons
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.close').forEach(closeButton => {
        closeButton.addEventListener('click', () => {
            const modal = closeButton.closest('.modal');
            if (modal) closeModal(modal.id);
        });
    });
});

// Close modal if the user clicks outside the modal content
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            closeModal(modal.id);
        }
    });
};

// Contact Form Submission
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const contactData = new FormData(contactForm);
            fetch("/contact/", {
                method: "POST",
                body: contactData,
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                const messageElement = document.getElementById('contactMessage');
                if (messageElement) {
                    messageElement.textContent = data.status === 'success' ? 
                        "Message sent successfully!" : 
                        data.message || "Message sending failed. Please try again.";
                    if (data.status === 'success') closeModal('contactModal');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('contactMessage').textContent = "An error occurred. Please try again.";
            });
        });
    }
});

// Login Form Submission
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const loginData = new FormData(loginForm);
            fetch("/login/", {
                method: "POST",
                body: loginData,
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                const messageElement = document.getElementById('loginMessage');
                if (data.status === 'success') {
                    alert(data.message);
                    setTimeout(() => window.location.href = "/base/", 1500);
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('loginMessage').textContent = "An error occurred. Please try again.";
            });
        });
    }
});

// Update Navbar based on login status
function updateNavbar() {
    fetch('/get-login-status/')
        .then(response => response.json())
        .then(data => {
            const isLoggedIn = data.is_logged_in;
            document.getElementById("loginbtn").style.display = isLoggedIn ? "none" : "block";
            document.getElementById("signupbtn").style.display = isLoggedIn ? "none" : "block";
            document.getElementById("profile-btn").style.display = isLoggedIn ? "block" : "none";
            document.getElementById("logout-btn").style.display = isLoggedIn ? "block" : "none";
        })
        .catch(error => console.error('Error fetching login status:', error));
}

document.addEventListener("DOMContentLoaded", updateNavbar);

// Logout Function
function logout() {
    fetch('/logout/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            updateNavbar();
            window.location.href = '';
        } else {
            alert('Logout failed. Please try again.');
        }
    })
    .catch(error => console.error('Error during logout:', error));
}

// Signup Form Submission
document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const signupData = new FormData(signupForm);
            fetch("/signup/", {
                method: "POST",
                body: signupData,
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                const messageElement = document.getElementById('signupMessage');
                if (messageElement) {
                    messageElement.textContent = data.status === 'success' ? 
                        "Signup successful!" : 
                        data.message || "Signup failed. Please try again.";
                    if (data.status === 'success') closeModal('signupModal');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('signupMessage').textContent = "An error occurred. Please try again.";
            });
        });
    }
});
