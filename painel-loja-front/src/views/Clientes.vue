<!-- eslint-disable vue/multi-word-component-names -->
<template>

<div class="container my-4">

<h1 class="mb-4">Clientes</h1>

<!-- Formulário de Cadastro -->
<form @submit.prevent="salvarCliente" class="row g-3 mb-4">
  <div class="col-md-3">
    <input v-model="novoCliente.nome" class="form-control" placeholder="Nome" required>
  </div>
  <div class="col-md-3">
    <input v-model="novoCliente.cpf" v-mask="'###.###.###-##'" class="form-control" placeholder="CPF" required>
  </div>
  <div class="col-md-3">
    <input v-model="novoCliente.telefone" v-mask="'(##) #####-####'" class="form-control" placeholder="Telefone" required>
  </div>
  <div class="col-md-3">
    <input v-model="novoCliente.endereco" class="form-control" placeholder="Endereço" required>
  </div>
  <div class="col-12">
    <button type="submit" class="btn btn-success">Cadastrar</button>
  </div>
</form>

<!-- Campo de Busca -->
<div class="mb-4">
  <input v-model="filtroCliente" class="form-control" placeholder="Buscar cliente por nome ou CPF">
</div>

<!-- Lista de Clientes -->
<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div v-for="cliente in clientesPaginados" :key="cliente.id" class="col">
        <div class="card h-100 shadow-sm">
      <div class="card-body">
        <h5 class="card-title">{{ cliente.nome }}</h5>
        <p class="card-text mb-1"><strong>CPF:</strong> {{ cliente.cpf }}</p>
        <p class="card-text mb-1"><strong>Telefone:</strong> {{ cliente.telefone }}</p>
        <p class="card-text"><strong>Endereço:</strong> {{ cliente.endereco }}</p>
      </div>
      <div class="card-footer d-flex justify-content-between">
        <button @click="prepararEdicao(cliente)" class="btn btn-sm btn-warning">Editar</button>
        <button @click="excluirCliente(cliente.id)" class="btn btn-sm btn-danger">Excluir</button>
      </div>
    </div>
  </div>
</div>

<!-- Paginação -->
<div class="d-flex justify-content-between align-items-center mb-4">
  <button @click="paginaAtual--" :disabled="paginaAtual === 1" class="btn btn-outline-primary">Anterior</button>
  <span>Página {{ paginaAtual }} de {{ totalPaginas }}</span>
  <button @click="paginaAtual++" :disabled="paginaAtual >= totalPaginas" class="btn btn-outline-primary">Próxima</button>
</div>

<!-- Exportar -->
<div>
  <button @click="exportarParaCSV" class="btn btn-secondary">Exportar Clientes</button>
</div>

</div>



</template>

<script>

import api from '../services/api'
import { VueMaskDirective } from 'v-mask'

export default {
    directives: {
        VueMaskDirective
    },
    data() {
        return {
            clientes: [],
            novoCliente: {
                nome: '',
                cpf: '',
                telefone: '',
                endereco: ''
            },
            filtroCliente: '',
            editando: false,
            clienteSelecionadoId: null,
            paginaAtual: 1,
            itensPorPagina: 6
        }
    },
    computed: {
        clientesFiltrados() {
            const termo = (this.filtroCliente || '').toLowerCase()
            return this.clientes.filter(cliente =>
                (cliente.nome || '').toLowerCase().includes(termo) ||
                (cliente.cpf || '').includes(termo)
            )
        },
        clientesPaginados() {
            const inicio = (this.paginaAtual - 1 ) * this.itensPorPagina
            return this.clientesFiltrados.slice(inicio, inicio + this.itensPorPagina) 
        },
        totalPaginas() {
            return Math.ceil(this.clientesFiltrados.length / this.itensPorPagina)
        }
    },
    methods: {
        async salvarCliente() {
            if (!this.validarCliente(this.novoCliente)) return;

            try {
                // Se estiver editando, faz o PUT (atualizar), caso contrário, faz o POST (cadastrar)
                if (this.editando) {
                    await api.put(`/clientes/${this.clienteSelecionadoId}`, this.novoCliente)
                } else {
                    await api.post('/clientes/', this.novoCliente)
                }

                this.resetarFormulario(); // Reseta o formulário após a operação
                this.carregarClientes();   // Atualiza a lista de clientes
            } catch (err) {
                alert('Erro ao salvar cliente.')
                console.error(err)
            }
        },
        async carregarClientes(){
            const response = await api.get('/clientes/')
            this.clientes = response.data
        },
        async adicionarCliente() {
            try {
                await api.post('/clientes/', this.novoCliente)
                this.novoCliente = { nome: '', cpf: '', telefone: '', endereco: ''}
                this.carregarClientes()
            } catch (err) {
                alert('Erro ao cadastrar cliente.')
                console.error(err)
            }
        },
        validarCliente(cliente){
            const cpfLimpo = cliente.cpf.replace(/\D/g, '')

                if (!cliente.nome.trim()) {
                    alert('Nome é obrigatório.')
                    return false
                }

                if (cpfLimpo.length !== 11 || !/^\d{11}$/.test(cpfLimpo)) {
                    alert('CPF inválido. Deve conter 11 dígitos numéricos.')
                    return false
                }

                if (!cliente.telefone.match(/^\(?\d{2}\)?[\s-]?\d{4,5}-?\d{4}$/)) {
                    alert('Telefone inválido. Ex: (11) 99999-9999')
                    return false
                }

                if (!cliente.endereco.trim()) {
                    alert('Endereço é obrigatório.')
                    return false
                }

                return true
        },
        prepararEdicao(cliente) {
            this.editando = true
            this.clienteSelecionadoId = cliente.id
            this.novoCliente = {...cliente}
        },
        async excluirCliente(id){
            if(confirm('Tem certeza que deseja excluir este cliente?')){
                try{
                await api.delete(`/clientes/${id}`)
                this.carregarClientes()
                }catch(error){
                    alert(error.response?.data?.erro || 'Erro ao excluir cliente.')
                }
            }
        },
        resetarFormulario() {
            this.novoCliente = {
                nome: '',
                cpf: '',
                telefone: '',
                endereco: ''
            }
            this.editando = false
            this.clienteSelecionadoId = null
        },
        exportarParaCSV(){
          if(!this.clientes.length) {
            alert('Não há clientes para exportar.')
            return
          }

          const headers = ['Nome', 'CPF', 'Telefone', 'Endereço']
          const linhas = this.clientes.map(cliente => [
            cliente.nome,
            cliente.cpf,
            cliente.telefone,
            cliente.endereco
          ])

          const csvContent = [headers, ...linhas]
          .map(linha => linha.map(campo => `"${campo}""`).join(',')).join('\n')

          const blob = new Blob([csvContent], {type: 'text/csv;charset=utf-8;'})
          const link = document.createElement('a')
          link.href = URL.createObjectURL(blob)
          link.download = 'clientes.csv'
          link.click()
        }
    },
    mounted(){
        this.carregarClientes()
    }
}

</script>