import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../views/Dashboard.vue';
import Raffles from '../views/Raffles.vue';
import Participants from '../views/Participants.vue';

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Dashboard },
    { path: '/raffles', component: Raffles },
    { path: '/participants', component: Participants }
  ]
});
