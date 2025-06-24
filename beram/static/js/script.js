document.addEventListener('DOMContentLoaded', function() {
    console.log("BeRAM Website JS Loaded");

    // --- Navbar Scroll Effect ---
    const navbar = document.getElementById('mainNavbar');
    // Increase threshold slightly for a less abrupt change
    const scrollThreshold = 80;

    const handleScroll = () => {
        if (navbar) { // Check if navbar exists on the page
            if (window.scrollY > scrollThreshold) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        }
    };

    // Initial check in case the page loads already scrolled down
    handleScroll();
    // Listen for scroll events
    window.addEventListener('scroll', handleScroll);
    // --- End Navbar Scroll Effect ---


    // --- Navbar Active Link Styling ---
    // Simplified active link handling (adjust if using dropdowns extensively)
    const navLinks = document.querySelectorAll('#mainNavbar .nav-link');
    const currentPath = window.location.pathname;

    navLinks.forEach(link => {
        // Exact match or starts with (for blueprint prefixes)
        if (link.getAttribute('href') === currentPath || (currentPath.startsWith(link.getAttribute('href')) && link.getAttribute('href') !== '/')) {
             // Check for home page explicitly
             if(currentPath === '/' && link.getAttribute('href') === '/') {
                link.classList.add('active');
             } else if (link.getAttribute('href') !== '/') {
                 link.classList.add('active');
             }
        } else {
            link.classList.remove('active');
        }
    });
     // Ensure home link is active only on home page
     const homeLink = document.querySelector('#mainNavbar .nav-link[href="/"]');
     if (homeLink && currentPath !== '/') {
         homeLink.classList.remove('active');
     } else if (homeLink && currentPath === '/') {
         homeLink.classList.add('active');
     }

    // --- End Navbar Active Link Styling ---


    // --- Initialize AOS ---
    AOS.init({
        duration: 800, // Animation duration
        once: true, // Whether animation should happen only once
        offset: 50, // Offset (in px) from the original trigger point
        easing: 'ease-in-out', // Default easing
    });
    // --- End Initialize AOS ---

});