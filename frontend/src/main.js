import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './routes'
import 'primeicons/primeicons.css'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";


const options = {
    
};

createApp(App).use(router).use(Toast, options).mount('#app')