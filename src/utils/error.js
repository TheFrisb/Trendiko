import {Notyf} from "notyf";

let notyf__long = new Notyf(
  {
    duration: 10000,
    ripple: true,
    position: {
      x: 'left',
      y: 'bottom',
    },
    dismissible: true,

  }
);

let notyf__short = new Notyf(
  {
    duration: 5000,
    ripple: true,
    position: {
      x: 'left',
      y: 'top',
    },
    dismissible: true,

  }
);

export {notyf__long, notyf__short};