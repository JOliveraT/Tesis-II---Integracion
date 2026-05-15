import { defineStore } from "pinia";
import bootstrap from "bootstrap/dist/js/bootstrap.min.js";
import { activateDarkMode, deactivateDarkMode } from "@/assets/js/dark-mode";

const SIDEBAR_TYPE_STORAGE_KEY = "pixelgift_sidebar_type";
const SIDEBAR_COLOR_STORAGE_KEY = "pixelgift_sidebar_color";
const DARK_MODE_STORAGE_KEY = "pixelgift_dark_mode";

const VALID_SIDEBAR_TYPES = ["bg-gradient-dark", "bg-transparent", "bg-white"];
const VALID_SIDEBAR_COLORS = ["primary", "dark", "info", "success", "warning", "danger"];

export const useAppStore = defineStore("storeId", {
  state: () => ({
    bootstrap,
    // === migrado desde el store del agregado ===
    hideConfigButton: false,
    isPinned: true,
    showConfig: false,
    //sidebarType: "bg-transparent",
    //sidebarType: "bg-white",
    sidebarType: "bg-gradient-dark",
    color: "success",
    isNavFixed: false,
    isAbsolute: false,
    showNavs: true,
    showSidenav: true,
    showNavbar: true,
    showFooter: true,
    showMain: true,
    isDarkMode: false,

    isTransparent: 'bg-transparent',
    
    

    navbarFixed:
      "position-sticky blur shadow-blur left-auto top-1 z-index-sticky px-0 mx-4",
    absolute: "position-absolute px-4 mx-0 w-100 z-index-2",
  }),

  actions: {
    hydrateVisualPreferences() {
      const savedSidebarType = localStorage.getItem(SIDEBAR_TYPE_STORAGE_KEY);
      const savedSidebarColor = localStorage.getItem(SIDEBAR_COLOR_STORAGE_KEY);
      const savedDarkMode = localStorage.getItem(DARK_MODE_STORAGE_KEY);

      if (VALID_SIDEBAR_TYPES.includes(savedSidebarType)) {
        this.sidebarType = savedSidebarType;
      }

      if (VALID_SIDEBAR_COLORS.includes(savedSidebarColor)) {
        this.setColor(savedSidebarColor);
      }

      if (savedDarkMode === "true" || savedDarkMode === "false") {
        this.setDarkMode(savedDarkMode === "true");
      }
    },

    toggleConfigurator() {
      this.showConfig = !this.showConfig;
    },

    navbarMinimize() {
      const sidenav_show = document.querySelector(".g-sidenav-show");
      if (sidenav_show?.classList.contains("g-sidenav-pinned")) {
        sidenav_show.classList.remove("g-sidenav-pinned");
        this.isPinned = false;
      } else {
        sidenav_show?.classList.add("g-sidenav-pinned");
        this.isPinned = true;
      }
    },

    navbarFixed() {
      this.isNavFixed = !this.isNavFixed;
    },

    toggleNavbarFixed() {
      this.isNavFixed = !this.isNavFixed;
    },

    toggleEveryDisplay() {
      this.showNavbar = !this.showNavbar;
      this.showSidenav = !this.showSidenav;
      this.showFooter = !this.showFooter;
    },

    toggleHideConfig() {
      this.hideConfigButton = !this.hideConfigButton;
    },

    setColor(payload) {
      if (!VALID_SIDEBAR_COLORS.includes(payload)) return;
      this.color = payload;
      localStorage.setItem(SIDEBAR_COLOR_STORAGE_KEY, payload);
    },

    setSidebarType(payload) {
      if (!VALID_SIDEBAR_TYPES.includes(payload)) return;
      this.sidebarType = payload;
      localStorage.setItem(SIDEBAR_TYPE_STORAGE_KEY, payload);
    },

    setDarkMode(payload) {
      this.isDarkMode = Boolean(payload);
      if (this.isDarkMode) {
        activateDarkMode();
      } else {
        deactivateDarkMode();
      }
      localStorage.setItem(DARK_MODE_STORAGE_KEY, String(this.isDarkMode));
    },

    darkMode() {
      this.setDarkMode(!this.isDarkMode);
    },
  },
});
