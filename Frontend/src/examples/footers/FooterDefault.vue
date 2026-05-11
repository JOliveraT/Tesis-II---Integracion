<script setup>
import logoOrvida from "@/assets/img/orvida-transparent.png";
defineProps({
  brand: {
    type: Object,
    name: String,
    logo: String,
    route: "",
    default: () => ({
      name: "ORVIDA",
      logo: logoOrvida,
      route: "/"
    })
  },
  socials: {
    type: Array,
    icon: String,
    link: String,
    default: () => [
      {
        icon: '<i class="fab fa-facebook text-lg opacity-8"></i>',
        link: ""
      },
      {
        icon: '<i class="fab fa-twitter text-lg opacity-8"></i>',
        link: ""
      },
      {
        icon: '<i class="fab fa-dribbble text-lg opacity-8"></i>',
        link: ""
      },
      {
        icon: '<i class="fab fa-youtube text-lg opacity-8"></i>',
        link: ""
      }
    ]
  },
  menus: {
    type: Array,
    name: String,
    items: {
      type: Array,
      name: String,
      href: String
    },
    default: () => [
      {
        name: "Compañía",
        items: [
          {
            name: "Sobre nosotros",
            href: ""
          },
          {
            name: "Recursos gratuitos",
            href: ""
          },
          {
            name: "Herramientas premium",
            href: ""
          }
        ]
      },
      {
        name: "Recursos",
        items: [
          { name: "Ilustraciones",
            href: "" },
          {
            name: "Componentes",
            href: ""
          },
          {
            name: "Programa de afiliados",
            href: ""
          }
        ]
      },
      {
        name: "Ayuda y soporte",
        items: [
          {
            name: "Contáctanos",
            href: ""
          },
          {
            name: "Desarrollo personalizado",
            href: ""
          },
          {
            name: "Patrocinios",
            href: ""
          }
        ]
      },
      {
        name: "Legal",
        items: [
          {
            name: "Términos y condiciones",
            href: ""
          },
          {
            name: "Política de privacidad",
            href: ""
          }
        ]
      }
    ]
  }
});
</script>
<template>
  <footer class="footer pt-5 mt-5">
    <div class="container">
      <div class="row">
        <div class="col-md-3 mb-4 ms-auto">
          <div>
            <a :href="brand.route">
              <img :src="brand.logo" class="mb-3 footer-logo" alt="main_logo" />
            </a>
            <h6 class="font-weight-bolder mb-4">{{ brand.name }}</h6>
          </div>
          <div>
            <ul class="d-flex flex-row ms-n3 nav">
              <li
                class="nav-item"
                v-for="{ icon, link } of socials"
                :key="link"
              >
                <a
                  class="nav-link pe-1"
                  :href="link"
                  target="_blank"
                  v-html="icon"
                >
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div
          class="col-md-2 col-sm-6 col-6 mb-4"
          v-for="{ name, items } of menus"
          :key="name"
        >
          <h6 class="text-sm">{{ name }}</h6>
          <ul class="flex-column ms-n3 nav">
            <li class="nav-item" v-for="item of items" :key="item.name">
              <a class="nav-link" :href="item.href" target="_blank">
                {{ item.name }}
              </a>
            </li>
          </ul>
        </div>

        <div class="col-12">
          <div class="text-center">
            <p class="text-dark my-4 text-sm font-weight-normal">
              Todos los derechos reservados ©
              {{ new Date().getFullYear() }}
              una herramienta de ORVIDA.
            </p>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>
