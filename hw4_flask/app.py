from flask import Flask, jsonify
import pandas as ps

data = ps.read_table('tes_data.tsv')
app = Flask(__name__)

@app.route("/")
def index():
    return '/movie_id – search by tag\n /movie – search by title\n /year – search by year'

@app.route('/movie_id/<idfilm>')
def movie(idfilm):
    if data['tconst'].isin([idfilm]).any():
        res =  data[data['tconst'] == idfilm][['primaryTitle','startYear','genres']].to_json(orient='records')
        return res
    else:
        return '', 404

@app.route('/movie/<title>')
def mov_atr(title):
    if data['primaryTitle'].isin([title]).any():
        res_2 =  data[data['primaryTitle'] == title][['tconst']].to_json(orient='records')
        return res_2
    else:
        return '', 404

@app.route('/year/<int:year_foo>')
def mov_by_year(year_foo):
    if data['startYear'].isin([year_foo]).any():
        res_3 =  data[data['startYear'] == year_foo][['tconst']].to_json(orient='values')
        return res_3
    else:
        return '', 404


if __name__ == '__main__':
    app.run(port=5000)
