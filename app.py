from flask import Flask, request,jsonify
import sqlite3


app = Flask(__name__)


def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS livros(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NO NULL,
                    categoria TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    imagem_url TEXT NOT NULL
                    )""")
        
        print("Banco de dados incializado com sucesso!!")
init_db()

@app.route('/')
def homepage():
    return '<h2>minha página Livia</h2>'

@app.route("/doar", methods=['POST'])
def doar():

    dados = request.get_jason()

    titulo = dados.get("titulo")

    categoria = dados.get("categoria")

    autor = dados.get("autor")

    imagem_url = dados.get("imagem_url")

    if not titulo or not categoria or not autor or not imagem_url:

        return jsonify ({'erro':'todos os campos são obrigatórios'}), 400
    
    with sqlite3.connect('database.db') as conn:
        conn.execute(""" INSERT INTO livros (titulos, categoria, autor, imagem_url))
                        VALUES(?,?,?,?)
                        """)
        conn.commit()

        return jsonify({'mensagem': 'livros cadastrados com sucesso'}), 201

@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect('database.db') as conn:
        livros = conn.execute("SELECT * FROM livros").fetchall()

    livros_formatados = []

    for livro in livros:
        dicionario_livros ={
            "id":livro[0],
            "titulo":livro[1],
            "categoria": livro[2],
            "autor": livro[3],
            "image_url":[4],

        }
        livros_formatados.append(dicionario_livros)
        return jsonify(livros_formatados)

if __name__ == "__main__":
    app.run(debug=True)