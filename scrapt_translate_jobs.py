# coding: utf-8
from flask import Flask
from translatorscafe import translatorscafe

app = Flask(__name__)

sites = [{"nome": u"Translators Café", "url": "translatorscafe", 'query': 'Portuguese'}]

@app.route('/')
def show_all():
    global sites
    html = u"origems disponíveis: <ul>"
    for item in sites:
        html += '<li><a href="/%s">%s</a></li>' % (item.get('url'), item.get('nome'))
    return html + "</ul>"

@app.route('/<onde>')
def show_home(onde):
    origem = {}
    for item in sites:
        if onde == item.get('url'):
            origem = item

    html = 'Origem selecionada <b>%s</b><br>' % origem.get('nome')
    html += ' procurar por <a href="%s/%s">%s</a>' % (onde, origem.get('query'), origem.get('query'))

    return html

@app.route('/<onde>/<query>')
def show_find(onde, query):
    server = eval(onde)()
    return server.find(query)

if __name__ == '__main__':
    app.run()