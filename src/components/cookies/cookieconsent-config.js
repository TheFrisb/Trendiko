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
      marketing: {
        enabled: true,
      }
    },
    language: {
      default: "en",
      translations: {
        en: {
          consentModal: {
            title: "Известување за колачиња",
            description: "Користиме колачиња („cookies“) за да Ви oвoзможиме да го прилагодите користењето на нашата веб-страница согласно Вашите потреби. Целта на колачињата е да Ви обезбедиме придобивки кои ќе Ви заштедат време и ќе го подобрат Вашето искуство при посета на нашата веб-страница. При користењето на нашата веб страна, Вие можете да одберете за кои категории на колачиња ни давате согласност. Доколку сакате поопширно да се информирате за нашата Политика за колачиња, <a href=\"https://trendiko.mk/brand/politika-za-privatnost-i-kolacinja/\">кликнете тука</a>.",
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
                description: "Користиме колачиња („cookies“) за да Ви oвoзможиме да го прилагодите користењето на нашата веб-страница согласно Вашите потреби. Целта на колачињата е да Ви обезбедиме придобивки кои ќе Ви заштедат време и ќе го подобрат Вашето искуство при посета на нашата веб-страница. При користењето на нашата веб страна, Вие можете да одберете за кои категории на колачиња ни давате согласност. Доколку сакате поопширно да се информирате за нашата Политика за колачиња, <a href=\"https://trendiko.mk/brand/politika-za-privatnost-i-kolacinja/\">кликнете тука</a>.",
              },
              {
                title: "Задолжителни колачиња <span class=\"pm__badge\">Задолжителни</span>",
                description: "Овие колачиња се задолжителни за правилно функционирање на нашите услуги, и не содржат лични информации.",
                linkedCategory: "necessary"
              },
              {
                title: "Маркетинг колачиња",
                description: "Овие количиња се користат за персонализација на содржината и рекламите, како и за анализа на сообраќајот на нашите сервиси.",
                linkedCategory: "marketing",
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