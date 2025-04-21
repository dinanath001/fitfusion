// Toggle password visibility using class selectors
document.querySelectorAll('.toggle-password').forEach(toggle => {
    toggle.addEventListener('click', function () {
        const input = this.closest('.input-group').querySelector('.password-input');
        const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
        input.setAttribute('type', type);

        // Change icon based on page/icon (optional emoji style)
        if (this.textContent === '👀') {
            this.textContent = '🙈';
        } else if (this.textContent === '👁️') {
            this.textContent = '🙈';
        } else if (this.textContent === '🙈'){
            this.textContent = '👁️'
        }

        else {
            this.textContent = '👀'; // fallback
        }
    });
});
