from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_restx import Api, Resource, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://alunos_n6kq_user:AINsCNuofHgFW83s5jDvJ9nMiUixZzrK@dpg-crkb541u0jms73bj3p90-a.oregon-postgres.render.com/alunos_n6kq"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

api = Api(app, version='1.0', title='API de Alunos',
          description='Uma API simples para gerenciar informações de alunos')

ns = api.namespace('alunos', description='Operações de alunos')

aluno_model = api.model('Aluno', {
    'ID': fields.Integer(readonly=True, description='ID único do aluno'),
    'Nome': fields.String(required=True, description='Nome do aluno'),
    'Idade': fields.Integer(required=True, description='Idade do aluno'),
    'Nota_do_primeiro_semestre': fields.Float(required=True, description='Nota do primeiro semestre'),
    'Nota_do_segundo_semestre': fields.Float(required=True, description='Nota do segundo semestre'),
    'Nome_do_professor': fields.String(required=True, description='Nome do professor'),
    'Número_da_sala': fields.Integer(required=True, description='Número da sala')
})


class Alunos(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(128), nullable=False)
    Idade = db.Column(db.Integer, nullable=False)
    Nota_do_primeiro_semestre = db.Column(db.Float, nullable=False)
    Nota_do_segundo_semestre = db.Column(db.Float, nullable=False)
    Nome_do_professor = db.Column(db.String(128), nullable=False)
    Número_da_sala = db.Column(db.Integer, nullable=False)

    def __init__(self, Nome, Idade, Nota_do_primeiro_semestre, Nota_do_segundo_semestre, Nome_do_professor, Número_da_sala):
        self.Nome = Nome
        self.Idade = Idade
        self.Nota_do_primeiro_semestre = Nota_do_primeiro_semestre
        self.Nota_do_segundo_semestre = Nota_do_segundo_semestre
        self.Nome_do_professor = Nome_do_professor
        self.Número_da_sala = Número_da_sala


@ns.route('/')
class AlunoList(Resource):
    @ns.doc('list_alunos')
    @ns.marshal_list_with(aluno_model)
    def get(self):
        '''Lista todos os alunos'''
        return Alunos.query.all()

    @ns.doc('create_aluno')
    @ns.expect(aluno_model)
    @ns.marshal_with(aluno_model, code=201)
    @ns.response(201, 'Aluno criado com sucesso')
    @ns.response(400, 'Erro de validação')
    def post(self):
        '''Cria um novo aluno'''
        novo_aluno = Alunos(**api.payload)
        db.session.add(novo_aluno)
        db.session.commit()
        return novo_aluno, 201


@ns.route('/<int:id>')
@ns.response(404, 'Aluno não encontrado')
@ns.param('id', 'O identificador do aluno')
class Aluno(Resource):
    @ns.doc('get_aluno')
    @ns.marshal_with(aluno_model)
    def get(self, id):
        '''Busca um aluno pelo ID'''
        return Alunos.query.get_or_404(id)

    @ns.doc('update_aluno')
    @ns.expect(aluno_model)
    @ns.marshal_with(aluno_model)
    @ns.response(200, 'Aluno atualizado com sucesso')
    @ns.response(400, 'Erro ao atualizar aluno. Verifique os dados.')
    def put(self, id):
        '''Atualiza um aluno'''
        aluno = Alunos.query.get_or_404(id)
        aluno.update(**api.payload)
        db.session.commit()
        return aluno

    @ns.doc('delete_aluno')
    @ns.response(204, 'Aluno deletado')
    def delete(self, id):
        '''Deleta um aluno'''
        aluno = Alunos.query.get_or_404(id)
        db.session.delete(aluno)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
