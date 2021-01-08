from flask import Flask, jsonify
import requests
import re
import os

app = Flask(__name__)

reques = requests.get(
    'https://br.investing.com/equities/brazil',
    headers={'User-Agent': 'Mozilla/5.0'})


def request(r):
    api = []

    res = r.text

    texto = re.findall('<tr id=\"pair_(.*?)</tr>', res)

    for tr in texto:
        title = re.findall(
            '<td class=\"bold left noWrap elp plusIconTd\"><a href=(.*?)>(.*?)</a>',
            tr)[0][1]
        valor_atual = re.findall('last(.*?)\">(.*?)</td>', tr)[0][1]
        alteracao = re.findall('pcp(.*?)\">(.*?)</td>', tr)[0][1]
        api.append({'title': title, 'value': valor_atual, 'porc': alteracao})

    return api


@app.route('/', methods=['GET'])
def get_api():
    return jsonify(request(reques))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
