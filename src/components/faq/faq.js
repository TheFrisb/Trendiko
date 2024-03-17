function initializeFAQItems() {
  let faqItems = document.querySelectorAll('.faqItem');

  faqItems.forEach(function (faqItem) {
    let faqItemheader = faqItem.querySelector('.faqItem__header');
    faqItemheader.addEventListener('click', function () {
      let faqItemContent = faqItem.querySelector('.faqItem__content');
      faqItemContent.classList.toggle('hidden');

      let faqItemIcon = faqItemheader.querySelector('.faqItem__icon');

      if (faqItemIcon.textContent === '+') {
        faqItemIcon.textContent = '-';
      } else {
        faqItemIcon.textContent = '+';
      }
    });
  });
}

export {initializeFAQItems};