// import "primevue/resources/themes/lara-light-indigo/theme.css";
// import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";
import "primeflex/primeflex.css";

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import PrimeVue from 'primevue/config';

import App from './App';
import Aura from "@primevue/themes/aura"
import components from '@/components/UI'; 
import router from "@/router/router"; 
// import '@/api'

const app = createApp(App);

components.forEach(component => {
    app.component(component.name, component); 
});

app
    .use(router)
    .use(PrimeVue, {
        theme: {
            preset: Aura
        }
    })
    .use(createPinia())
    .mount('#app');
