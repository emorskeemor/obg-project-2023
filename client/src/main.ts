import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { Quasar } from 'quasar'
import quasarUserOptions from '@/quasar-user-options'
import VueApexCharts from "vue3-apexcharts";


const app = createApp(App)
// Quasar for styling
app.use(Quasar, quasarUserOptions)
// Apex charts for statistics
app.use(VueApexCharts)
// store
app.use(store)
// VUE routing
app.use(router)
app.mount('#app')
