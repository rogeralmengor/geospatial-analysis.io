document.addEventListener("DOMContentLoaded", function() {
    const themeToggle = document.querySelector('button[title="Switch to dark mode"], button[title="Switch to light mode"]');
    
    if (themeToggle) {
      // Check if theme is stored in localStorage
      const currentTheme = localStorage.getItem("theme");
      if (currentTheme) {
        document.documentElement.setAttribute("data-md-color-scheme", currentTheme);
      }
  
      themeToggle.addEventListener("click", function() {
        // Get the currently active theme
        const theme = document.documentElement.getAttribute("data-md-color-scheme");
        const newTheme = theme === "default" ? "slate" : "default";  // Toggle theme
  
        // Apply new theme and store in localStorage
        document.documentElement.setAttribute("data-md-color-scheme", newTheme);
        localStorage.setItem("theme", newTheme);
      });
    }
  });