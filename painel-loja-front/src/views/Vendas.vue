<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="container my-4">

<h1 class="mb-4">Nova Venda</h1>

<div class="mb-3">
  <label for="cliente" class="form-label">Cliente:</label>
  <select v-model="venda.cliente_id" id="cliente" class="form-select">
    <option disabled value="">Selecione um cliente</option>
    <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
      {{ cliente.nome }}
    </option>
  </select>
</div>

<hr class="my-4">

<div class="mb-4">
  <div class="mb-3">
    <label for="categorias" class="form-label">Categoria:</label>
    <select v-model="categoriasSelecionadas" multiple id="categorias" class="form-select">
      <option value="" disabled>Todas</option>
      <option :value="categoria" :key="categoria" v-for="categoria in categorias">
        {{ categoria }}
      </option>
    </select>
  </div>

  <label class="form-label">Produto:</label>

  <input type="text" v-model="buscaProduto" class="form-control mb-3" placeholder="Buscar produto por nome...">

  <div class="row g-3 align-items-center mb-3">
    <div class="col-auto">
      <label for="ordenar" class="col-form-label">Ordenar por:</label>
    </div>
    <div class="col-auto">
      <select v-model="ordemSelecionada" id="ordenar" class="form-select">
        <option value="nome">Nome</option>
        <option value="preco">Preço</option>
      </select>
    </div>
    <div class="col-auto">
      <label class="form-check-label">
        <input type="checkbox" v-model="ordemReversa" class="form-check-input me-2">
        Reverter Ordem
      </label>
    </div>
  </div>

  <div class="input-group mb-3">
    <select v-model="produtoSelecionadoId" class="form-select">
      <option disabled value="">Selecione um produto</option>
      <option v-for="produto in produtosFiltrados" :key="produto.id" :value="produto.id">
        {{ produto.nome }} (Estoque: {{ produto.estoque }}) - R$ {{ produto.preco }}
      </option>
    </select>
    <input type="number" min="1" v-model.number="quantidade" placeholder="Qtd" class="form-control">
    <button class="btn btn-primary" @click="adicionarItem">Adicionar</button>
  </div>
</div>

<ul class="list-group mb-3">
  <li v-for="(item, index) in venda.itens" :key="index" class="list-group-item d-flex justify-content-between align-items-center">
    <div>
      {{ item.nome }} - {{ item.quantidade }} x R$ {{ item.preco_unitario }} = R$ {{ item.quantidade * item.preco_unitario }}
    </div>
    <button class="btn btn-sm btn-danger" @click="removerItem(index)">Remover</button>
  </li>
</ul>

<p class="fs-5 fw-bold">
  Total da Venda: R$ {{ calcularTotal() }}
</p>

<button class="btn btn-success" :disabled="carregandoVenda || !venda.cliente_id || venda.itens.length === 0" @click="registrarVenda">
  {{ carregandoVenda ? 'Registrando...' : 'Registrar Venda' }}
</button>

<div v-if="vendaRegistradaId" class="alert alert-success mt-3">
  <p class="mb-1">Venda registrada com sucesso! ID: {{ vendaRegistradaId }}</p>
  <a :href="`http://localhost:5000/api/vendas/${vendaRegistradaId}/pdf`" class="btn btn-outline-secondary btn-sm" target="_blank">
    Baixar PDF
  </a>
</div>

<div class="container my-4">

<h2 class="mb-4">Histórico de Vendas</h2>

<ul class="list-unstyled">
  <li v-for="venda in vendas" :key="venda.id" class="mb-4">
    <div class="card shadow">
      <div class="card-header bg-primary text-white">
        Cliente: {{ venda.cliente.nome }}
      </div>
      <div class="card-body">
        <h5 class="card-title mb-3">Itens da Compra</h5>

        <ul class="list-group list-group-flush">
          <li class="list-group-item" v-for="item in venda.itens" :key="item.id">
            <div class="row">
              <div class="col-md-4"><strong>Produto:</strong> {{ item.produto.nome }}</div>
              <div class="col-md-2"><strong>Qtd:</strong> {{ item.produto.estoque }}</div>
              <div class="col-md-3"><strong>Unitário:</strong> R$ {{ item.preco_unitario.toFixed(2) }}</div>
              <div class="col-md-3"><strong>Total:</strong> R$ {{ (item.preco_unitario * item.produto.estoque).toFixed(2) }}</div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </li>
</ul>

</div>

</div>

</template>

<script>

import api from '../services/api'

export default {
    data(){
        return {
            carregandoVenda: false,
            clientes: [],
            buscaProduto: '',
            ordemSelecionada: 'nome',
            ordemReversa: false,
            categoriasSelecionadas: [],
            categorias: [],
            produtos: [],
            produtoSelecionadoId: '',
            quantidade: 1,
            vendas: [],
            venda: {
                cliente_id: '',
                itens: []
            },
            vendaRegistradaId: null        
        }
    },
    computed: {
        produtosFiltrados() {

            let produtosFiltrados = this.produtos

            if(this.buscaProduto) {
                produtosFiltrados = produtosFiltrados.filter(produto =>
                    produto.nome.toLowerCase().includes(this.buscaProduto.toLowerCase())
                )
            }

            if(this.categoriasSelecionadas.length > 0) {
              produtosFiltrados = produtosFiltrados.filter(produto => 
                this.categoriasSelecionadas.includes(produto.categoria)
              )
            }

            if(this.ordemSelecionada === 'nome'){
                return produtosFiltrados.sort((a, b) => a.nome.localeCompare(b.nome))
            }else if(this.ordemSelecionada === 'preco') {
                return produtosFiltrados.sort((a, b) => a.preco - b.preco)
            }

            if(this.ordemReversa) {
                produtosFiltrados = produtosFiltrados.reverse()
            }

            return produtosFiltrados
        }
    },
    methods: {
        async carregarDados() {
            const [resClientes, resProdutos, resVendas] = await Promise.all([
                api.get('/clientes/'),
                api.get('/produtos/'),
                api.get('/vendas/')
            ])
            this.clientes = resClientes.data
            this.produtos = resProdutos.data
            this.vendas = resVendas.data

            this.categorias = [...new Set(this.produtos.map(produto => produto.categoria))]

            this.produtos = this.produtos.sort((a, b) => a.nome.localeCompare(b.nome))
        },
        adicionarItem() {
            const produto = this.produtos.find(p => p.id === this.produtoSelecionadoId)
            if(!produto || this.quantidade < 1) return

            if(this.quantidade > produto.estoque){
                alert(`Estoque insuficiente. Disponível: ${produto.estoque}`)
                return
            }

            this.venda.itens.push({
                produto_id: produto.id,
                nome: produto.nome,
                preco_unitario: produto.preco,
                quantidade: this.quantidade
            })

            this.produtoSelecionadoId = ''
            this.quantidade = 1
        },
        removerItem(index){
            this.venda.itens.splice(index, 1)
        },
        calcularTotal(){
            return this.venda.itens.reduce((total, item) => {
                return total + item.quantidade * item.preco_unitario
            }, 0).toFixed(2)
        },
        async registrarVenda(){

            this.carregandoVenda = true

            try{
                if(!this.venda.cliente_id){
                    alert('Selecione um cliente.')
                    return
                }

                if(this.venda.itens.length === 0){
                    alert('Adicione pelo menos um produto.')
                    return
                }

                const payload = {
                    cliente_id: this.venda.cliente_id,
                    itens: this.venda.itens.map(({produto_id, quantidade}) => ({produto_id, quantidade}))
                }

                try {
                    const res = await api.post('/vendas/', payload)
                    this.vendaRegistradaId = res.data.id
                    this.venda = { cliente_id: '', itens: []}
                    await this.carregarDados()
                }catch(err){
                    alert('Erro ao registrar venda')
                    console.error(err)
                }
            } finally {
                this.carregandoVenda = false
            }

            
        }
    },
    mounted(){
        this.carregarDados().then(() =>{
            this.ordemSelecionada = 'nome'
            this.ordemReversa = false
        })
    }
}

</script>