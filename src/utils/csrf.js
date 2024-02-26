function getCsrfToken() {
  const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
  return csrfTokenElement ? csrfTokenElement.value : null;
}

export {getCsrfToken};