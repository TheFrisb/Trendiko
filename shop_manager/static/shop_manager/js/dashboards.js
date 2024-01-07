document.addEventListener('DOMContentLoaded', function () {
    const openMenuIcon = document.querySelector('#dashboard__menuIcon');
    const closeMenuIcon = document.querySelector('#dashboard__closeMenuIcon');
    const dashboardMenu = document.querySelector('#dashboard__menu');

    openMenuIcon.addEventListener('click', function () {
        dashboardMenu.classList.remove('hidden');
        dashboardMenu.classList.add('flex');
        openMenuIcon.classList.add('hidden');
        closeMenuIcon.classList.remove('hidden');
      }
    );

    closeMenuIcon.addEventListener('click', function () {
        dashboardMenu.classList.add('hidden');
        dashboardMenu.classList.remove('flex');
        openMenuIcon.classList.remove('hidden');
        closeMenuIcon.classList.add('hidden');
      }
    );


  }
);