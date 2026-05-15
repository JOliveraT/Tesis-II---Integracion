import { computed } from "vue";
import { useAppStore } from "@/stores";

export function useSidenavContrast() {
  const appStore = useAppStore();

  const isWhiteSidenav = computed(() => appStore.sidebarType === "bg-white");
  const isDarkSidenav = computed(() => appStore.sidebarType === "bg-gradient-dark");

  const shouldUseDarkText = computed(() => {
    if (isWhiteSidenav.value) return true;
    if (isDarkSidenav.value) return false;
    return !appStore.isDarkMode;
  });

  const sidenavTextClass = computed(() =>
    shouldUseDarkText.value ? "sidenav-text-contrast-dark" : "sidenav-text-contrast-light"
  );

  const sidenavItemClass = computed(() => ({
    [sidenavTextClass.value]: true,
  }));

  return {
    sidenavTextClass,
    sidenavItemClass,
    shouldUseDarkText,
    isWhiteSidenav,
    isDarkSidenav,
  };
}
