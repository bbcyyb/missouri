# -*- coding: utf-8 -*-

@app.route('/')
def hello_world():
    return render_template('index.html', name="kevin yu")