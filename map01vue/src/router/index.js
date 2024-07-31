import { createRouter, createWebHashHistory } from 'vue-router';
import map from '@/components/map.vue';

const routes = [
  {
    path: '/',
    name: 'map',
    component: map
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;
