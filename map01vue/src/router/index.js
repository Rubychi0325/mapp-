import { createRouter, createWebHashHistory } from 'vue-router';
import map from '@/components/map.vue';
import maptest from '@/components/maptest.vue';
import MapFunction from '@/components/MapFunction.vue';

const routes = [
  {
    path: '/',
    name: 'map',
    component: map
  },
  {
    path: '/test',
    name: 'maptest',
    component: maptest
  },
  {
    path: '/MapFunction',
    name: 'MapFunction',
    component: MapFunction
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;
