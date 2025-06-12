// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Typed.js
    var typed = new Typed('#typed', {
        stringsElement: '#typed-strings',
        typeSpeed: 50,
        backSpeed: 30,
        loop: false,
        showCursor: true,
        cursorChar: '|',
        startDelay: 500
    });


    // Google Sign In Button
    const googleBtn = document.querySelector('.google-btn');
    if (googleBtn) {
        googleBtn.addEventListener('click', function() {
            // Here you would redirect to Google OAuth
            console.log('Google sign-in clicked');
            alert('Google sign-in integration would happen here.');
            
            // In a real app:
            // window.location.href = '/accounts/google/login/';
        });
    }
});