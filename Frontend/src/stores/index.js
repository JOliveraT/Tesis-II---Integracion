import { defineStore } from "pinia";
import bootstrap from "bootstrap/dist/js/bootstrap.min.js";

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
      this.color = payload;
    },
    darkMode() {
      this.isDarkMode = !this.isDarkMode;
      if (this.isDarkMode) {
        activateDarkMode();
      } else {
        deactivateDarkMode();
      }
    },
  },
});
