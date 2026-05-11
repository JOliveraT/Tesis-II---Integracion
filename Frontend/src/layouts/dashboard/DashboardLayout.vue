<script setup>
import { computed } from "vue";
import { useAppStore } from "@/stores";
import Sidenav from "@/examples/Sidenav/index.vue";
import Navbar from "@/examples/navbars/Navbar.vue";
import Configurator from "@/examples/Configurator.vue";
import AppFooter from "@/examples/Footer.vue";

const appStore = useAppStore();

// 🛠️ Cambio 4: creamos computed properties para la reactividad
const color = computed(() => appStore.color);
const isAbsolute = computed(() => appStore.isAbsolute);
const isNavFixed = computed(() => appStore.isNavFixed);
const navbarFixed = computed(() => appStore.navbarFixed);
const absolute = computed(() => appStore.absolute);
const showSidenav = computed(() => appStore.showSidenav);
const showNavbar = computed(() => appStore.showNavbar);
const showFooter = computed(() => appStore.showFooter);
const showConfig = computed(() => appStore.showConfig);

// Método para alternar el configurador (lo manejamos en el store)
const toggleConfigurator = () => {
  appStore.toggleConfigurator(); // Alternamos el estado en el store
};
</script>

<template>
  <div class="g-sidenav-show">
    <!-- 🛠️ Cambio 5: mostrar Sidenav solo si showSidenav -->
    <Sidenav
      :custom_class="color"
      class="fixed-start"
      v-if="showSidenav"
    />
    
    <main class="main-content position-relative max-height-vh-100 h-100 overflow-x-hidden">
      
      <!-- 🛠️ Cambio 6: mostrar Navbar solo si showNavbar, y aplicar clases dinámicas -->
      <Navbar
        v-if="showNavbar"
        :class="[isNavFixed ? navbarFixed : '', isAbsolute ? absolute : '']"
        :color="isAbsolute ? 'text-white opacity-8' : ''"
        :minNav="appStore.isPinned"
      />

      <!-- El contenido de la página -->
      <router-view />

      <!-- 🛠️ Cambio 7: mostrar Footer solo si showFooter -->
      <AppFooter v-if="showFooter" />

      <configurator
        :toggle="toggleConfigurator"
        :class="[showConfig ? 'show' : '', appStore.hideConfigButton ? 'd-none' : '']"
      />
    </main>
  </div>
</template>
