import Vue from 'vue'
import { sync } from 'vuex-router-sync'
import VueResource from 'vue-resource'
import App from './components/App'
import router from './router'
import store from './store'
import filters from './filters'

Vue.use(VueResource)
sync(store, router)

const app = new Vue({
    router,
    store,
    filters,
    ...App
})

export { app, router, store }
