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
    nav: true,


    controls: true,
    navAsThumbnails: true,
    mouseDrag: true,
  });
}

export {initProductPageMainSlider};