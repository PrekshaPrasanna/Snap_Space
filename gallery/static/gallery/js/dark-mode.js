document.addEventListener('DOMContentLoaded', function() {
    // Check for saved dark mode preference
    const darkModeEnabled = localStorage.getItem('darkMode') === 'true';
    
    // Initialize dark mode based on saved preference
    if (darkModeEnabled) {
        document.body.classList.add('dark-mode');
        updateDarkModeToggle(true);
    }
    
    // Set up dark mode toggle
    const darkModeToggle = document.querySelector('.dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            const isDarkMode = document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', isDarkMode);
            updateDarkModeToggle(isDarkMode);
        });
    }
    
    // Update toggle icon and text
    function updateDarkModeToggle(isDarkMode) {
        const toggleIcon = document.querySelector('.dark-mode-toggle');
        if (toggleIcon) {
            toggleIcon.innerHTML = isDarkMode ? '☀️' : '🌙';
            toggleIcon.setAttribute('title', isDarkMode ? 'Switch to light mode' : 'Switch to dark mode');
        }
    }
});