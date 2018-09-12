## 简陋API 文档

###  服务器地址: http://www.ikebo.cn:3000/service

#### 如需要所有物品信息:
调用 http://www.ikebo.cn:3000/service/api/v1/item
数据在 res.data.data 中获取

用户相关API 前缀: /api/v1/user
1. /<int: code>  GET  
   code 为调用wx.login 后返回的code   
   返回用户信息(如用户第一次登陆则自动注册一个新用户并返回)

2. /<int: user_id> GET   
   返回用户信息

3. /avatar/<int:user_id>  POST   
   更新用户头像和用户名   


物品相关API 前缀: /api/v1/item

1. ' ' GET   
   返回所有物品信息   

2. /<int:user_id>   GET   
   返回特定用户的所有物品信息

3. /<int:item_id>   PUT   
   修改物品信息

4. /<int:user_id> POST   
   发布物品信息, user_id 为用户id

5. /<int: user_id> DELETE   
   删除物品信息

6. /upload_img  POST   
   上传图片  返回图片地址
