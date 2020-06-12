## 飞书 sdk

第三方Feishu库，目前只实现了使用的`机器人`部分功能，后续会看精力继续完善

### 导入
```python
from feishu.Application import Bot

bot = Bot(app_id='xxxxxxxxxxxxxxx', app_secret="xxxxxxxxxxxxxxx")
```

### 事前准备

测试的话需要给自己发送消息，我们需要一个飞书的[登录预授权码](https://open.feishu.cn/document/ukTMukTMukTM/ukzN4UjL5cDO14SO3gTN)
注意失效，仅为5分钟

你需要在[飞书开放平台](https://open.feishu.cn/) 所测试的机器人 -> 安全设置中 添加一个重定向URL,内容为`https://example.com`

然后下面方法或手动拼接，获取一个地址，类似于 https://open.feishu.cn/open-apis/authen/v1/index?app_id=xxxxxxxxx&redirect_uri=https://example.com&state= `，在浏览器中打开，登录后,从地址栏中拿到预授权码
``` python
print(bot.get_authorization_code_by_browser_url())
```

然后获取你自己的 open_id
``` python
print(bot.get_user_info(code='上面获取的预授权码'))
```

### 部分功能实例

#### 获取Token
``` python
# 租户Token
print(bot.get_tenant_access_token())
# app Token
print(bot.get_app_access_token())
```

#### 创建群组
``` python
bot.create_group(name="测试测试", open_ids=['xxxxxxx'])
```

#### 发送文字消息
``` python
bot.send_user_message(user_open_id="xxxxxxxxxxxxx", text='测试消息')
```

#### 发送卡片消息
``` python
bot.send_user_card_message(user_open_id="ou_b7fd6a20da4e3903bc2324b71232c5ac", title="测试标题", text="测试内容")
```

#### 发送复杂卡片消息
``` python
message_config = {
            'title': '上线任务审批通知',
            'action': '上线审批',
            'system': '，'.join(['a', 'b', 'c']),
            'reason': '因为地球毁灭',
            'detail': '用户：xxxx 申请发布服务，您可以确认。',
            'button': [
                {
                    'title': '同意',
                    'type': 'primary',
                    'value': {
                        'action': 'approval_online_order',
                        'order_id': '12345',
                        'option': 'agree'
                    },
                },
                {
                    'title': '拒绝',
                    'type': 'danger',
                    'value': {
                        'action': 'approval_online_order',
                        'order_id': '12345',
                        'user_id': '123',
                        'option': 'disagree'
                    }
                },
            ]
        }
bot.send_user_card_message(user_open_id="ou_b7fd6a20da4e3903bc2324b71232c5ac", **message_config)
```

#### 卡片消息格式自定义
``` python
bot.configuration_card_message(image_key="img_5abe5193-14df-4b7d-af6f-15fac38c485g", 
                               button_confirm=False, 
                               name='123', 
                               auto_add_time=True
                               )

bot.send_user_card_message(user_open_id="ou_b7fd6a20da4e3903bc2324b71232c5ac", **message_config)
```
