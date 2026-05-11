<script setup>
import { onMounted, onUnmounted } from "vue";

//example components
import NavbarDefault from "../..//examples/navbars/NavbarDefault.vue";
import DefaultFooter from "../../examples/footers/FooterDefault.vue";
import Header from "../../examples/Header.vue";
import FilledInfoCard from "../../examples/Cards/infoCards/FilledInfoCard.vue";

//images
import vueMkHeader from "@/assets/img/vue-mk-header.jpg";
import wavesWhite from "@/assets/img/waves-white.svg";
import donate from "@/assets/img/bg-donate.png";

//hooks
const body = document.getElementsByTagName("body")[0];
onMounted(() => {
  body.classList.add("presentation-page");
  body.classList.add("bg-gray-200");
});
onUnmounted(() => {
  body.classList.remove("presentation-page");
  body.classList.remove("bg-gray-200");
});
</script>

<template>
  <div class="container position-sticky z-index-sticky top-0">
    <div class="row">
      <div class="col-12">
        <NavbarDefault :sticky="true" />
      </div>
    </div>
  </div>
  <Header>
    <div
      class="page-header min-vh-75"
      :style="`background-image: url(${vueMkHeader})`"
      loading="lazy"
    >
      <div class="container">
        <div class="row">
          <div class="col-lg-7 text-center mx-auto position-relative">
            <h1
              class="text-white pt-3 mt-n5 me-2"
              :style="{ display: 'inline-block ' }"
            >
              Bienvenido a Pixel Gift
            </h1>
            <p class="lead text-white px-5 mt-3" :style="{ fontWeight: '500' }">
              ¡Haz comunidad, conecta y gana... así ganas tú y ganamos todos!
            </p>
          </div>
        </div>
      </div>
    </div>
  </Header>

<div class="card card-body blur shadow-blur mx-3 mx-md-4 mt-n6">
    <div class="container">
      <div class="row">
        <div class="col-lg-4">
          <FilledInfoCard
            class="p-4"
            :color="{ text: 'white', background: 'bg-gradient-faded-dark' }"
            :icon="{ component: 'how_to_vote', color: 'success' }"
            title="¿Cómo participar?"
            description="Para ingresar al sorteo, solo debes escribir el comando que el streamer haya definido en el chat en vivo. Tu nombre aparecerá automáticamente en la animación del sorteo."
          />
        </div>
        <div class="col-lg-4">
          <FilledInfoCard
            class="p-4"
            :color="{ text: 'white', background: 'bg-gradient-faded-dark' }"
            :icon="{ component: 'volunteer_activism', color: 'success' }"
            title="Causas benéficas"
            description="Este proyecto vincula sorteos con campañas solidarias. Todas las causas son seleccionadas por el equipo de la plataforma para asegurar impacto real y transparencia."
          />
        </div>
        <div class="col-lg-4">
          <FilledInfoCard
            class="p-4"
            :color="{ text: 'white', background: 'bg-gradient-faded-dark' }"
            :icon="{ component: 'campaign', color: 'success' }"
            title="Donaciones con visibilidad"
            description="Empresas pueden donar a campañas activas y, a cambio, aparecer en las animaciones de los sorteos. Una forma transparente de apoyar y conectar con la audiencia."
          />
        </div>
      </div>
    </div>

    <div
      class="container-fluid mt-sm-5 border-radius-xl"
      :style="{
          backgroundImage: `url(${donate})`
        }"
    >
      <div
        class="page-header py-6 py-md-5 my-sm-3 mb-3 border-radius-xl"
        
        loading="lazy"
      >
        <span class="mask bg-gradient-transparent"></span>
        <div class="container">
          <div class="row">
            <div class="d-flex justify-content-center p-5">
              <div class="col-lg-8 ms-lg-5 text-center">
                <h3 class="text-white">
                  Contribuye a una buena causa
                </h3>
                <p class="text-white text-md">
                  Este proyecto une el poder del streaming con la solidaridad. A través de sorteos en vivo, buscamos apoyar causas reales que hacen la diferencia.
                  <br /><br />
                  Si tú también quieres aportar, puedes hacerlo en cualquier momento mediante PayPal, sin necesidad de registrarte ni participar del sorteo. Cada donación cuenta. Cada aporte transforma.
                </p>

                <a
                  href="https://www.paypal.com/donate/?hosted_button_id=SZDU8Y2LAFYGC"
                  class="btn btn-sm mb-0 bg-gradient-success px-5 py-3 mt-4"
                  >Donar vía PayPal</a
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>

  <DefaultFooter />
</template>
