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
    shouldUseDarkText.value ? "text-dark" : "text-white"
  );

  return {
    sidenavTextClass,
    shouldUseDarkText,
    isWhiteSidenav,
    isDarkSidenav,
  };
}
