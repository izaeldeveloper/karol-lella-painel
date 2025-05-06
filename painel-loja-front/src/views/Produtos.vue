<!-- eslint-disable vue/multi-word-component-names -->
<template>

<div class="container my-4">
  <h1 class="mb-4">Produtos</h1>

  <!-- Formulário de Adição -->
  <form @submit.prevent="adicionarPoduto" class="row g-3 mb-4">
    <div class="col-md-3">
      <label class="form-label">Nome:</label>
      <input v-model="novoProduto.nome" class="form-control" :class="{ 'is-invalid': !novoProduto.nome }" placeholder="Nome">
    </div>
    <div class="col-md-3">
      <label class="form-label">Categoria:</label>
      <input v-model="novoProduto.categoria" class="form-control" :class="{ 'is-invalid': !novoProduto.categoria }" placeholder="Categoria">
    </div>
    <div class="col-md-3">
      <label class="form-label">Preço:</label>
      <input v-model="novoProduto.preco" class="form-control" :class="{ 'is-invalid': !novoProduto.preco }" placeholder="Preço">
    </div>
    <div class="col-md-3">
      <label class="form-label">Quantidade:</label>
      <input v-model="novoProduto.estoque" class="form-control" :class="{ 'is-invalid': !novoProduto.estoque }" placeholder="Estoque">
    </div>
    <div class="col-12">
      <button type="submit" class="btn btn-success">Adicionar</button>
    </div>
  </form>

  <!-- Filtros -->
  <div class="row align-items-end mb-4">
    <div class="col-md-4">
      <label class="form-label">Buscar produto:</label>
      <input v-model="filtroNome" class="form-control" placeholder="Nome do produto">
    </div>
    <div class="col-md-4">
      <label class="form-label">Categoria:</label>
      <select v-model="filtroCategoria" class="form-select">
        <option :key="categoria" :value="categoria" v-for="categoria in categorias">
          {{ categoria }}
        </option>
      </select>
    </div>
    <div class="col-md-4 d-flex gap-2">
      <button @click="aplicarFiltros" class="btn btn-primary w-100">Filtrar</button>
    </div>
  </div>

  <!-- Ordenação -->
  <div class="mb-4">
    <button @click="ordenarProdutos('nome')" class="btn btn-outline-secondary me-2">Ordenar por Nome</button>
    <button @click="ordenarProdutos('preco')" class="btn btn-outline-secondary">Ordenar por Preço</button>
  </div>

  <!-- Lista de Produtos -->
  <ul class="list-group mb-4">
    <li v-for="produto in produtos" :key="produto.id" class="list-group-item d-flex justify-content-between align-items-center">
      <div>
        <strong>{{ produto.nome }}</strong> - R$ {{ produto.preco }} | ({{ produto.estoque }} un.)
      </div>
      <div>
        <button @click="editarProduto(produto.id)" class="btn btn-sm btn-warning me-2">Editar</button>
        <button @click="excluirProduto(produto.id)" class="btn btn-sm btn-danger">Excluir</button>
      </div>
    </li>
  </ul>

  <!-- Paginação -->
  <div class="d-flex justify-content-between">
    <button @click="paginaAtual--" :disabled="paginaAtual <= 1" class="btn btn-outline-primary">Anterior</button>
    <button @click="paginaAtual++" class="btn btn-outline-primary">Próxima</button>
  </div>
</div>

</template>

<script>

import api from '../services/api'

export default {
    data(){
        return {
            produtos: [],
            paginaAtual: 1,
            produtosPorPagina: 10,
            ordem: 'nome',
            filtroNome: '',
            filtroCategoria: '',
            novoProduto: {
                nome: '',
                categoria: '',
                preco: 0,
                estoque: 0
            }
        }
    },
    computed: {
        isFormValid() {
            return this.novoProduto.nome && this.novoProduto.categoria
            && this.novoProduto.preco && this.novoProduto.estoque
        }
    },
    methods: {
        async carregarProdutos() {
            const response = await api.get(`/produtos/?pagina=${this.paginaAtual}&ordem=${this.ordem}`)
            this.produtos = response.data
        },
        ordenarProdutos(criterio) {
            this.ordem = criterio;
            this.carregarProdutos;
        },
        async aplicarFiltros(){
            const response = await api.get('/produtos', {
                params: {
                    nome: this.filtroNome,
                    categoria: this.filtroCategoria,
                }
            });
            this.produtos = response.data;
        },
        mudarPagina(pagina) {
            this.paginaAtual = pagina;
            this.carregarProdutos();
        },
        async adicionarPoduto() {
            await api.post('/produtos/', this.novoProduto)
            this.novoProduto = { nome: '', preco: 0, estoque: 0}
            this.carregarProdutos()
        },
        async editarProduto(id) {
            const produto = this.produtos.find(p => p.id === id);
            this.novoProduto = {...produto};
        },
        async excluirProduto(id) {
            const confirmacao = confirm('Você tem certeza que deseja excluir este produto?');
            if(confirmacao) {
                await api.delete(`/produtos/${id}`)
                this.carregarProdutos();
            }
        }
    },
    mounted() {
        this.carregarProdutos()
    }
}

</script>