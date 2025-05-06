<template>
  <div class="d-flex">
  <!-- Sidebar -->
  <nav class="flex-column bg-light p-3 vh-100" style="min-width: 220px;">
    <h5 class="mb-4 text-center">Menu</h5>
    <router-link to="/produtos" class="nav-link p-2 w-100" active-class="active">📦 Produtos</router-link>
    <router-link to="/vendas" class="nav-link p-2 w-100" active-class="active">🧾 Vendas</router-link>
    <router-link to="/clientes" class="nav-link p-2 w-100" active-class="active">👥 Clientes</router-link>
  </nav>

  <!-- Conteúdo Principal -->
  <div class="flex-grow-1 p-4">
    <transition name="fade" mode="out-in">
      <router-view/>
    </transition>
  </div>
</div>
</template>

<style>

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  background-color: aqua;
}

.fade-enter-active, .fade-leave-active{
  transition: opacity 1s ease, transform 0.6s ease;
}



.fade-enter-from, .fade-leave-to{
  opacity: 0;
  transform: scale(0.95);
}

.fade-enter-to, .fade-leave-from{
  opacity: 1;
  transform: scale(1);
}
</style>
