#!/usr/bin/python3
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
import requests
from urllib.request import urlopen
import json
import sys

accessKeyId = "accesskeyid"  # 账户的accessKeyId
accessSecret = "accesssecret"  # 账户的accessSecret
domain = "domain"  # 主域名
sub_domain = sys.argv[3]  # 要进行解析的子域名
value = sys.argv[4] # 解析值，如ip地址，域名，与解析类型有关
type = sys.argv[2] # 解析类型，如A，CNAME
action = sys.argv[1] #操作，入add，update，delete


client = AcsClient(accessKeyId, accessSecret, 'cn-shanghai')

def update(RecordId, RR, Type, Value):  # 修改域名解析记录
    from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    request.set_RecordId(RecordId)
    request.set_RR(RR)
    request.set_Type(Type)
    request.set_Value(Value)
    response = client.do_action_with_exception(request)

def add(DomainName, RR, Type, Value):  # 添加新的域名解析记录
    from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
    request = AddDomainRecordRequest()
    request.set_accept_format('json')
    request.set_DomainName(DomainName)
    request.set_RR(RR)
    request.set_Type(Type)
    request.set_Value(Value)
    response = client.do_action_with_exception(request)

def delete(RecordId):  # 删除域名解析记录
    from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
    request = DeleteDomainRecordRequest()
    request.set_accept_format('json')
    request.set_RecordId(RecordId)
    response = client.do_action_with_exception(request)

request = DescribeSubDomainRecordsRequest()
request.set_accept_format('json')
request.set_DomainName(domain)
request.set_SubDomain(sub_domain + '.' + domain)
request.set_Type(type)
response = client.do_action_with_exception(request)  # 获取域名解析记录列表
domain_list = json.loads(response)  # 将返回的JSON数据转化为Python能识别的

if action == "add": # 添加解析
    if domain_list['TotalCount'] == 0: # 未找到记录，则添加新记录
        add(domain, sub_domain, type, value)
        print("新建域名解析"+sub_domain+"."+domain+"成功")
    elif domain_list['TotalCount'] == 1: # 找到一条记录，且与预期不符，更新记录
        if domain_list['DomainRecords']['Record'][0]['Value'].strip() != value.strip():
            update(domain_list['DomainRecords']['Record'][0]['RecordId'], sub_domain, type, value)
            print("修改域名解析"+sub_domain+"."+domain+"成功")
        else:                            # 找到一条记录且与预期符合，不作任何操作
            print("域名解析"+sub_domain+"."+domain+"没变")
    elif domain_list['TotalCount'] > 1:  # 找到多条记录，删除并新增记录
        for i in range(len(domain_list['DomainRecords']['Record'])):
            delete(domain_list['DomainRecords']['Record'][i]['RecordId'])
        add(domain, sub_domain, type, value)
        print("修改域名解析"+sub_domain+"."+domain+"成功")
elif action == "delete": # 删除解析
    if domain_list['TotalCount'] == 0: # 未找到记录，不作任何操作
        print("无此域名解析"+sub_domain+"."+domain+"记录")
    elif domain_list['TotalCount'] >= 1: # 找到一条或多条记录，删除之
        for i in range(len(domain_list['DomainRecords']['Record'])):
            delete(domain_list['DomainRecords']['Record'][i]['RecordId'])
        print("删除域名解析"+sub_domain+"."+domain+"成功")
elif action == "update":   # 更新记录
    if domain_list['TotalCount'] == 0: # 未找到记录，新增记录
        print("无此域名解析"+sub_domain+"."+domain+"记录")
        add(domain, sub_domain, type, value)
        print("新增域名解析"+sub_domain+"."+domain+"成功")
    elif domain_list['TotalCount'] >= 1: #找到一条或多条记录，删除之后再新增
        for i in range(len(domain_list['DomainRecords']['Record'])):
            delete(domain_list['DomainRecords']['Record'][i]['RecordId'])
        add(domain, sub_domain, type, value)
        print("修改域名解析"+sub_domain+"."+domain+"成功")
