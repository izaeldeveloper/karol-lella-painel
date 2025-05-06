from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify
from app import db
from app.models import Cliente

bp = Blueprint('clientes', __name__, url_prefix='/api/clientes')


@bp.route('/', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])


@bp.route('/', methods=['POST'])
def adicionar_cliente():
    data = request.get_json()
    cliente = Cliente(**data)
    db.session.add(cliente)
    db.session.commit()
    return jsonify(cliente.to_dict()), 201


@bp.route('/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.get_json()

    cliente.nome = data.get('nome', cliente.nome)
    cliente.cpf = data.get('cpf', cliente.cpf)
    cliente.telefone = data.get('telefone', cliente.telefone)
    cliente.endereco = data.get('endereco', cliente.endereco)

    db.session.commit()
    return jsonify(cliente.to_dict())


@bp.route('/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    try:
        cliente = Cliente.query.get_or_404(id)
        db.session.delete(cliente)
        db.session.commit()
        return '', 204
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'erro': "Não é possível excluir o cliente com vendas ativas."
            }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
