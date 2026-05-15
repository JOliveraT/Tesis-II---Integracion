<script>
import { computed } from "vue";
import { useAppStore } from "@/stores";
import { useSidenavContrast } from "./useSidenavContrast";
import SidenavList from "./SidenavList.vue";
import logo from "@/assets/img/pixelgift_logo_white.png";
import logoDark from "@/assets/img/pixelgift_logo_darkblue.png";

export default {
  name: "index",
  components: {
    SidenavList,
  },
  data() {
    return {
      logo,
      logoDark,
    };
  },
  setup() {
    const appStore = useAppStore();

    const isLightText = computed(() => {
      const isWhite = appStore.sidebarType === "bg-white";
      const isTransparentLight = appStore.sidebarType === "bg-transparent" && !appStore.isDarkMode;
      return !(isWhite || isTransparentLight);
    });

    const brandTextClass = computed(() => (isLightText.value ? "text-white" : "text-dark"));

    return {
      sidebarType: appStore.sidebarType,
      isDarkMode: appStore.isDarkMode,
      brandTextClass,
    };
  },
};
</script>

<template>
  <aside
    id="sidenav-main"
    class="sidenav navbar navbar-vertical navbar-expand-xs border-0 border-radius-xl my-3 ms-3"
    :class="`${sidebarType}`"
  >
    <div class="sidenav-header">
      <i
        class="top-0 p-3 cursor-pointer fas fa-times text-secondary opacity-5 position-absolute end-0 d-none d-xl-none"
        aria-hidden="true"
        id="iconSidenav"
      ></i>
      <a class="m-0 navbar-brand" href="/">
        <img
          :src="
            sidebarType === 'bg-white' ||
            (sidebarType === 'bg-transparent' && !isDarkMode)
              ? logoDark
              : logo
          "
          class="navbar-brand-img h-100"
          alt="main_logo"
        />
        <span class="ms-2 font-weight-bold" :class="brandTextClass"
          >Pixel Gift</span
        >
      </a>
    </div>
    <hr class="horizontal light mt-0 mb-2" />
    <sidenav-list />
  </aside>
</template>
