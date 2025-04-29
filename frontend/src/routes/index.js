import { createRouter, createWebHistory } from 'vue-router';
import Register from '../views/Register.vue';
import Login from '../views/Login.vue';
import Home from '../views/Home.vue';
import NotFound from '../views/NotFound.vue';
import ManageUsers from '../views/ManageUsers.vue';
import api from '../api'; 
import ManageUserModels from '../views/ManageUserModels.vue';
import ModelOne from "../views/ModelOne.vue"
import UserModel from '../views/UserModel.vue';
import UserModels from '../views/UserModels.vue';
import Dashboard from '../views/Dashboard.vue';
import UserReports from '../views/UserReports.vue';
import UserAnalyses from '../views/UserAnalyses.vue';
import UserAnalysis from '../views/UserAnalysis.vue';
const routes = [
  { path: '/', component: Home },
  { path: '/register', component: Register, name: "register" },
  { path: '/login', component: Login , name: "login"},
  { path: '/models/:modelId', component: UserModel },
  { path: '/models', component: UserModels },
  { path: '/reports', component: UserReports },
  
  { path: '/analyses/:analysisId', component: UserAnalysis },
  { path: '/analyses', component: UserAnalyses },
  { path: '/dashboard', component: Dashboard },
  { path: '/admin/users', component: ManageUsers, meta: { requiresAdmin: true } },
  
  { path: '/admin/models/:modelId', component: ModelOne, meta: { requiresAdmin: true } },
  { path: '/admin/models', component: ManageUserModels, meta: { requiresAdmin: true } },
  { path: '/:pathMatch(.*)*', component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('accessToken');
  const isAuthenticated = !!token;

  if(!isAuthenticated && to.path === '/')
      return next()

  if (!isAuthenticated && to.path !== '/login' && to.path !== '/register') {
    return next('/login');
  }

  if (isAuthenticated) {
    if (to.path === '/login' || to.path === '/register') {
      return next('/');
    }

    try {
      const res = await api.get('/auth/profile/');
      const role = res.data.role;

      if (to.matched.some(record => record.meta.requiresAdmin)) {
        if (role === 'admin') {
          return next();
        } else {
          return next('/');
        }
      }

      return next();
    } catch (error) {
      console.error('Error fetching profile:', error);
      return next('/login');
    }
  }

  next();
});

export default router;
