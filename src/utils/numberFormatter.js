// format number to user locale
function formatNumberToLocale(number) {

  return number.toLocaleString('en-US');
}

function parseLocaleNumber(number) {
  return parseInt(number.replace(/,/g, ''));
}

export {formatNumberToLocale, parseLocaleNumber};