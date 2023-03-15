import json
import random
from flask import request, abort, jsonify, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from passlib.hash import pbkdf2_sha256
from sqlalchemy import or_, and_
from app import app
from exts import db, jwt
from models import User, Apis, Result, Record


# ==========User==========
@app.route('/mock/user/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        abort(400)
    if User.query.filter_by(username=username).first():
        abort(400)
    user = User(username=username)
    user.password = pbkdf2_sha256.hash(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "code": 200,
        "message": "register user success!"
    })


@app.route('/mock/user/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        abort(400)
    user = User.query.filter_by(username=username).first()
    if user:
        if pbkdf2_sha256.verify(password, user.password):
            access_token = create_access_token(identity=username)
            return jsonify({
                "code": 200,
                "message": "login success!",
                "access_token": access_token
            }), 200
    return jsonify({
        "code": 400,
        "message": "error username or password!"
    }), 200


# ==========Apis==========
@app.route('/mock/apis', methods=['GET', 'POST'])
@jwt_required()
def apis_list():
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if request.method == 'GET':
        data = []
        apis = Apis.query.filter_by(user_id=current_user.id).all()
        for a in apis:
            data.append({
                'id': a.id,
                'title': a.title,
                'path': a.path,
                'method': a.method
            })
        return jsonify({
            "code": 200,
            "message": "success",
            "data": data
        })
    if request.method == 'POST':
        if len(request.json):
            for a in request.json:
                title = a.get('title')
                method = a.get('method')
                path = a.get('path')
                api = Apis(user_id=current_user.id, title=title, method=method, path=path)
                db.session.add(api)
            db.session.commit()
            return jsonify({
                "code": 200,
                "message": "成功新建{}个接口".format(len(request.json))
            })
        else:
            return jsonify({
                "code": 200,
                "message": "成功新建0个接口"
            })


@app.route('/mock/apis/<int:api_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def apis_detail(api_id):
    api = Apis.query.filter_by(id=api_id).first()
    if api:
        if request.method == 'GET':
            return jsonify({
                "code": 200,
                "message": "success",
                "data": {
                    "id": api.id,
                    "title": api.title,
                    "method": api.method,
                    "path": api.path
                }
            })
        elif request.method == 'PUT':
            title = request.json.get('title')
            method = request.json.get('method')
            path = request.json.get('path')
            res = Apis.query.filter_by(id=api_id).update({"title": title, "path": path, "method": method})
            print(res)
            db.session.commit()
            return jsonify({
                "code": 200,
                "message": "成功更新1条数据!"
            })
        elif request.method == 'DELETE':
            res = Apis.query.filter_by(id=api_id).delete()
            print(res)
            db.session.commit()
            return jsonify({
                "code": 200,
                "message": "成功删除1条数据!"
            })
    else:
        return jsonify({
            "code": 200,
            "message": "未查询到对应接口,请修改参数后重试!",
            "data": {}
        })


# ==========Result==========
@app.route('/mock/apis/result', methods=['POST', 'GET'])
@jwt_required()
def result_list():
    if request.method == 'GET':
        api_id = request.json.get('api_id')
        if api_id:
            results = Result.query.filter_by(api_id=api_id).all()
            data = []
            for r in results:
                data.append({
                    "id": r.id,
                    "api_id": r.api_id,
                    "payload": r.payload,
                    "response": r.response,
                    "response_type": r.response_type
                })
            return jsonify({
                "code": 200,
                "message": "success",
                "data": data
            }), 200
        else:
            return jsonify({
                "code": 400,
                "message": "缺少必填参数api_id"
            }), 400
    elif request.method == 'POST':
        api_id = request.json.get('api_id')
        if api_id:
            payload = request.json.get('payload')
            response = request.json.get('response')
            response_type = request.json.get('response_type')
            result = Result(api_id=api_id, payload=str(payload), response=str(response), response_type=response_type)
            db.session.add(result)
            db.session.commit()
            return jsonify({
                "code": 201,
                "message": "成功添加1条数据!"
            }), 201
        else:
            return jsonify({
                "code": 400,
                "message": "缺少必填参数api_id"
            }), 400


@app.route('/mock/apis/result/<int:result_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def result_detail(result_id):
    if request.method == 'GET':
        result = Result.query.filter_by(id=result_id).first()
        if result:
            return jsonify({
                "code": 200,
                "message": "success",
                "data": {
                    "id": result.id,
                    "payload": result.payload,
                    "response": result.response,
                    "response_type": result.response_type
                }
            }), 200
        else:
            return jsonify({
                "code": 200,
                "message": "未找到对应结果!"
            }), 200
    elif request.method == 'PUT':
        payload = request.json.get('payload')
        response = request.json.get('response')
        response_type = request.json.get('response_type')
        res = Result.query.filter_by(id=result_id).update({"payload": str(payload), "response": str(response),
                                                           "response_type": response_type})
        print(res)
        db.session.commit()
        return jsonify({
            "code": 200,
            "message": "成功更新1条数据!"
        }), 200
    elif request.method == 'DELETE':
        res = Result.query.filter_by(id=result_id).delete()
        print(res)
        db.session.commit()
        return jsonify({
            "code": 200,
            "message": "成功删除1条数据!"
        }), 200


# ==========404==========
@app.errorhandler(404)
def err_404(err):
    # 从token中获取当前用户
    # current_user = User.query.filter_by(username=get_jwt_identity()).first()
    # 过滤出路径和方法匹配的接口
    # api = Apis.query.filter_by(user_id=current_user.id).filter(
    #     and_(Apis.path == request.path, Apis.method == request.method)).first()

    # 调用自定义接口时不用传token
    app.logger.info('请求的地址是{}'.format(request.path))
    app.logger.info('请求的内容是{}'.format(request.json))
    if not request.path.startswith('/mock'):
        return jsonify({
            "code": 400,
            "message": "访问的接口不存在，如果是自定义接口，地址请以/mock开头。"
        }), 404

    api = Apis.query.filter(
        and_(Apis.path == request.path, Apis.method == request.method)).first()
    if api:
        # 根据接口查询出所有的结果集
        results = Result.query.filter(and_(Result.api_id == api.id)).all()
        if results:
            re_list = []
            for re in results:
                # 结果集中报文与请求的报文一致则保存到列表中随机返回
                if eval(re.payload) == request.json:
                    re_list.append(re)
            if re_list:
                r = random.choice(re_list)
                if r.response_type == 'json':
                    return eval(r.response)
                elif r.response_type == 'str':
                    return r.response
    return jsonify({
        "code": 200,
        "message": "未找到接口对应结果集,请检查配置!"
    })


@app.after_request
def record_req(response):
    url = request.path
    method = request.method
    if request.content_type == 'application/json':
        body = json.dumps(request.json)
    else:
        body = ''
    resp = response.response[0].decode('unicode_escape')
    record = Record(url=url, method=method, payload=body, response=resp)
    db.session.add(record)
    db.session.commit()
    return response
