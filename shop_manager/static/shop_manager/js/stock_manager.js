const BANNER_TEXT = {
  ADD_STOCK: 'СЕГА ДОДАВАШ ЗАЛИХА',
  REMOVE_STOCK: 'СЕГА МИНУСИРАШ ЗАЛИХА',
}

const shouldPauseVideo = true;
window.addEventListener('load', function () {
    function onScanFailure(error) {
      // handle scan failure, if needed...
    }

    function onScanSuccess(decodedText, decodedResult) {
      console.log(`Code matched = ${decodedText}`, decodedResult);
      console.log(`Is adding stock = ${stockManagerState.isAddingStock}`);
      html5QrcodeScanner.pause(shouldPauseVideo);
    }


    const html5QrcodeScanner = new Html5QrcodeScanner(
      'qrCodeReader',
      {
        fps: 10,
        aspectRatio: 1.0,
        disableFlip: false,
        disableAutoScan: false,
        formatsToSupport: ['QR_CODE'],
        rememberLastUsedCamera: true,
        supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA],
        showTorchButtonIfSupported: true,
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

    const addStockButton = document.getElementById('stockManagerActions__addStockButton');
    const removeStockButton = document.getElementById('stockManagerActions__removeStockButton');
    const stockManagerCurrentActionBanner = document.getElementById('stockManagerCurrentActionBanner');
    const stockManagerCurrentActionBannerText = document.getElementById('stockManagerCurrentActionBanner__actionLabel');
    const scannerOverlay = document.getElementById('scanner__overlay');
    const scannedProductModal = document.getElementById('scannedProductModal');


    // document.getElementById('html5-qrcode-button-camera-stop').addEventListener('click', function () {
    //     stockManagerCurrentActionBanner.classList.add('isDoingNothing');
    //     stockManagerCurrentActionBannerText.innerText = '';
    //     stockManagerCurrentActionBanner.classList.remove('isAddingStock');
    //     stockManagerCurrentActionBanner.classList.remove('isRemovingStock');
    //     stockManagerState.isAddingStock = null;
    //   }
    // );

    const stockManagerState = {
      isAddingStock: null,
    };

    // on click add stock button
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
  }
);
