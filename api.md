# API

标签（空格分隔）： api

---

**host: http://sc.chafanbao.com**

**api_version: v1**

# 概要

 2. API请求格式：host + "api" + api_version + 请求地址。
 3. API返回格式：`json:{"status":1,"body":{}}`status返回操作结果码,body包含返回信息，如果无返回信息，body为空。
 4. status结果码对照表：

|status结果码|状态|
| --------------  | :---: |
|0|未知错误|
|1|成功|
|2|权限不足|
|3|帐号不存在|
|4|数据错误|
|5|密码错误|
|6|已存在|
|7|不存在|
|8|已过期|
|10|验证码为空|
|11|验证码错误|


# 文档

# 门店
## **门店列表**
```
GET /stores/
```
### **Parameters**

### **Return**
成功
```
{
    "body": {
        "store_list": [
            {
                "province": "1",
                "city": "1",
                "name": "test111",
                "lon": 222,
                "order": 0,
                "phone": "123",
                "score": 4.5,
                "create_time": "2018-10-11 10:34:27",
                "modify_time": "2018-10-11 10:35:00",
                "address": "123",
                "lat": 111,
                "id": 1,
                "inventory": 0
            }
        ],
        "page_obj": {},
        "is_paginated": false
    },
    "status": 1,
    "msg": "success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": "请输入手机号"
}
```

## **创建门店**
```
POST /stores/
```
### **Parameters**
* name(_Required_|string)-门店名称
* phone(_Required_|string)-联系方式
* score(_Required_|float)-评分
* province(_Required_|string)-省份
* city(_Required_|string)-城市
* lat(_Required_|string)-纬度
* lon(_Required_|string)-经度
* address(_Required_|string)-详细地址
* inventory(_Required_|int)-库存
* order(_Required_|int)-订单


### **Return**
成功
```
{
    "body": {
        "page_obj": {}
    },
    "status": 1,
    "msg": "success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": ""
}
```

## **更新门店**
```
POST /store/<sid>/
```
### **Parameters**
* name(_Optional_|string)-门店名称
* phone(_Optional_|string)-联系方式
* score(_Optional_|float)-评分
* province(_Optional_|string)-省份
* city(_Optional_|string)-城市
* lat(_Optional_|string)-纬度
* lon(_Optional_|string)-经度
* address(_Optional_|string)-详细地址
* inventory(_Optional_|int)-库存
* order(_Optional_|int)-订单


### **Return**
成功
```
{
    "body": {
        "page_obj": {}
    },
    "status": 1,
    "msg": "success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": ""
}
```