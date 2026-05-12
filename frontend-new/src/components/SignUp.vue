<template>
  <section class='card'><h3>Registro</h3>
    <input v-model='form.email' placeholder='Email' />
    <input v-model='form.password' type='password' placeholder='Password' />
    <button class='btn' @click='submit'>Crear cuenta</button>
    <p v-if='msg'>{{ msg }}</p>
  </section>
</template>
<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
const auth = useAuthStore();
const router = useRouter();
const msg = ref('');
const form = reactive({ email: '', password: '' });
const submit = async () => {
  try {
    await auth.signUp(form);
    msg.value = 'Registro exitoso';
    router.push('/dashboard');
  } catch (e) { msg.value = e.message; }
};
</script>
