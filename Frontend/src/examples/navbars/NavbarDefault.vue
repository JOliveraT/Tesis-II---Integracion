<script setup>
import { RouterLink } from "vue-router";
import { ref, watch, onMounted } from "vue";
import { twitchService } from "@/services/twitchService";
import { useWindowsWidth } from "../../assets/js/useWindowsWidth";

// images
import ArrDark from "@/assets/img/down-arrow-dark.svg";
import downArrow from "@/assets/img/down-arrow.svg";
import DownArrWhite from "@/assets/img/down-arrow-white.svg";

const props = defineProps({
  action: {
    type: Object,
    route: String,
    color: String,
    label: String,
    default: () => ({
      route: "{ name: 'signup' }",
      color: "bg-gradient-success",
      label: "Registrarse"
    })
  },
  actionSignIn: {
    type: Object,
    route: String,
    color: String,
    label: String,
    default: () => ({
      route: "{ name: 'signin' }",
      color: "bg-gradient-info",
      label: "Ingresar"
    })
  },
  transparent: {
    type: Boolean,
    default: false
  },
  light: {
    type: Boolean,
    default: false
  },
  dark: {
    type: Boolean,
    default: false
  },
  sticky: {
    type: Boolean,
    default: false
  },
  darkText: {
    type: Boolean,
    default: false
  }
});

// set arrow  color
function getArrowColor() {
  if (props.transparent && textDark.value) {
    return ArrDark;
  } else if (props.transparent) {
    return DownArrWhite;
  } else {
    return ArrDark;
  }
}

// set text color
const getTextColor = () => {
  let color;
  if (props.transparent && textDark.value) {
    color = "text-dark";
  } else if (props.transparent) {
    color = "text-white";
  } else {
    color = "text-dark";
  }

  return color;
};

// Burbuja de texto (notificación) para canal en vivo
const isLive = ref(false);
const showLiveBubble = ref(false);

// set nav color on mobile && desktop
let textDark = ref(props.darkText);
const { type } = useWindowsWidth();

if (type.value === "mobile") {
  textDark.value = true;
} else if (type.value === "desktop" && textDark.value == false) {
  textDark.value = false;
}

watch(
  () => type.value,
  (newValue) => {
    if (newValue === "mobile") {
      textDark.value = true;
    } else {
      textDark.value = false;
    }
  }
);

// Función para comprobar si el canal está en vivo
const checkIfLive = async (username) => {
  try {
    const response = await twitchService.getMe();
    isLive.value = Boolean(response?.is_live);
    showLiveBubble.value = isLive.value;
  } catch (error) {
    console.error('Error al obtener el estado en vivo:', error);
  }
};

// Ejecutar la comprobación al montar el componente
onMounted(() => {
  checkIfLive("ESL_SC2"); // Cambia esto por el canal que deseas verificar
});
</script>

<template>
  <nav
    class="navbar navbar-expand-lg top-0"
    :class="{
      'z-index-3 w-100 shadow-none navbar-transparent position-absolute my-3':props.transparent,
      'my-3 blur border-radius-lg z-index-3 py-2 shadow py-2 start-0 end-0 mx-4 position-absolute mt-4':props.sticky,
      'navbar-light bg-white py-3': props.light,
      'navbar-dark bg-gradient-dark z-index-3 py-3': props.dark
    }"
  >
    <div
      :class="
        props.transparent || props.light || props.dark
          ? 'container'
          : 'container-fluid px-0'
      "
    >
      <RouterLink
        class="navbar-brand d-none d-md-block"
        :class="[
          (props.transparent && textDark.value) || !props.transparent
            ? 'text-dark font-weight-bolder ms-sm-3'
            : 'text-white font-weight-bolder ms-sm-3'
        ]"
        :to="{ name: 'presentation' }"
        rel="tooltip"
        title="Diseñado por ORVIDA"
        data-placement="bottom"
      >
      <!-- nav desktop -->
        Pixel Gift
      </RouterLink>
      <RouterLink
        class="navbar-brand d-block d-md-none"
        :class="
          props.transparent || props.dark
            ? 'text-white'
            : 'font-weight-bolder ms-sm-3'
        "
        to="/"
        rel="tooltip"
        title="Diseñado por ORVIDA"
        data-placement="bottom"
      >
      <!-- nav mobile -->
        Pixel Gift
      </RouterLink>
      <router-link
        :to="{ name: 'signin' }"
        class="btn btn-sm bg-gradient-success mb-0 ms-auto d-lg-none d-block"
      >
        Ingresar
      </router-link>

      <button
        class="navbar-toggler shadow-none ms-2"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navigation"
        aria-controls="navigation"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon mt-2">
          <span class="navbar-toggler-bar bar1"></span>
          <span class="navbar-toggler-bar bar2"></span>
          <span class="navbar-toggler-bar bar3"></span>
        </span>
      </button>
      <div
        class="collapse navbar-collapse w-100 pt-3 pb-2 py-lg-0"
        id="navigation"
      >
        <ul class="navbar-nav navbar-nav-hover ms-auto">
          <li class="nav-item dropdown dropdown-hover mx-2">
            <a
              href="https://www.twitch.tv/impactocritico"
              class="nav-link d-flex cursor-pointer align-items-center"
              target="_blank"
              rel="noopener noreferrer"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 512 512"
                class="material-icons me-2 opacity-6"
                
                :fill="props.transparent && '#fff'"
              >
                <path
                  d="M391.17,103.47H352.54v109.7h38.63ZM285,103H246.37V212.75H285ZM120.83,0,24.31,91.42V420.58H140.14V512l96.53-91.42h77.25L487.69,256V0ZM449.07,237.75l-77.22,73.12H294.61l-67.6,64v-64H140.14V36.58H449.07Z">
                </path>
              </svg>
              Twitch
              <span v-if="showLiveBubble" class="live-bubble">En Vivo</span>
            </a>
          </li>
        </ul>
        <ul class="navbar-nav d-lg-block d-none">
          <li class="nav-item">
            <!-- Botón de Sign In -->
            <router-link
              :to="{name:'signin'}"
              class="btn btn-sm mb-0"
              :class="action.color"
            >
              {{ actionSignIn.label }}
          </router-link>
            <!-- Botón de Sign Up -->
            <router-link
              :to="{name:'signup'}"
              class="btn btn-sm mb-0"
              :class="action.color"
              >{{ action.label }}
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <!-- End Navbar -->
</template>

<style scoped>
.nav-item .btn {
  margin-left: 10px;
}
.live-bubble {
      position: absolute;
      top: -5px;
      right: -5px;
      background-color: red;
      color: white;
      font-size: 12px;
      padding: 5px 10px;
      border-radius: 50%;
      text-align: center;
    }
</style>
