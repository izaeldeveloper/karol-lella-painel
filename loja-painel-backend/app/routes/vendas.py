from flask import Blueprint, request, jsonify, send_file
from app import db
from app.models import Venda, ItemVenda, Produto
from app.utils.pdf_generator import gerar_pdf_venda
import io

bp = Blueprint('vendas', __name__, url_prefix='/api/vendas')


@bp.route('/', methods=['GET'])
def listar_vendas():
    vendas = Venda.query.all()
    return jsonify([v.to_dict() for v in vendas])


@bp.route('/', methods=['POST'])
def registrar_venda():
    data = request.get_json()
    itens_data = data.pop('itens')

    venda = Venda(**data)
    total = 0

    for item in itens_data:
        produto = Produto.query.get(item['produto_id'])
        if produto.estoque < item['quantidade']:
            return jsonify(
                {'erro': f"Estoque insuficiente para {produto.nome}"}), 400
        produto.estoque -= item['quantidade']

        item_venda = ItemVenda(
            produto_id=produto.id,
            quantidade=item['quantidade'],
            preco_unitario=produto.preco
        )
        venda.itens.append(item_venda)
        total += produto.preco * item['quantidade']

    venda.total = total
    db.session.add(venda)
    db.session.commit()
    return jsonify({'id': venda.id}), 201


@bp.route('/<int:venda_id>/pdf', methods=['GET'])
def download_pdf_venda(venda_id):
    pdf_bytes = gerar_pdf_venda(venda_id)
    return send_file(
        io.BytesIO(pdf_bytes),
        as_attachment=True,
        download_name=f'venda_{venda_id}.pdf',
        mimetype='application/pdf')
