## 说明
- 魔改自：[-Python-aliddns_ipv4-ipv6][1],修复了一些错误，新增了操作选项

## 使用方法
- 1.安装依赖库
```
pip install aliyun-python-sdk-core-v3
pip install aliyun-python-sdk-domain
pip install aliyun-python-sdk-alidns
pip install requests
```

若安装失败，请更新pip源
```
mkdir ~/.pip
vim ~/.pip/pip.conf

[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com

pip install --upgrade pip
```

- 2.修改配置
```
accessKeyId = "accesskeyid"  # 账户的accessKeyId
accessSecret = "accesssecret"  # 账户的accessSecret
domain = "domain"  # 主域名
```

- 3.执行脚本
```
./alidns.py 操作 解析记录类型 子域名前缀 值
```

### 操作支持
- add：新增，没有记录就新增一条，有一条记录就更新，有多条记录就删除所有再新增
- delete：删除，没有记录就不操作，有一条或者多条记录就全部删除
- update：更新，没有记录就新增一条，有一条就更新，有多条就删除全部再新增

### 解析记录支持
- A:将域名指向一个IPV4地址
- CNAME:将域名指向另外一个域名
- AAAA:将域名指向一个IPV6地址
- NS:将子域名指向其他dns服务器解析
- MX:将域名指向其他邮件服务器地址
- SRV:记录提供特定的服务的服务器
- TXT:文本长度限制512，通常做SPF记录（反垃圾邮件）
- CAA:CA证书颁发机构授权校验

## 示例

```
./alidns.py add A kkk 192.168.31.65
./alidns.py add AAAA kkk fe80::e2e:a91f:8ad1:5d09
./alidns.py delete A kkk 192.168.31.65
./alidns.py update CNAME kkk www.baidu.com
```

[1]: https://github.com/zeruns/-Python-aliddns_ipv4-ipv6
