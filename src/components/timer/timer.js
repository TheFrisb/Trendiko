const timers = document.querySelectorAll('.countdownByMinutesAndSeconds');
const buttonsToDisable = document.querySelectorAll('.canBeDisabledByTimerBtn');

function makeCountDownByMinutesAndSeconds() {
  timers.forEach(timer => {
    let parts = timer.innerHTML.split(':');
    let minutes = parseInt(parts[0]);
    let seconds = parseInt(parts[1]);
    let totalSeconds = minutes * 60 + seconds;
    let interval = setInterval(() => {
      totalSeconds--;
      if (totalSeconds <= 0) {
        disableButtons();
        clearInterval(interval);
      }
      minutes = Math.floor(totalSeconds / 60);
      seconds = totalSeconds % 60;
      timer.innerHTML = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }, 1000);

  })
}


function disableButtons() {
  buttonsToDisable.forEach(button => {
    button.disabled = true;
    let buttonText = button.getAttribute('data-disabled-text');
    if (buttonText) {
      button.querySelector('.buttonText').innerHTML = buttonText;
    }
  });
}


export {makeCountDownByMinutesAndSeconds};