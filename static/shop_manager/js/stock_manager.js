const BANNER_TEXT = {
  ADD_STOCK: 'СЕГА ДОДАВАШ ЗАЛИХА',
  REMOVE_STOCK: 'СЕГА МИНУСИРАШ ЗАЛИХА',
}

const MODAL_TEXT = {
  ADD_STOCK: 'Додади залиха на',
  REMOVE_STOCK: 'Минусирај залиха од',
}

const notyf = new Notyf();
const CSRF_TOKEN = document.querySelector('[name=csrfmiddlewaretoken]').value;

function retrieveProductByCode(code) {
  return fetch(`/api/stock/stock-item/${code}`)
    .then(response => {
      if (!response.ok) {
        return response.json().then(errData => {
          return Promise.reject({status: response.status, data: errData});
        });
      }
      return response.json();
    })
    .then(data => {
      return data;
    })
}

function updateStockItem(sku, isAddingStock) {
  if (isAddingStock === null) {
    notyf.error('Please choose an action first!');
    return Promise.reject('Please choose an action first!');
  }

  const action = isAddingStock ? 'ADD' : 'REMOVE';
  return fetch(`/api/stock/manage-stock-item/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': CSRF_TOKEN,
    },
    body: JSON.stringify({
      sku: sku,
      action: action,
    })
  })
    .then(response => {
      if (!response.ok) {
        return response.json().then(errData => {
          return Promise.reject({status: response.status, data: errData});
        });
      }
      return response.json();
    })
    .then(data => {

      return data;
    })
    .catch(error => {

      console.error('There was a problem with the fetch operation: ', error);
      throw error;
    });
}


function toggleElement(element) {
  element.classList.toggle('isDoingNothing');
}

const shouldPauseVideo = true;
window.addEventListener('load', function () {
    const addStockButton = document.getElementById('stockManagerActions__addStockButton');
    const removeStockButton = document.getElementById('stockManagerActions__removeStockButton');
    const stockManagerCurrentActionBanner = document.getElementById('stockManagerCurrentActionBanner');
    const stockManagerCurrentActionBannerText = document.getElementById('stockManagerCurrentActionBanner__actionLabel');
    const scannedProductModalConfirmButton = document.getElementById('scannedProductModal__confirmActionButton');
    const scannedProductModalCancelButton = document.getElementById('scannedProductModal__cancelActionButton');
    const scannedProductModal = document.getElementById('scannedProductModal');
    const scannerOverlay = document.getElementById('scanner__overlay');


    function populateScannedProductModal(product) {
      const scannedProductCurrentActionLabel = document.getElementById('scannedProductModal__currentActionLabel');
      const scannedProductModalLabel = document.getElementById('scannedProductModal__label');
      const scannedProductModalThumbnail = document.getElementById('scannedProductModal__thumbnail');

      scannedProductModalLabel.innerText = product.label;
      scannedProductModalThumbnail.src = product.thumbnail;
      scannedProductCurrentActionLabel.innerText = stockManagerState.isAddingStock ? MODAL_TEXT.ADD_STOCK : MODAL_TEXT.REMOVE_STOCK;
      scannedProductCurrentActionLabel.classList.remove('text-red-600')
      scannedProductCurrentActionLabel.classList.remove('text-green-600')
      scannedProductCurrentActionLabel.classList.add(stockManagerState.isAddingStock ? 'text-green-600' : 'text-red-600');

      toggleElement(scannedProductModal);
      console.log('Showing modal');
    }

    // retrieveProductByCode("awdawd").then(data => {
    //   initReader();
    //   console.log(data)
    //   populateScannedProductModal(data);
    // }).catch(err => {
    //   console.log(err);
    // })

    function onScanFailure(error) {
      // handle scan failure, if needed...
    }

    function onScanSuccess(decodedText, decodedResult) {
      console.log(`Code matched = ${decodedText}`, decodedResult);
      console.log(`Is adding stock = ${stockManagerState.isAddingStock}`);
      // stockManagerState.currentSku = decodedText;
      html5QrcodeScanner.pause(shouldPauseVideo);
      toggleElement(scannerOverlay);

      retrieveProductByCode(stockManagerState.currentSku).then(data => {
        stockManagerState.currentSku = data.sku;
        populateScannedProductModal(data);
      }).catch(error => {
        if (error.status && error.data) {
          if (error.status === 400) {
            notyf.error(error.data.detail);
            return;
          }
          const messages = Object.keys(error.data).map(key => error.data[key]);
          messages.forEach(message => {
            notyf.error(message);
          });
        } else {
          notyf.error('An unexpected error occurred');
        }

      })
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


    const stockManagerState = {
      isAddingStock: false,
      currentSku: "awdawd",
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

    // on click confirm button
    scannedProductModalConfirmButton.addEventListener('click', function () {
      console.log(`Confirming action for SKU ${stockManagerState.currentSku}`);

      updateStockItem(stockManagerState.currentSku, stockManagerState.isAddingStock).then(data => {
        notyf.success('Stock updated successfully!');
        stockManagerState.currentSku = null;
        toggleElement(scannerOverlay);
        toggleElement(scannedProductModal);
        html5QrcodeScanner.resume();

      })
        .catch(error => {
          console.error('Error:', error);

          if (error.status && error.data) {
            if (error.status === 400) {
              notyf.error(error.data.detail);
              return;
            }
            const messages = Object.keys(error.data).map(key => error.data[key]);
            messages.forEach(message => {
              notyf.error(message);
            });
          } else {
            notyf.error('An unexpected error occurred');
          }
        });
    });

    scannedProductModalCancelButton.addEventListener('click', function () {
      console.log(`Canceling action for SKU ${stockManagerState.currentSku}`);
      stockManagerState.currentSku = null;
      toggleElement(scannerOverlay);
      toggleElement(scannedProductModal);
      html5QrcodeScanner.resume();
      

    });

  }
);
