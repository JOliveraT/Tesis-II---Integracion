<script>
import SidenavCollapse from "./SidenavCollapse.vue";
import { useAppStore } from "@/stores";
import { computed } from "vue";

export default {
  name: "SidenavList",
  props: {
    cardBg: String,
  },
  setup() {
    const appStore = useAppStore();

    const color = computed(() => appStore.color);

    return {
      color,
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
          <template v-slot:icon>
            <i class="material-icons-round opacity-10 fs-5">dashboard</i>
          </template>
        </sidenav-collapse>
      </li>
      <li class="mt-3 nav-item">
        <h6
          class="text-xs ps-4 text-uppercase font-weight-bolder text-white ms-2"
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
          <template v-slot:icon>
            <i class="material-icons-round opacity-10 fs-5">table_view</i>
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse
          url="#"
          :aria-controls="''"
          v-bind:collapse="false"
          collapseRef="billing"
          navText="Facturación"
        >
          <template v-slot:icon>
            <i class="material-icons-round opacity-10 fs-5">receipt_long</i>
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
          <template v-slot:icon>
            <i class="material-icons-round opacity-10 fs-5">notifications</i>
          </template>
        </sidenav-collapse>
      </li>
      <li class="mt-3 nav-item">
        <h6
          class="text-xs ps-4 text-uppercase font-weight-bolder text-white ms-2"
        >
          GESTIÓN DE CUENTA
        </h6>
      </li>
      <li class="nav-item">
        <sidenav-collapse
          url="#"
          :aria-controls="''"
          v-bind:collapse="false"
          collapseRef="profile"
          navText="Perfil"
        >
          <template v-slot:icon>
            <i class="material-icons-round opacity-10 fs-5">person</i>
          </template>
        </sidenav-collapse>
      </li>
    </ul>
    <div class="sidenav-footer position-absolute w-100 bottom-0">
      <div class="mx-3">
        <a
          class="btn mt-4 w-100"
          :class="`bg-gradient-${color}`"
          href=""
          target="_blank"
          >Hazte Pro</a
        >
      </div>
    </div>
  </div>
</template>