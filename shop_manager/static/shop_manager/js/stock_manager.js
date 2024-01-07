// eslint-disable-next-line require-jsdoc
function onScanSuccess(decodedText, decodedResult) {
  console.log(`Code matched = ${decodedText}`, decodedResult);
  html5QrcodeScanner.pause();
}

function onScanFailure(error) {
  // handle scan failure, usually better to ignore and keep scanning.
  // for example:

}

const html5QrcodeScanner = new Html5QrcodeScanner(
  'reader',
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

html5QrcodeScanner.render(onScanSuccess, onScanFailure);
