import {tns} from "tiny-slider";

function initProductPageMainSlider() {
  const productGalleryContainer = document.getElementById('productGallery');

  if (!productGalleryContainer) {
    return;
  }

  let slider = tns({
    container: '#productGallery',
    items: 1,
    slideBy: 1,
    autoplay: false,
    nav: false,

    controls: false,
    navAsThumbnails: false,
    mouseDrag: true,
  });
}

export {initProductPageMainSlider};