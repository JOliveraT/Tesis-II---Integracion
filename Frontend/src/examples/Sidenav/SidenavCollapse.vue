<script>
import { computed } from "vue";
import { useAppStore } from "@/stores";
import { useRoute } from "vue-router";

export default {
  name: "SidenavCollapse",
  props: {
    collapseRef: {
      type: String,
      required: true
    },
    navText: {
      type: String,
      required: true
    },
    collapse: {
      type: Boolean,
      default: true
    },
    url: {
      type: [String, Object],
      default: "#"
    }
  },
  data() {
    return {
      isExpanded: false
    };
  },
  setup(props) {
    const appStore = useAppStore();
    const route = useRoute();

    const isActive = computed(() => {
      const currentRoute = route.name ? route.name.toLowerCase() : "";
      return currentRoute.includes(props.collapseRef.toLowerCase());
    });

    const activeClass = computed(() =>
      isActive.value ? `active bg-gradient-${appStore.color}` : ""
    );

    const navTextClass = computed(() => {
      if (isActive.value) return "text-white";

      const isWhite = appStore.sidebarType === "bg-white";
      const isTransparentLight =
        appStore.sidebarType === "bg-transparent" && !appStore.isDarkMode;

      return isWhite || isTransparentLight ? "text-dark" : "text-white";
    });

    return {
      activeClass,
      navTextClass
    };
  }
};
</script>

<template>
  <div>
    <router-link
      :to="url"
      :data-bs-toggle="collapse ? 'collapse' : ''"
      :aria-controls="collapseRef"
      :aria-expanded="isExpanded"
      class="nav-link"
      :class="activeClass"
      @click="isExpanded = !isExpanded"
    >
      <div class="text-center d-flex align-items-center justify-content-center me-2">
        <slot name="icon"></slot>
      </div>
      <span class="nav-link-text ms-1" :class="navTextClass">{{ navText }}</span>
    </router-link>
    <div :class="isExpanded ? 'collapse show' : 'collapse'">
      <slot name="list"></slot>
    </div>
  </div>
</template>
