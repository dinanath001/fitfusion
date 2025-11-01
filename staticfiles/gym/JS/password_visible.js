// Function to toggle the icon based on the current state
function toggleIcon() {
    if (this.textContent === '👀') {
        this.textContent = '🙈';
    } else if (this.textContent === '🙈') {
        this.textContent = '👀';
    } else {
        this.textContent = '👀'; // fallback (in case something goes wrong)
    }
}

// Toggle password visibility using class selectors
document.querySelectorAll('.toggle-password').forEach(toggle => {
    toggle.addEventListener('click', function () {
        // Toggle the password input type (password <-> text)
        const input = this.closest('.input-group').querySelector('.password-input');
        const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
        input.setAttribute('type', type);

        // Use the toggleIcon function to change the emoji based on the current state
        toggleIcon.call(this);
    });
});
