from flask import Flask, jsonify, request
import pandas as ps
import numpy as np

data = ps.read_table('tes_data.tsv')
data['rating'] = np.random.rand(data.shape[0])
app = Flask(__name__)

@app.route("/")
def index():
    return '/movie_id – search by tag\n /movie – search by title\n /year – search by year\n'

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

@app.route('/suggest/<int:topk>', methods=['POST'])
def recommend(topk):
    djson = request.get_json()
    if not 'likes' in djson:
        return 'missing "likes"', 400
    for key in djson['likes']:
        data.at[data['tconst'] == key, 'mark'] = djson['likes'][key]
    res =  data[data['mark'].isna()]['tconst'].sample(n=topk).to_json(orient='values')
    return res 
if __name__ == '__main__':
    app.run(host='0.0.0.0')
