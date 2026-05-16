<script>
import SidenavCollapse from "./SidenavCollapse.vue";
import { useAppStore } from "@/stores";
import { useAuthStore } from "@/stores/authStore";
import { computed } from "vue";
import { useSidenavContrast } from "./useSidenavContrast";
import { useRouter } from "vue-router";

export default {
  name: "SidenavList",
  props: {
    cardBg: String,
  },
  setup() {
    const appStore = useAppStore();
    const authStore = useAuthStore();
    const router = useRouter();

    const color = computed(() => appStore.color);
    const { sidenavTextClass } = useSidenavContrast();

    const handleLogout = async () => {
      authStore.logout();
      await router.push("/signin");
    };

    return {
      color,
      sidenavTextClass,
      handleLogout,
    };
  },
  components: {
    SidenavCollapse,
  },
};
</script>

<template>
  <div
    class="w-auto h-auto collapse navbar-collapse max-height-vh-100 h-100"
    id="sidenav-collapse-main"
  >
    <ul class="navbar-nav">
      <li class="nav-item">
        <sidenav-collapse
          url="/dashboard-layout"
          :aria-controls="''"
          :collapse="false"
          collapseRef="dashboard"
          navText="Dashboard"
        >
          <template #icon="{ iconClass }">
            <i class="material-icons-round fs-5" :class="iconClass">dashboard</i>
          </template>
        </sidenav-collapse>
      </li>
      <li class="mt-3 nav-item">
        <h6
          class="text-xs ps-4 text-uppercase font-weight-bolder ms-2"
          :class="sidenavTextClass"
        >
          PARAMETROS DE SORTEO
        </h6>
      </li>
      <li class="nav-item">
        <sidenav-collapse
          url="/dashboard-layout/draw"
          :aria-controls="''"
          v-bind:collapse="false"
          collapseRef="draw"
          navText="Sorteo"
        >
          <template #icon="{ iconClass }">
            <i class="material-icons-round fs-5" :class="iconClass">table_view</i>
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse
          url="/dashboard-layout/profile"
          :aria-controls="''"
          v-bind:collapse="false"
          collapseRef="billing"
          navText="Facturación"
        >
          <template #icon="{ iconClass }">
            <i class="material-icons-round fs-5" :class="iconClass">receipt_long</i>
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse
          url="#"
          :aria-controls="''"
          v-bind:collapse="false"
          collapseRef="notifications"
          navText="Notificaciones"
        >
          <template #icon="{ iconClass }">
            <i class="material-icons-round fs-5" :class="iconClass">notifications</i>
          </template>
        </sidenav-collapse>
      </li>
      <li class="mt-3 nav-item">
        <h6
          class="text-xs ps-4 text-uppercase font-weight-bolder ms-2"
          :class="sidenavTextClass"
        >
          GESTIÓN DE CUENTA
        </h6>
      </li>
      <li class="nav-item">
        <sidenav-collapse
          url="/dashboard-layout/profile"
          :aria-controls="''"
          v-bind:collapse="false"
          collapseRef="profile"
          navText="Perfil"
        >
          <template #icon="{ iconClass }">
            <i class="material-icons-round fs-5" :class="iconClass">person</i>
          </template>
        </sidenav-collapse>
      </li>
    </ul>
    <div class="sidenav-footer position-absolute w-100 bottom-0">
      <div class="mx-3">
        <a
          href="#"
          class="nav-link w-100 text-start mb-2 d-flex align-items-center"
          @click.prevent="handleLogout"
        >
          <div class="text-center d-flex align-items-center justify-content-center me-2">
            <i class="material-icons-round fs-5" :class="sidenavTextClass">logout</i>
          </div>
          <span class="nav-link-text ms-1" :class="sidenavTextClass">Cerrar sesión</span>
        </a>
        <a
          class="btn mt-2 w-100"
          :class="`bg-gradient-${color}`"
          href=""
          target="_blank"
          >Hazte Pro</a
        >
      </div>
    </div>
  </div>
</template>
