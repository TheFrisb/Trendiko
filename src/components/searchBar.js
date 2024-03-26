const searchIcon = document.querySelector('#searchIcon');
const closeSearchIcon = document.querySelector('#searchScreenContainer__closeSearch');
const searchContainer = document.querySelector('#searchScreenContainer');
const searchBar = document.querySelector('#searchScreenContainer__searchBar');

function showSearchBar() {
  searchContainer.classList.add('active');
  searchBar.focus();
}

function hideSearchBar() {
  searchContainer.classList.remove('active');
}


function initializeSearchBar() {
  if (searchIcon && closeSearchIcon && searchContainer && searchBar) {
    searchIcon.addEventListener('click', showSearchBar);
    closeSearchIcon.addEventListener('click', hideSearchBar);
  }
}

export {initializeSearchBar};
