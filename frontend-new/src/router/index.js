import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../views/Dashboard.vue';
import Raffles from '../views/Raffles.vue';
import Participants from '../views/Participants.vue';
import SignUp from '../components/SignUp.vue';
import Login from '../components/Login.vue';

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Login },
    { path: '/signup', component: SignUp },
    { path: '/signin', component: Login },
    { path: '/dashboard', component: Dashboard },
    { path: '/raffles', component: Raffles },
    { path: '/participants', component: Participants }
  ]
});
