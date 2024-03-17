import {tns} from "tiny-slider";

function makeSliderButtons(iconSize) {
  let prevButton = `<svg xmlns="http://www.w3.org/2000/svg" width="${iconSize}" height="${iconSize}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-left"><path d="m15 18-6-6 6-6"/></svg>`
  let nextButton = `<svg xmlns="http://www.w3.org/2000/svg" width="${iconSize}" height="${iconSize}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-right"><path d="m9 18 6-6-6-6"/></svg>`
  return [prevButton, nextButton];
}

function initProductPageMainSlider() {
  const productGalleryContainer = document.getElementById('productGallery');
  if (!productGalleryContainer) {
    return;
  }

  const images = productGalleryContainer.querySelectorAll('img');
  const thumbnailsContainer = document.getElementById('productGallery__Thumbnails');
  initializeSlider();

  function initializeSlider() {
    let slider = tns({
      container: '#productGallery',
      items: 1,
      slideBy: 1,
      autoplay: false,
      nav: true,
      navPosition: 'bottom',
      navAsThumbnails: true,
      controls: true,
      controlsText: makeSliderButtons(28),
      mouseDrag: true,
      preventScrollOnTouch: 'auto',
    });

    // if tablet or desktop screen, make thumbnails
    if (window.innerWidth > 768) {
      makeThumbnails(slider);
    }
  }

  function makeThumbnails(slider) {
    images.forEach((image, index) => {
      let thumbnailDiv = document.createElement('div');
      let pictureEl = document.createElement('picture');
      let sourceEl = document.createElement('source');
      let imgEl = document.createElement('img');
      thumbnailDiv.classList.add('productGallery__Thumbnail');
      thumbnailDiv.dataset.index = index;
      thumbnailDiv.classList.add('productGallery__Thumbnail');
      sourceEl.srcset = image.src;
      imgEl.src = image.src;
      imgEl.alt = image.alt;
      imgEl.width = 50;
      imgEl.height = 50;
      imgEl.classList.add('productGallery__ThumbnailImage');
      pictureEl.appendChild(sourceEl);
      pictureEl.appendChild(imgEl);
      thumbnailDiv.appendChild(pictureEl);
      thumbnailsContainer.appendChild(thumbnailDiv);

      thumbnailDiv.addEventListener('click', () => {
        slider.goTo(index);
      });
    });
    thumbnailsContainer.classList.remove('hidden')
  }
}

export {initProductPageMainSlider};