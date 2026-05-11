<script>
import { useAppStore } from "@/stores";
import { activateDarkMode, deactivateDarkMode } from "@/assets/js/dark-mode";

export default {
  name: "configurator",
  props: ["toggle"],
  setup() {
    // Acceso al store de Pinia
    const store = useAppStore();

    // Métodos
    const toggle = () => {
      store.toggleConfigurator();
    };

    const sidebarColor = (color = "success") => {
      document.querySelector("#sidenav-main").setAttribute("data-color", color);
      store.setColor(color);  // Cambiar color del sidebar
    };

    const sidebar = (type) => {
      //store.setSidebarType(type); // Cambiar el tipo de sidebar
      store.sidebarType = type;
       // ahora, actualizamos el DOM manualmente
      const sidenav = document.querySelector("#sidenav-main");

    if (sidenav) {
      sidenav.classList.remove("bg-white", "bg-transparent", "bg-gradient-dark"); // quitamos todas
      sidenav.classList.add(type); // agregamos la nueva
      }
      // Luego manejamos las clases de color de texto
    const links = sidenav.querySelectorAll("a, span, h6, p"); // o los elementos que quieras afectar

      if (type === "bg-gradient-dark") {
        sidenav.classList.remove("text-dark");
        sidenav.classList.add("text-white");

        links.forEach((el) => {
          el.classList.remove("text-dark");
          el.classList.add("text-white");
        });
      } else {
        sidenav.classList.remove("text-white");
        sidenav.classList.add("text-dark");

        links.forEach((el) => {
          el.classList.remove("text-white");
          el.classList.add("text-dark");
        });
      }
    };

    const setNavbarFixed = () => {
      if (
        store.currentRoute !== "Profile" || // Validación de la ruta
        store.currentRoute !== "All Projects"
      ) {
        store.toggleNavbarFixed();  // Toggle navbar fijo
      }
    };

    const darkMode = () => {
      if (store.isDarkMode) {
        store.isDarkMode = false;
        deactivateDarkMode(); // Desactivar modo oscuro
      } else {
        store.isDarkMode = true;
        activateDarkMode(); // Activar modo oscuro
      }
    };

    const sidenavTypeOnResize = () => {
      let transparent = document.querySelector("#btn-transparent");
      let white = document.querySelector("#btn-white");
      if (window.innerWidth < 1200) {
        transparent.classList.add("disabled");
        white.classList.add("disabled");
      } else {
        transparent.classList.remove("disabled");
        white.classList.remove("disabled");
      }
    };

    return {
      store,
      toggle,
      sidebarColor,
      sidebar,
      darkMode,
      sidenavTypeOnResize,
    };
  },
  computed: {
    isConfigVisible() {
      return this.store.showConfig;  // Estado de la visibilidad del configurador
    },
    isDarkModeChecked() {
      return this.store.isDarkMode;  // Estado de modo oscuro
    },
    sidenavResponsive() {
      return this.sidenavTypeOnResize;  // Responsividad del sidenav
    },
  },
  beforeMount() {
    this.store.isTransparent = "bg-transparent"; // Configuración de fondo transparente
    window.addEventListener("resize", this.sidenavTypeOnResize); // Escuchar el cambio de tamaño de ventana
    window.addEventListener("load", this.sidenavTypeOnResize); // Escuchar el evento de carga
  },
};
</script>

<template>
  <div class="fixed-plugin">
    <a
      class="px-3 py-2 fixed-plugin-button text-dark position-fixed"
      @click="toggle"
    >
      <i class="material-icons py-2">settings</i>
    </a>
    <div class="shadow-lg card">
      <div class="pt-3 pb-0 bg-transparent card-header">
        <div class="float-start">
          <h5 class="mt-3 mb-0">Configurador</h5>
          <p>Explora las opciones de dashboard.</p>
        </div>
        <div class="mt-4 float-end" @click="toggle">
          <button class="p-0 btn btn-link text-dark fixed-plugin-close-button">
            <i class="material-icons">clear</i>
          </button>
        </div>
        <!-- End Toggle Button -->
      </div>
      <hr class="my-1 horizontal dark" />
      <div class="pt-0 card-body pt-sm-3">
        <!-- Sidebar Backgrounds -->
        <div>
          <h6 class="mb-0">Colores de la barra lateral</h6>
        </div>
        <a href="#" class="switch-trigger background-color">
          <div
            class="my-2 badge-colors text-start"
          >
            <span
              class="badge filter bg-gradient-primary"
              data-color="primary"
              @click="sidebarColor('primary')"
            ></span>
            <span
              class="badge filter bg-gradient-dark"
              data-color="dark"
              @click="sidebarColor('dark')"
            ></span>
            <span
              class="badge filter bg-gradient-info"
              data-color="info"
              @click="sidebarColor('info')"
            ></span>
            <span
              class="badge filter bg-gradient-success"
              data-color="success"
              @click="sidebarColor('success')"
            ></span>
            <span
              class="badge filter bg-gradient-warning"
              data-color="warning"
              @click="sidebarColor('warning')"
            ></span>
            <span
              class="badge filter bg-gradient-danger"
              data-color="danger"
              @click="sidebarColor('danger')"
            ></span>
          </div>
        </a>
        <!-- Sidenav Type -->
        <div class="mt-3">
          <h6 class="mb-0">Tipo de menú lateral</h6>
          <p class="text-sm">Elige entre 2 tipos diferentes de menú lateral.</p>
        </div>
        <div class="d-flex">
          <button
            id="btn-dark"
            class="px-3 mb-2 btn bg-gradient-dark"
            :class="store.sidebarType === 'bg-gradient-dark' ? 'active' : ''"
            @click="sidebar('bg-gradient-dark')"
          >
            Dark
          </button>
          <button
            id="btn-transparent"
            class="px-3 mb-2 btn bg-gradient-dark ms-2"
            :class="store.sidebarType === 'bg-transparent' ? 'active' : ''"
            @click="sidebar('bg-transparent')"
          >
            Transparent
          </button>
          <button
            id="btn-white"
            class="px-3 mb-2 btn bg-gradient-dark ms-2"
            :class="store.sidebarType === 'bg-white' ? 'active' : ''"
            @click="sidebar('bg-white')"
          >
            White
          </button>
        </div>
        <p class="text-sm d-xl-none d-block mt-2">
          Solo puedes cambiar el tipo de menú lateral en la vista de escritorio.
        </p>

        <!-- Navbar Fixed -->
        <hr class="horizontal dark my-3" />
        <div class="mt-2 d-flex">
          <h6 class="mb-0">Light / Dark</h6>
          <div class="form-check form-switch ps-0 ms-auto my-auto">
            <input
              class="form-check-input mt-1 ms-auto"
              type="checkbox"
              :checked="store.isDarkMode"
              @click="darkMode"
            />
          </div>
        </div>
        <hr class="horizontal dark my-sm-4" />

        <div class="text-center w-100">
          <h6 class="mt-3">¡Gracias por compartirlo! 😊</h6>
          <a
            href=""
            class="mb-0 btn btn-dark me-2"
            target="_blank"
          >
            <i class="fab fa-twitter me-1" aria-hidden="true"></i> Tweet
          </a>
          <a
            href=""
            class="mb-0 btn btn-dark me-2"
            target="_blank"
          >
            <i class="fab fa-facebook-square me-1" aria-hidden="true"></i> Compartir
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
