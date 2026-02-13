/*!
* Start Bootstrap - Grayscale v7.0.6 (https://startbootstrap.com/theme/grayscale)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when a nav link or dropdown item is clicked (not when opening the Trips dropdown)
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const closeOnClick = (el) => {
        if (navbarToggler && window.getComputedStyle(navbarToggler).display !== 'none') {
            navbarToggler.click();
        }
    };
    document.querySelectorAll('#navbarResponsive .dropdown-item').forEach(el => {
        el.addEventListener('click', closeOnClick);
    });
    document.querySelectorAll('#navbarResponsive .nav-link:not(.dropdown-toggle)').forEach(el => {
        el.addEventListener('click', closeOnClick);
    });

});