<script setup>
import { ref, reactive, computed, watch, onMounted, onBeforeUnmount } from 'vue';
import { useAppStore } from '@/stores';
import setMaterialInput from '@/assets/js/material-input';

// Componentes
import DefaultNavbar from '@/examples/navbars/NavbarDefault.vue';
import Header from '@/examples/Header.vue';
import MaterialInput from '@/components/MaterialInput.vue';
import MaterialCheckbox from '@/components/MaterialCheckbox.vue';
import MaterialButton from '@/components/MaterialButton.vue';
import BgSignUp from '@/assets/img/illustrations/illustration-signup.jpg';

const store = useAppStore();
const body = document.getElementsByTagName("body")[0];

// Estado del formulario
const formData = reactive({
  firstName: '', lastNameP: '', lastNameM: '', nickname: '', country: '',
  phoneCode: '', phone: '', birthDate: '', email: '', password: '', confirmPassword: '', termsAccepted: false
});

const errors = reactive({});
const formSubmitted = ref(false);
const isLoading = ref(false);
const selectedCountryFlag = computed(() => {
  const country = countries.find(c => c.code === formData.country);
  return country ? country.flag : null;
});

// Lista de países (se mantiene igual)
const countries = [
  { code: 'AR', name: 'Argentina', phoneCode: '+54', flag: 'https://flagcdn.com/ar.svg' },
  { code: 'BO', name: 'Bolivia', phoneCode: '+591', flag: 'https://flagcdn.com/bo.svg' },
  { code: 'BR', name: 'Brasil', phoneCode: '+55', flag: 'https://flagcdn.com/br.svg' },
  { code: 'CL', name: 'Chile', phoneCode: '+56', flag: 'https://flagcdn.com/cl.svg' },
  { code: 'CO', name: 'Colombia', phoneCode: '+57', flag: 'https://flagcdn.com/co.svg' },
  { code: 'CR', name: 'Costa Rica', phoneCode: '+506', flag: 'https://flagcdn.com/cr.svg' },
  { code: 'CU', name: 'Cuba', phoneCode: '+53', flag: 'https://flagcdn.com/cu.svg' },
  { code: 'DO', name: 'República Dominicana', phoneCode: '+1-809', flag: 'https://flagcdn.com/do.svg' },
  { code: 'EC', name: 'Ecuador', phoneCode: '+593', flag: 'https://flagcdn.com/ec.svg' },
  { code: 'SV', name: 'El Salvador', phoneCode: '+503', flag: 'https://flagcdn.com/sv.svg' },
  { code: 'GT', name: 'Guatemala', phoneCode: '+502', flag: 'https://flagcdn.com/gt.svg' },
  { code: 'HN', name: 'Honduras', phoneCode: '+504', flag: 'https://flagcdn.com/hn.svg' },
  { code: 'MX', name: 'México', phoneCode: '+52', flag: 'https://flagcdn.com/mx.svg' },
  { code: 'NI', name: 'Nicaragua', phoneCode: '+505', flag: 'https://flagcdn.com/ni.svg' },
  { code: 'PA', name: 'Panamá', phoneCode: '+507', flag: 'https://flagcdn.com/pa.svg' },
  { code: 'PY', name: 'Paraguay', phoneCode: '+595', flag: 'https://flagcdn.com/py.svg' },
  { code: 'PE', name: 'Perú', phoneCode: '+51', flag: 'https://flagcdn.com/pe.svg' },
  { code: 'PR', name: 'Puerto Rico', phoneCode: '+1-787', flag: 'https://flagcdn.com/pr.svg' },
  { code: 'UY', name: 'Uruguay', phoneCode: '+598', flag: 'https://flagcdn.com/uy.svg' },
  { code: 'ES', name: 'España', phoneCode: '+34', flag: 'https://flagcdn.com/es.svg' },
  { code: 'PT', name: 'Portugal', phoneCode: '+351', flag: 'https://flagcdn.com/pt.svg' },
  { code: 'IT', name: 'Italia', phoneCode: '+39', flag: 'https://flagcdn.com/it.svg' },
  { code: 'FR', name: 'Francia', phoneCode: '+33', flag: 'https://flagcdn.com/fr.svg' },
  { code: 'RO', name: 'Rumanía', phoneCode: '+40', flag: 'https://flagcdn.com/ro.svg' },
  { code: 'MD', name: 'Moldavia', phoneCode: '+373', flag: 'https://flagcdn.com/md.svg' }
];


// Actualiza phoneCode según país
watch(() => formData.country, (newCode) => {
  const selected = countries.find(c => c.code === newCode);
  formData.phoneCode = selected ? selected.phoneCode : '';
});

// Validación en tiempo real
const isFormValid = computed(() => {
  return formData.firstName && formData.lastNameP && formData.lastNameM && formData.nickname &&
    formData.country && formData.phone && formData.birthDate &&
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email) &&
    formData.password.length >= 8 && formData.password === formData.confirmPassword &&
    formData.termsAccepted;
});

// Validación completa con errores
const validateForm = () => {
  errors.firstName = formData.firstName ? '' : 'First name is required';
  errors.lastNameP = formData.lastNameP ? '' : 'Last name (paternal) is required';
  errors.lastNameM = formData.lastNameM ? '' : 'Last name (maternal) is required';
  errors.nickname = formData.nickname ? '' : 'Nickname is required';
  errors.country = formData.country ? '' : 'Country is required';
  errors.phone = formData.phone ? '' : 'Phone number is required';
  errors.birthDate = formData.birthDate ? '' : 'Birth date is required';
  errors.email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email) ? '' : 'Valid email required';
  errors.password = formData.password.length >= 8 ? '' : 'Min 8 characters';
  errors.confirmPassword = formData.confirmPassword === formData.password ? '' : 'Passwords do not match';
  errors.termsAccepted = formData.termsAccepted ? '' : 'Must accept terms';
  return Object.values(errors).every(e => !e);
};

// Enviar formulario a Edge Function
const handleSubmit = async (e) => {
  e.preventDefault();
  formSubmitted.value = true;

  if (!validateForm()) return;

  try {
    const response = await fetch("`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/twitch/callback`", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        nickname: formData.nickname,
        email: formData.email,
        password: formData.password,
        firstName: formData.firstName,
        lastNameP: formData.lastNameP,
        lastNameM: formData.lastNameM,
        country: formData.country,
        phone: formData.phoneCode + formData.phone,
        birthDate: formData.birthDate,
      }),
    });

    const result = await response.json();

    if (!response.ok) {
      console.error("Registration error:", result?.error || result?.message || "Unknown error");
      alert(`Error al registrar: ${result?.error || result?.message || "Unknown error"}`);
      return;
    }

    console.log("Registration successful:", result.message);
    alert(result.message || "Registro exitoso");
    // Puedes redirigir a una página de confirmación aquí
  } catch (error) {
    console.error("Unexpected error:", error);
    alert("Error inesperado al registrar");
  }
};

onMounted(() => {
  store.toggleEveryDisplay(); store.toggleHideConfig();
  body.classList.remove("bg-gray-100");
  setMaterialInput();
});
onBeforeUnmount(() => {
  store.toggleEveryDisplay(); store.toggleHideConfig();
  body.classList.add("bg-gray-100");
});
</script>

<template>
  <div class="bg-white">
    <div class="container position-sticky z-index-sticky top-0">
      <div class="row">
        <div class="col-12">
          <DefaultNavbar :sticky="true" />
        </div>
      </div>
    </div>

    <main class="mt-0 main-content">
      <Header>
        <div class="page-header min-vh-100" :style="{ backgroundImage: 'url(' + BgSignUp + ')' }" loading="lazy">
          <span class="mask bg-gradient-dark opacity-6"></span>
          <div class="container my-auto">
            <div class="row">
              <div class="col-lg-6 col-md-8 col-12 mx-auto">
                <div class="card z-index-0 fadeIn3 fadeInBottom">
                  <!-- Cuadro verde superior -->
                  <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
                    <div class="bg-gradient-success shadow-success border-radius-lg py-3 pe-1">
                      <h4 class="text-white font-weight-bolder text-center mt-2 mb-0">Registro</h4>
                      <p class="text-white text-center mt-1 mb-0">Ingresa tus datos para registrarte</p>
                    </div>
                  </div>

                  <!-- Contenido del formulario -->
                  <div class="card-body d-flex">
                    <form role="form" class="flex-fill me-3" @submit.prevent="handleSubmit">
                      <div class="mb-3">
                        <MaterialInput id="input-nickname" v-model="formData.nickname" class="input-group-outline my-3" :label="{ text: 'NickName', class: 'form-label' }" type="text" />
                        <div v-if="formSubmitted && errors.nickname" class="text-danger">{{ errors.nickname }}</div>
                      </div>

                      <div class="row mb-3">
                        <div class="col">
                          <MaterialInput id="input-lastnamep" v-model="formData.lastNameP" class="input-group-outline my-3" :label="{ text: 'Apellido Paterno', class: 'form-label' }" type="text" />
                          <div v-if="formSubmitted && errors.lastNameP" class="text-danger">{{ errors.lastNameP }}</div>
                        </div>
                        <div class="col">
                          <MaterialInput id="input-lastnamem" v-model="formData.lastNameM" class="input-group-outline my-3" :label="{ text: 'Apellido Materno', class: 'form-label' }" type="text" />
                          <div v-if="formSubmitted && errors.lastNameM" class="text-danger">{{ errors.lastNameM }}</div>
                        </div>
                      </div>

                      <div class="row mb-3">
                        <div class="col">
                          <MaterialInput id="input-firstname" v-model="formData.firstName" class="input-group-outline my-3" :label="{ text: 'Nombre', class: 'form-label' }" type="text" />
                          <div v-if="formSubmitted && errors.firstName" class="text-danger">{{ errors.firstName }}</div>
                        </div>
                        <div class="col">
                          <MaterialInput id="input-email" v-model="formData.email" class="input-group-outline my-3" :label="{ text: 'Correo Electrónico', class: 'form-label' }" type="text" />
                          <div v-if="formSubmitted && errors.email" class="text-danger">{{ errors.email }}</div>
                        </div>
                      </div>

                      <div class="row mb-3">
                        <div class="col">
                          <label for="select-country" class="form-label">País</label>
                          <div class="d-flex align-items-center">
                            <img v-if="selectedCountryFlag" :src="selectedCountryFlag" alt="Flag" width="24" height="16" class="me-2" />
                            <select id="select-country" v-model="formData.country" class="form-control input-group-outline my-3">
                              <option value="">Selecciona tu país</option>
                              <option v-for="c in countries" :key="c.code" :value="c.code">{{ c.name }}</option>
                            </select>
                          </div>
                          <div v-if="formSubmitted && errors.country" class="text-danger">{{ errors.country }}</div>
                        </div>
                        <div class="col">
                          <label for="input-phone" class="form-label">Número Telefónico</label>
                          <div class="d-flex align-items-center">
                            <MaterialInput id="input-phonecode" v-model="formData.phoneCode" class="input-group-outline my-3 me-1" type="text" readonly style="width:80px;" />
                            <MaterialInput id="input-phone" v-model="formData.phone" class="input-group-outline my-3 flex-fill" :label="{ text: ' ', class: 'form-label' }" type="text" />
                          </div>
                          <div v-if="formSubmitted && errors.phone" class="text-danger">{{ errors.phone }}</div>
                        </div>
                      </div>

                      <div class="mb-3">
                        <label for="input-birthdate" class="form-label">Fecha de Nacimiento</label>
                        <MaterialInput id="input-birthdate" v-model="formData.birthDate" class="input-group-outline my-3" type="date" />
                        <div v-if="formSubmitted && errors.birthDate" class="text-danger">{{ errors.birthDate }}</div>
                      </div>

                      <div class="mb-3">
                        <MaterialInput id="input-password" v-model="formData.password" class="input-group-outline my-3" :label="{ text: 'Contraseña', class: 'form-label' }" type="password" :showToggle="true" />
                        <div v-if="formSubmitted && errors.password" class="text-danger">{{ errors.password }}</div>
                      </div>

                      <div class="mb-3">
                        <MaterialInput id="input-confirm-password" v-model="formData.confirmPassword" class="input-group-outline my-3" :label="{ text: 'Repetir Contraseña', class: 'form-label' }" type="password" />
                        <div v-if="formSubmitted && errors.confirmPassword" class="text-danger">{{ errors.confirmPassword }}</div>
                      </div>

                      <MaterialCheckbox id="checkbox-terms" class="font-weight-light" v-model="formData.termsAccepted">
                        Estoy de acuerdo con los <a href="../../../pages/privacy.html" class="text-dark font-weight-bolder">Terminos y Condiciones.</a>
                      </MaterialCheckbox>
                      <div v-if="formSubmitted && errors.termsAccepted" class="text-danger">{{ errors.termsAccepted }}</div>

                      <div class="text-center">
                        <MaterialButton class="mt-4 mb-2" variant="gradient" color="success" fullWidth size="lg" :disabled="!isFormValid" @click="handleSubmit">
                          REGISTRAR
                        </MaterialButton>
                      </div>
                    </form>
                  </div>
                  <div class="px-1 pt-0 text-center card-footer px-lg-2">
                    <p class="mx-auto mb-4 text-sm">
                      ¿Ya tienes una cuenta?
                      <router-link :to="{ name: 'signin' }" class="text-success text-gradient font-weight-bold">
                        Ingresar
                      </router-link>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Header>
    </main>
  </div>
</template>
