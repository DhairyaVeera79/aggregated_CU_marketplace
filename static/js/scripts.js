document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('#sidebar-nav .nav-link');
    const tabContents = document.querySelectorAll('.tab-content');

    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            // Remove active class from all links
            navLinks.forEach(link => link.classList.remove('active'));

            // Hide all tab contents
            tabContents.forEach(content => content.classList.add('d-none'));

            // Add active class to the clicked link
            this.classList.add('active');

            // Show the corresponding tab content
            const target = this.getAttribute('href');
            document.querySelector(target).classList.remove('d-none');
        });
    });
});
