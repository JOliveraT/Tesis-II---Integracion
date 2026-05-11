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
    type: [String,Object],
    default: "#"
    }
  },
  data() {
    return {
      isExpanded: false
    };
  },
  methods: {
    getRoute() {
      return this.$route.name ? this.$route.name.toLowerCase() : "";
    }
  },
  setup(props) {
    const appStore = useAppStore();
    const route = useRoute(); // Usamos useRoute para obtener la ruta actual

    const activeClass = computed(() => {
      const currentRoute = route.name ? route.name.toLowerCase() : "";
      if (currentRoute.includes(props.collapseRef.toLowerCase())) {
        return `active bg-gradient-${appStore.color}`; // Añadimos el gradiente al botón activo
      }
      return "";
    });
    return {
      color: appStore.color,
      activeClass
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
    <span class="nav-link-text ms-1">{{navText}}</span>
  </router-link>
  <div :class="isExpanded ? 'collapse show' : 'collapse'">
    <slot name="list"></slot>
  </div>
</div>
</template>

