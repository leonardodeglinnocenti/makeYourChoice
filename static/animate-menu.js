// When .menu-button is tapped, make navbar visible

// TODO: fix this (broken)

const mobileMenu = document.getElementsByClassName('menu-button');

mobileMenu.addEventListener('click', toggleMobileNavbar);

function toggleMobileNavbar() {
    document.getElementById('navbar').classList.toggle('hideMobileNavbar');
}