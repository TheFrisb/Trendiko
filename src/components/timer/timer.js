const timers = document.querySelectorAll('.countdownByMinutesAndSeconds');

function makeCountDownByMinutesAndSeconds() {
  timers.forEach(timer => {
    let parts = timer.innerHTML.split(':');
    let minutes = parseInt(parts[0]);
    let seconds = parseInt(parts[1]);
    let totalSeconds = minutes * 60 + seconds;
    let interval = setInterval(() => {
      totalSeconds--;
      if (totalSeconds <= 0) {
        clearInterval(interval);
      }
      minutes = Math.floor(totalSeconds / 60);
      seconds = totalSeconds % 60;
      timer.innerHTML = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }, 1000);

  })
}

export {makeCountDownByMinutesAndSeconds};