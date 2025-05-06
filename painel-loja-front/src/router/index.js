import { createRouter, createWebHistory } from 'vue-router'
import Produtos from '../views/Produtos.vue'
import Clientes from '../views/Clientes.vue'
import Vendas from '../views/Vendas.vue'

const routes = [
  { path: '/produtos', component: Produtos},
  { path: '/clientes', component: Clientes},
  { path: '/vendas', component: Vendas},
  { path: '/', redirect: '/produtos'},
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
