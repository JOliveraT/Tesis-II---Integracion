import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import { useAppStore } from "./stores";

// Nucleo Icons
import "./assets/css/nucleo-icons.css";
import "./assets/css/nucleo-svg.css";

import materialKit from "./material-kit";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(materialKit);

const appStore = useAppStore(pinia);
appStore.hydrateVisualPreferences();

app.mount("#app");
