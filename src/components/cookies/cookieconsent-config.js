import * as CookieConsent from "vanilla-cookieconsent";

function initializeCookieConsent() {
  CookieConsent.run({
    guiOptions: {
      consentModal: {
        layout: "cloud inline",
        position: "bottom center",
        equalWeightButtons: true,
        flipButtons: false
      },
      preferencesModal: {
        layout: "bar",
        position: "right",
        equalWeightButtons: true,
        flipButtons: false
      }
    },
    categories: {
      necessary: {
        readOnly: true
      },
      marketing: {}
    },
    language: {
      default: "en",
      translations: {
        en: {
          consentModal: {
            title: "Известување за колачиња",
            description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            closeIconLabel: "",
            acceptAllBtn: "Прифати ги сите",
            acceptNecessaryBtn: "Одбиј ги сите",
            showPreferencesBtn: "Поднеси поставки",
            footer: "<a href=\"https://trendiko.mk/brand/politika-za-privatnost-i-kolacinja/\">Политика на приватност</a>\n<a href=\"https://trendiko.mk/brand/pravila-za-koristenje/\">Правила на користење</a>"
          },
          preferencesModal: {
            title: "Поднесување поставки",
            closeIconLabel: "Close modal",
            acceptAllBtn: "Прифати ги сите",
            acceptNecessaryBtn: "Одбиј ги сите",
            savePreferencesBtn: "Зачуви поставки",
            serviceCounterLabel: "Service|Services",
            sections: [
              {
                title: "Користење на колачиња",
                description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
              },
              {
                title: "Задолжителни колачиња <span class=\"pm__badge\">Задолжителни</span>",
                description: "Овие колачиња се задолжителни за правилно функционирање на нашите услуги, и не содржат лични информации.",
                linkedCategory: "necessary"
              },
              {
                title: "Маркетинг колачиња",
                description: "Lorem mollis aliquam ut porttitor leo a. Pharetra diam sit amet nisl suscipit adipiscing bibendum est. Ut aliquam purus sit amet. Senectus et netus et malesuada fames ac turpis. Adipiscing elit duis tristique sollicitudin nibh sit amet. Lacinia at quis risus sed vulputate odio ut enim blandit. Sed elementum tempus egestas sed sed. Quam pellentesque nec nam aliquam. Quam pellentesque nec nam aliquam sem et tortor. At risus viverra adipiscing at. Potenti nullam ac tortor vitae purus faucibus ornare suspendisse sed. Eu turpis egestas pretium aenean pharetra. Sapien nec sagittis aliquam malesuada bibendum arcu. Volutpat sed cras ornare arcu dui vivamus arcu felis bibendum. Cras fermentum odio eu feugiat.",
                linkedCategory: "marketing"
              }
            ]
          }
        }
      }
    },
    disablePageInteraction: true
  });
}

export {initializeCookieConsent};