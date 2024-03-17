import autoComplete from "@tarekraafat/autocomplete.js/dist/autoComplete";
import {notyf__short} from "../../utils/error";

let checkoutCity = document.getElementById('checkoutForm__city');
let municipalityContainer = document.getElementById('checkoutForm__municipalityContainer');
let municipalityInput = document.getElementById('checkoutForm__municipality');

const cityAutocompleteJs = new autoComplete({
  selector: "#checkoutForm__city",
  placeHolder: "Одбери град",
  data: {
    src: [
      {"latin": "Aerodrom", "cyrillic": "Аеродром"},
      {"latin": "Aracinovo", "cyrillic": "Арачиново"},
      {"latin": "Berovo", "cyrillic": "Берово"},
      {"latin": "Bitola", "cyrillic": "Битола"},
      {"latin": "Bogdanci", "cyrillic": "Богданци"},
      {"latin": "Butel", "cyrillic": "Бутел"},
      {"latin": "Valandovo", "cyrillic": "Валандово"},
      {"latin": "Veles", "cyrillic": "Велес"},
      {"latin": "Vinica", "cyrillic": "Виница"},
      {"latin": "Gazi Baba", "cyrillic": "Гази Баба"},
      {"latin": "Gevgelija", "cyrillic": "Гевгелија"},
      {"latin": "Gostivar", "cyrillic": "Гостивар"},
      {"latin": "Debar", "cyrillic": "Дебар"},
      {"latin": "Delcevo", "cyrillic": "Делчево"},
      {"latin": "Demir Kapija", "cyrillic": "Демир Капија"},
      {"latin": "Demir Hisar", "cyrillic": "Демир Хисар"},
      {"latin": "Dojran", "cyrillic": "Дојран"},
      {"latin": "Gjorce Petrov", "cyrillic": "Ѓорче Петров"},
      {"latin": "Zelenikovo", "cyrillic": "Зелениково"},
      {"latin": "Ilinden", "cyrillic": "Илинден"},
      {"latin": "Kavadarci", "cyrillic": "Кавадарци"},
      {"latin": "Karpos", "cyrillic": "Карпош"},
      {"latin": "Kisela Voda", "cyrillic": "Кисела Вода"},
      {"latin": "Kichevo", "cyrillic": "Кичево"},
      {"latin": "Kocani", "cyrillic": "Кочани"},
      {"latin": "Kratovo", "cyrillic": "Кратово"},
      {"latin": "Kriva Palanka", "cyrillic": "Крива Паланка"},
      {"latin": "Krusevo", "cyrillic": "Крушево"},
      {"latin": "Kumanovo", "cyrillic": "Куманово"},
      {"latin": "Mavrovo", "cyrillic": "Маврово"},
      {"latin": "Makedonska Kamenica", "cyrillic": "Македонска Каменица"},
      {"latin": "Makedonski Brod", "cyrillic": "Македонски Брод"},
      {"latin": "Negotino", "cyrillic": "Неготино"},
      {"latin": "Ohrid", "cyrillic": "Охрид"},
      {"latin": "Petrovec", "cyrillic": "Петровец"},
      {"latin": "Pehcevo", "cyrillic": "Пехчево"},
      {"latin": "Prilep", "cyrillic": "Прилеп"},
      {"latin": "Probistip", "cyrillic": "Пробиштип"},
      {"latin": "Radovis", "cyrillic": "Радовиш"},
      {"latin": "Resen", "cyrillic": "Ресен"},
      {"latin": "Saraj", "cyrillic": "Сарај"},
      {"latin": "Sveti Nikole", "cyrillic": "Свети Николе"},
      {"latin": "Skopje", "cyrillic": "Скопје"},
      {"latin": "Sopiste", "cyrillic": "Сопиште"},
      {"latin": "Struga", "cyrillic": "Струга"},
      {"latin": "Strumica", "cyrillic": "Струмица"},
      {"latin": "Studenicani", "cyrillic": "Студеничани"},
      {"latin": "Tetovo", "cyrillic": "Тетово"},
      {"latin": "Centar", "cyrillic": "Центар"},
      {"latin": "Cair", "cyrillic": "Чаир"},
      {"latin": "Cucer Sandevo", "cyrillic": "Чучер-Сандево"},
      {"latin": "Stip", "cyrillic": "Штип"},
      {"latin": "Suto Orizari", "cyrillic": "Шуто Оризари"}
    ],
    keys: ["latin", "cyrillic"]

  },
  resultItem: {
    highlight: true,
  },
  events: {
    input: {
      selection: (event) => {
        const selection = event.detail.selection.value.latin;
        cityAutocompleteJs.input.value = selection;

        if (selection === "Skopje") {
          municipalityContainer.classList.remove("hidden");
          municipalityInput.setAttribute("required", "required");
          municipalityInput.removeAttribute("disabled")
        } else {
          municipalityContainer.classList.add("hidden");
          municipalityInput.removeAttribute("required");
          municipalityInput.setAttribute("disabled", "disabled");
        }
      },
      focus() {
        const inputValue = cityAutocompleteJs.input.value;

        if (inputValue.length) cityAutocompleteJs.start();
      },
      blur: () => { // Adding a blur event
        const inputValue = cityAutocompleteJs.input.value;
        const options = cityAutocompleteJs.data.src;
        let isValidOption = false;

        for (let option of options) {
          if (inputValue === option.latin || inputValue === option.cyrillic) {
            isValidOption = true;
            break;
          }
        }


        if (!isValidOption && cityAutocompleteJs.input.value.length > 0) {
          cityAutocompleteJs.input.value = '';
          notyf__short.error('Ве молиме одберете град од листата');
          cityAutocompleteJs.close();
        }

      },
    }
  },
  threshold: 0,
  resultsList: {
    noResults: true,
  },

});


const municipalityAutocompleteJs = new autoComplete({
  selector: "#checkoutForm__municipality",
  placeHolder: "Одбери општина",
  data: {
    src: [
      {"latin": "Aerodrom", "cyrillic": "Аеродром"},
      {"latin": "Aracinovo", "cyrillic": "Арачиново"},
      {"latin": "Berovo", "cyrillic": "Берово"},
      {"latin": "Bitola", "cyrillic": "Битола"},
      {"latin": "Bogdanci", "cyrillic": "Богданци"},
      {"latin": "Butel", "cyrillic": "Бутел"},
      {"latin": "Valandovo", "cyrillic": "Валандово"},
      {"latin": "Veles", "cyrillic": "Велес"},
      {"latin": "Vinica", "cyrillic": "Виница"},
      {"latin": "Gazi Baba", "cyrillic": "Гази Баба"},
      {"latin": "Gevgelija", "cyrillic": "Гевгелија"},
      {"latin": "Gostivar", "cyrillic": "Гостивар"},
      {"latin": "Debar", "cyrillic": "Дебар"},
      {"latin": "Delcevo", "cyrillic": "Делчево"},
      {"latin": "Demir Kapija", "cyrillic": "Демир Капија"},
      {"latin": "Demir Hisar", "cyrillic": "Демир Хисар"},
      {"latin": "Dojran", "cyrillic": "Дојран"},
      {"latin": "Gjorce Petrov", "cyrillic": "Ѓорче Петров"},
      {"latin": "Zelenikovo", "cyrillic": "Зелениково"},
      {"latin": "Ilinden", "cyrillic": "Илинден"},
      {"latin": "Kavadarci", "cyrillic": "Кавадарци"},
      {"latin": "Karpos", "cyrillic": "Карпош"},
      {"latin": "Kisela Voda", "cyrillic": "Кисела Вода"},
      {"latin": "Kichevo", "cyrillic": "Кичево"},
      {"latin": "Kocani", "cyrillic": "Кочани"},
      {"latin": "Kratovo", "cyrillic": "Кратово"},
      {"latin": "Kriva Palanka", "cyrillic": "Крива Паланка"},
      {"latin": "Krusevo", "cyrillic": "Крушево"},
      {"latin": "Kumanovo", "cyrillic": "Куманово"},
      {"latin": "Mavrovo", "cyrillic": "Маврово"},
      {"latin": "Makedonska Kamenica", "cyrillic": "Македонска Каменица"},
      {"latin": "Makedonski Brod", "cyrillic": "Македонски Брод"},
      {"latin": "Negotino", "cyrillic": "Неготино"},
      {"latin": "Ohrid", "cyrillic": "Охрид"},
      {"latin": "Petrovec", "cyrillic": "Петровец"},
      {"latin": "Pehcevo", "cyrillic": "Пехчево"},
      {"latin": "Prilep", "cyrillic": "Прилеп"},
      {"latin": "Probistip", "cyrillic": "Пробиштип"},
      {"latin": "Radovis", "cyrillic": "Радовиш"},
      {"latin": "Resen", "cyrillic": "Ресен"},
      {"latin": "Saraj", "cyrillic": "Сарај"},
      {"latin": "Sveti Nikole", "cyrillic": "Свети Николе"},
      {"latin": "Skopje", "cyrillic": "Скопје"},
      {"latin": "Sopiste", "cyrillic": "Сопиште"},
      {"latin": "Struga", "cyrillic": "Струга"},
      {"latin": "Strumica", "cyrillic": "Струмица"},
      {"latin": "Studenicani", "cyrillic": "Студеничани"},
      {"latin": "Tetovo", "cyrillic": "Тетово"},
      {"latin": "Centar", "cyrillic": "Центар"},
      {"latin": "Cair", "cyrillic": "Чаир"},
      {"latin": "Cucer Sandevo", "cyrillic": "Чучер-Сандево"},
      {"latin": "Stip", "cyrillic": "Штип"},
      {"latin": "Suto Orizari", "cyrillic": "Шуто Оризари"}
    ],
    keys: ["latin", "cyrillic"]

  },
  resultItem: {
    highlight: true,
  },
  events: {
    input: {
      selection: (event) => {
        const selection = event.detail.selection.value.latin;
        municipalityAutocompleteJs.input.value = selection;
      },
      focus() {
        const inputValue = municipalityAutocompleteJs.input.value;
        if (inputValue.length) municipalityAutocompleteJs.start();
      },
      blur: () => { // Adding a blur event
        const inputValue = municipalityAutocompleteJs.input.value;
        const options = municipalityAutocompleteJs.data.src;
        let isValidOption = false;

        for (let option of options) {
          if (inputValue === option.latin || inputValue === option.cyrillic) {
            isValidOption = true;
            break;
          }
        }


        if (!isValidOption && municipalityAutocompleteJs.input.value.length > 0) {
          municipalityAutocompleteJs.input.value = '';
          notyf__short.error('Ве молиме одберете општина од листата');
          municipalityAutocompleteJs.close();
        }

      },
    }
  },
  threshold: 0,
  resultsList: {
    noResults: true,
  },

});


function initCheckoutCityListeners() {
  if (checkoutCity) {
    cityAutocompleteJs.init();

  }
}

export {initCheckoutCityListeners};