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

    // Newsletter signup (Loops.so) – submit via fetch and show success/error
    document.querySelectorAll('.newsletter-form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const endpoint = form.getAttribute('data-loops-endpoint') || form.action;
            const emailInput = form.querySelector('input[name="email"]');
            const submitBtn = form.querySelector('button[type="submit"]');
            const fieldsWrap = form.querySelector('.newsletter-form-fields');
            const successEl = form.closest('.newsletter-signup-section').querySelector('.newsletter-success-message');
            const errorEl = form.closest('.newsletter-signup-section').querySelector('.newsletter-error-message');
            const email = emailInput && emailInput.value ? emailInput.value.trim() : '';

            if (!email) return;

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Signing up…';
            }
            if (errorEl) errorEl.style.display = 'none';

            try {
                const body = `email=${encodeURIComponent(email)}`;
                const res = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: body
                });
                const data = await res.json().catch(() => ({}));

                if (res.status === 429) {
                    if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Sign up'; }
                    if (errorEl) {
                        errorEl.textContent = 'Too many signups from this address. Please try again in a few minutes.';
                        errorEl.style.display = 'block';
                    }
                    return;
                }

                if (res.ok && data.success) {
                    if (fieldsWrap) fieldsWrap.style.display = 'none';
                    if (successEl) successEl.style.display = 'block';
                } else {
                    if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Sign up'; }
                    if (errorEl) {
                        errorEl.textContent = data.message || 'Something went wrong. Please try again.';
                        errorEl.style.display = 'block';
                    }
                }
            } catch (err) {
                if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Sign up'; }
                if (errorEl) {
                    errorEl.textContent = 'Something went wrong. Please try again.';
                    errorEl.style.display = 'block';
                }
            }
        });
    });

});