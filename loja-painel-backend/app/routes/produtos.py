from flask import Blueprint, request, jsonify
from app import db
from app.models import Produto

bp = Blueprint('produtos', __name__, url_prefix='/api/produtos')


@bp.route('/', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([p.to_dict() for p in produtos])


@bp.route('/', methods=['POST'])
def adicionar_produto():
    data = request.get_json()
    produto = Produto(**data)
    db.session.add(produto)
    db.session.commit()
    return jsonify(produto.to_dict()), 201
