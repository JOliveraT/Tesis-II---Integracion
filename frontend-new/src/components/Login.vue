<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
const auth = useAuthStore();
const router = useRouter();
const form = reactive({ email: '', password: '' });
const msg = ref('');
const submit = async () => {
  try { await auth.signIn(form); router.push('/dashboard'); }
  catch (e) { msg.value = e.message; }
};
</script>
<template>
  <section class='card'><h3>Login</h3>
    <input v-model='form.email' placeholder='Email' />
    <input v-model='form.password' type='password' placeholder='Password' />
    <button class='btn' @click='submit'>Iniciar sesión</button>
    <p v-if='msg'>{{ msg }}</p>
  </section>
</template>
