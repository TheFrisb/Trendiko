const listable_items = document.querySelector("#listable_items");

// make a function to apply scroll and drag functionality to the listable_items div

function initializeListableItems() {
  if (!listable_items) {
    return;
  }

  let scrollToElement = listable_items.querySelector(".scrollTo");
  if (scrollToElement) {
    listable_items.scrollLeft = scrollToElement.offsetLeft;
  }

  let isDown = false;
  let startX;
  let scrollLeft;

  listable_items.addEventListener("mousedown", (e) => {
    isDown = true;
    listable_items.classList.add("active");
    startX = e.pageX - listable_items.offsetLeft;
    scrollLeft = listable_items.scrollLeft;

    // make cursor a grabbing hand
    listable_items.style.cursor = "grabbing";
  });

  listable_items.addEventListener("mouseleave", () => {
    isDown = false;
    listable_items.classList.remove("active");

  });

  listable_items.addEventListener("mouseup", () => {
    isDown = false;
    listable_items.classList.remove("active");
    // make cursor a grab hand
    listable_items.style.cursor = "grab";
  });

  listable_items.addEventListener("mousemove", (e) => {
    if (!isDown) return;
    e.preventDefault();

    const x = e.pageX - listable_items.offsetLeft;
    const walk = (x - startX)
    listable_items.scrollLeft = scrollLeft - walk;
  });

  listable_items.addEventListener("wheel", (e) => {
    e.preventDefault();
    if (e.deltaY > 0) {
      // get remaining width of the listable_items div
      const remainingWidth = listable_items.scrollWidth - listable_items.offsetWidth;
      // if the scrollLeft is greater than the remaining width, scroll to the remaining width
      if (listable_items.scrollLeft >= remainingWidth) {
        listable_items.scrollLeft = remainingWidth;
      } else {
        listable_items.scrollLeft += 100;

      }
    } else {
      const remainingWidth = listable_items.scrollWidth - listable_items.offsetWidth;
      if (listable_items.scrollLeft <= 0) {
        listable_items.scrollLeft = 0;
      } else {
        listable_items.scrollLeft -= 100;
      }
    }
  });
}


export {initializeListableItems};