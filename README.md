# SimpleMock服务部署与使用

## 项目介绍
simple-mock是一个基于Flask框架开发的mock服务，可手动配置需要mock的接口地址和响应，用于应对与第三方对接时不方便调试的情况。主要逻辑写在vies.py的err_404方法中。

## 配置与部署

1. 检查服务器中MySQL正确安装并创建mocker数据库
2. 检查服务器中Python版本为3.8并安装pipenv
```shell
pip install pipenv
```
3. 进入该项目根目录，安装所需依赖包
```shell
pipenv install
```
4. 修改config.py中USERNAME和PASSWORD为服务器中MySQL用户名密码
5. 启动服务（需要开发对应端口，示例为85和5000）
```shell
pipenv run -w 2 -b 0.0.0.0:85 manage:app
```
6. 检查gunicorn服务是否正常运行
```shell
ps -aux | grep gunicorn
```

## 接口文档

### 一、获取token
访问 /mock/user/login 获取用户token  
方法：POST  
报文：
```javascript
{
    "username": "zhaixuwen",
    "password": "123456"
}
```
响应：
```javascript
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ...",
    "code": 200,
    "message": "login success!"
}
```
复制响应中的access_token字段，并在后面的请求头上都加上 {"authorization": "Bearer ${access_token}"}

### 二、创建接口
#### 2.1、创建接口
访问 /mock/apis 创建接口  
方法：POST  
报文：（注意：path 接口地址必须以 /mock/ 开头，否则在后续调用时会被拦截）
```javascript
[
    {
        "title": "票据mock接口",
        "path": "/mock/piaoju/mock",
        "method": "POST"
    }
]
```
响应：
```javascript
{
    "code": 200,
    "message": "成功新建1个接口"
}
```
#### 2.2、查询当前账户的所有接口
访问 /mock/apis 创建接口  
方法：GET  
响应：
```javascript

{
    "code": 200,
    "data": [
        {
            "id": 1,
            "method": "POST",
            "path": "/piaoju/mock",
            "title": "票据mock接口"
        }
    ],
    "message": "success"
}
```
#### 2.3、更新接口
访问 /mock/apis/接口id 更新接口  
方法：PUT  
报文：
```javascript
{
    "title": "票据mock接口222",
    "path": "/mock/piaoju/mock/222",
    "method": "POST"
}
```
响应：
```javascript
{
    "code": 200,
    "message": "成功更新1条数据!"
}
```
#### 2.4、删除接口
访问 /mock/apis/接口id 删除接口  
方法：DELETE

### 三、添加响应返回
#### 3.1、添加接口响应
访问 /mock/apis/result 添加接口响应  
方法：POST  
字段解释：
1. api_id → 需要添加响应的接口id
2. response → 响应的内容，可以是json也可以是字符串
3. response_type → 响应的类型，是json传json，是字符串就传str
报文：
```javascript
{
    "api_id": 1,
    "payload": {
        "bizId": "634899ef-d591-4829-ac18...",
        "timestamp": 1597910515274,
        "data": {
            "identification_ids": [
                "123",
                "456",
                "789"
            ],
            "language": "zh_CN"
        }
    },
    "response": {
        "resCode": 200000,
        "resMsg": "票据查询成功"
    },
    "response_type": "json"
}
```
响应：
```javascript
{
    "code": 201,
    "message": "成功添加1条数据!"
}
```
#### 3.2、查询一个接口下的所有响应
访问 /mock/apis/result 添加接口响应  
方法：GET  
报文：
```javascript
{
    "api_id": 1
}
```
响应：
```javascript

{
    "code": 200,
    "data": [
        {
            "api_id": 1,
            "id": 1,
            "payload": "{'bizId': '634899ef-d591-4829-ac1...', 'timestamp': 1597910515274, 'data': {'identification_ids': ['123', '456', '789'], 'language': 'zh_CN'}}",
            "response": "{'resCode': 200000, 'resMsg': '票据查询成功', 'bizId': 'c40f1bf0-e757-4a72-886...', 'data': {'identification_id': '34334', 'creation_date': '2020-09-18', 'created_by': 'test'}]}}",
            "response_type": "json"
        }
    ],
    "message": "success"
}
```
#### 3.3、查询接口响应详情
访问 /mock/apis/result/响应id 查询响应详情  
方法：GET  
响应：
```javascript
{
    "code": 200,
    "data": {
        "id": 1,
        "payload": "{'bizId': '634899ef-d591-4829-ac1...', 'timestamp': 1597910515274, 'data': {'identification_ids': ['123', '456', '789'], 'language': 'zh_CN'}}",
        "response": "{'resCode': 200000, 'resMsg': '票据查询成功', 'bizId': 'c40f1bf0-e75...', 'data': {'identification_id': '34334', 'creation_date': '2020-09-18', 'created_by': 'test'}]}}",
        "response_type": "json"
    },
    "message": "success"
}
```
#### 3.4、更新接口响应结果
访问 /mock/apis/result/响应id 更新响应结果  
方法：PUT  
响应：
```javascript
{
    "payload": {},
    "response": {},
    "response_type": "json"
}
```
响应：
```javascript
{
    "code": 200,
    "message": "成功更新1条数据!"
}
```
#### 3.5、删除接口响应
访问 /mock/apis/result/响应id 删除响应结果  
方法：DELETE

### 四、调用配置的接口获取响应
#### 4.1、访问配置的接口
> 以步骤2.3中的接口：/mock/piaoju/mock/222 为例

地址：/mock/piaoju/mock/222  
方法：POST  
报文：返回配置的响应内容
