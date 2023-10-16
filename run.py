import os

import flask
from flask import Flask, request, jsonify

from processing.Filter import Filter
from util import FileReader

app = Flask(__name__)


@app.route('/process', methods=['GET'])
def process():
    path = "Source/"
    # 预估的处理流程是：用户上传一个问卷后将其缓存到Source目录下，前端调用API时提供文件名称（包括扩展名xlsx），后端正确处理完后，前端再把缓存文件删掉
    f = request.args.get('filename')
    print(f)

    if not os.path.exists(path + f):
        return jsonify({'success': False, 'error': 'File does not exist'})

    try:
        data = FileReader.read_source(path + f)
        filter = Filter(data, f[:-5], test=True)
        filter.get_questionnaire_info()
        filter.process()
        report = filter.save_record()

        return jsonify({'success': True, 'content': report})
    except Exception as e:
        return jsonify(
            {'success': False, 'error': 'Process failed. Please check basic information and condition settings.'})


if __name__ == '__main__':
    app.run(debug=True)
