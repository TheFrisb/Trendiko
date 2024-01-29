// on document loaded vanilla js

document.addEventListener('DOMContentLoaded', function () {
  const menuIcon = document.getElementById('menuIcon');
  const navbar = document.getElementById('navbar');


  menuIcon.addEventListener('click', function () {
    navbar.classList.toggle('hidden');
  });
   
})
