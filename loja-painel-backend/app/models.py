from datetime import datetime
from . import db


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'endereco': self.endereco
        }


class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(
        db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float)

    itens = db.relationship(
        'ItemVenda', backref='venda', cascade='all,delete-orphan')
    cliente = db.relationship('Cliente')

    def to_dict(self):
        return {
            'id': self.id,
            'cliente': self.cliente.to_dict() if self.cliente else None,
            'data': self.data.isoformat(),
            'total': self.total,
            'itens': [item.to_dict() for item in self.itens]
        }


class ItemVenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(
        db.Integer, db.ForeignKey('venda.id'), nullable=False)
    produto_id = db.Column(
        db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

    produto = db.relationship('Produto')

    def to_dict(self):
        return {
            'id': self.id,
            'produto': self.produto.to_dict() if self.produto else None,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario
        }


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, default=0)
    categoria = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': self.preco,
            'estoque': self.estoque,
            'categoria': self.categoria
        }
