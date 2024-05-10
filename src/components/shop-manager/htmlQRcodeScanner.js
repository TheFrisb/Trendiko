import {notyf__short} from "../../utils/error";
import {HTTP} from "../../http/client";
import {ADMIN_URLS} from "../../http/adminURLS";
import {Html5QrcodeScanner, Html5QrcodeScannerState, Html5QrcodeScanType} from "html5-qrcode";

const notyf = notyf__short;
const scannedProductCurrentActionLabel = document.getElementById('scannedProductModal__currentActionLabel');
const scannedProductModalLabel = document.getElementById('scannedProductModal__label');
const scannedProductModalThumbnail = document.getElementById('scannedProductModal__thumbnail');
const addStockButton = document.getElementById('stockManagerActions__addStockButton');
const removeStockButton = document.getElementById('stockManagerActions__removeStockButton');
const stockManagerCurrentActionBanner = document.getElementById('stockManagerCurrentActionBanner');
const stockManagerCurrentActionBannerText = document.getElementById('stockManagerCurrentActionBanner__actionLabel');
const scannedProductModalConfirmButton = document.getElementById('scannedProductModal__confirmActionButton');
const scannedProductModalCancelButton = document.getElementById('scannedProductModal__cancelActionButton');
const scannedProductModal = document.getElementById('scannedProductModal');
const scannerOverlay = document.getElementById('scanner__overlay');
const shouldPauseVideo = true;

const BANNER_TEXT = {
  ADD_STOCK: 'СЕГА ДОДАВАШ ЗАЛИХА',
  REMOVE_STOCK: 'СЕГА МИНУСИРАШ ЗАЛИХА',
}
const MODAL_TEXT = {
  ADD_STOCK: 'Додади залиха на',
  REMOVE_STOCK: 'Минусирај залиха од',
}
const stockManagerState = {
  isAddingStock: false,
  currentSku: "",
};


function retrieveProductByCode(code) {
  return HTTP.get(`${ADMIN_URLS.RETRIEVE_PRODUCT_BY_CODE}${code}`).then(response => {
    return response;
  });
}

function updateStockItem(sku, isAddingStock) {
  if (isAddingStock === null) {
    notyf.error('Please choose an action first!');
    return Promise.reject('Please choose an action first!');
  }

  const action = isAddingStock ? 'ADD' : 'REMOVE';
  let data = {
    sku: sku,
    action: action,
  }

  return HTTP.post(ADMIN_URLS.UPDATE_STOCK_ITEM, data).then(response => {
    return response;
  });
}


function toggleElement(element) {
  element.classList.toggle('isDoingNothing');
}

function populateScannedProductModal(product) {
  scannedProductModalLabel.innerText = product.label;
  scannedProductModalThumbnail.src = product.thumbnail;
  scannedProductCurrentActionLabel.innerText = stockManagerState.isAddingStock ? MODAL_TEXT.ADD_STOCK : MODAL_TEXT.REMOVE_STOCK;
  scannedProductCurrentActionLabel.classList.remove('text-red-600')
  scannedProductCurrentActionLabel.classList.remove('text-green-600')
  scannedProductCurrentActionLabel.classList.add(stockManagerState.isAddingStock ? 'text-green-600' : 'text-red-600');

  toggleElement(scannedProductModal);
}


function initializeQRScanner() {
  if (!document.getElementById('qrCodeReader')) {
    return;
  }

  function onScanFailure(error) {
    // handle scan failure, if needed...
  }

  function onScanSuccess(decodedText, decodedResult) {
    console.log(`Code matched = ${decodedText}`, decodedResult);
    console.log(`Is adding stock = ${stockManagerState.isAddingStock}`);
    stockManagerState.currentSku = decodedText;
    html5QrcodeScanner.pause(shouldPauseVideo);
    toggleElement(scannerOverlay);

    retrieveProductByCode(decodedText).then(response => {
      if (response.success) {
        let product = response.data;
        populateScannedProductModal(product);
      } else {
        let status_code = response.status;
        if (status_code === 404) {
          notyf.error('Stock Item not found');
        } else {
          notyf.error('An unexpected error occurred');
        }

        stockManagerState.currentSku = null;
        toggleElement(scannerOverlay);
        html5QrcodeScanner.resume();
      }

    });
  }


  const html5QrcodeScanner = new Html5QrcodeScanner(
    'qrCodeReader',
    {
      fps: 60,
      aspectRatio: 2.0,
      disableFlip: false,
      formatsToSupport: ['QR_CODE'],
      rememberLastUsedCamera: true,
      supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA],
      showTorchButtonIfSupported: true,
      showZoomSliderIfSupported: true,
      defaultZoomValueIfSupported: 2,
      qrbox: 250,
      facingMode: {exact: "environment"},
      focusMode: "continuous",
      useBarCodeDetectorIfSupported: true,
    },
    /* verbose= */ false);

  function initReader() {
    if (stockManagerState.isAddingStock === null) {
      alert("Please choose an action first!");
      return;
    }
    try {
      if (html5QrcodeScanner.getState() === Html5QrcodeScannerState.PAUSED) {
        console.log('Resuming scanner');
        html5QrcodeScanner.resume();
      }
    } catch (err) {
      console.log(err);
      html5QrcodeScanner.render(onScanSuccess, onScanFailure);
    }

  }

  addStockButton.addEventListener('click', function () {
    stockManagerCurrentActionBannerText.innerText = BANNER_TEXT.ADD_STOCK;

    stockManagerCurrentActionBanner.classList.remove('isDoingNothing');
    stockManagerCurrentActionBanner.classList.remove('isRemovingStock');

    stockManagerCurrentActionBanner.classList.add('isAddingStock');
    stockManagerState.isAddingStock = true;

    if (!html5QrcodeScanner.isScanning) {
      initReader();
    }
  });

  // on click remove stock button

  removeStockButton.addEventListener('click', function () {
    stockManagerCurrentActionBannerText.innerText = BANNER_TEXT.REMOVE_STOCK;

    stockManagerCurrentActionBanner.classList.remove('isDoingNothing');
    stockManagerCurrentActionBanner.classList.remove('isAddingStock');

    stockManagerCurrentActionBanner.classList.add('isRemovingStock');
    stockManagerState.isAddingStock = false;

    if (!html5QrcodeScanner.isScanning) {
      initReader();
    }
  });

  // on click confirm button
  scannedProductModalConfirmButton.addEventListener('click', function () {
    console.log(`Confirming action for SKU ${stockManagerState.currentSku}`);

    updateStockItem(stockManagerState.currentSku, stockManagerState.isAddingStock).then(response => {
      if (response.success) {
        notyf.success('Stock updated successfully');
      } else {
        let status_code = response.status;
        // if 404 else if 400 else
        if (status_code === 404) {
          notyf.error(`Stock Item not found`);
        } else if (status_code === 403) {
          notyf.error(response.data.message);
        } else if (status_code === 400) {
          notyf.error(response.data.detail);
        } else {
          notyf.error('An unexpected error occurred');
        }
      }
      stockManagerState.currentSku = null;
      toggleElement(scannerOverlay);
      toggleElement(scannedProductModal);
    }).finally(() => {
      html5QrcodeScanner.resume();
    });
  });

  scannedProductModalCancelButton.addEventListener('click', function () {
    stockManagerState.currentSku = null;
    toggleElement(scannerOverlay);
    toggleElement(scannedProductModal);
    html5QrcodeScanner.resume();
  });

}

export {initializeQRScanner};
