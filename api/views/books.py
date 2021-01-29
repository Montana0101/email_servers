
import smtplib   
import email   #文件名不可以和引入的库同名
from email.mime.image import MIMEImage   #图片类型邮件
from email.mime.text import MIMEText # MIME 多用于邮件扩充协议
from email.mime.multipart import MIMEMultipart #创建附件类型
from django.http import HttpResponse
import json
import os

def fetchBooks(request):
	body_data = json.loads(request.body.decode())
	title = ""
	email = ""
	content = ""
	source = 'montana0101@qq.com'
	source_key = 'cquqijpmmpezjegd'
	response = {}
	try :
		if body_data['title']:
			 title = body_data['title']
		else:
			 title = 'hey~葛朗台的算板来信'
	except:
		print("异常处理~~title")

	try :
		email = body_data['email']
	except:
		response['code'] = -1
		response['text'] = '没有传入邮箱参数'
		return HttpResponse(json.dumps(response),content_type='application/json')
	
	try :
		content = body_data['content']
		print('打印下收到的信息',content)
	except:
		response['code'] = -1
		response['message'] = '没有传入文本信息'
		return HttpResponse(json.dumps(response),content_type='application/json')
		
	HOST = 'smtp.qq.com'  #调用的邮箱借借口
	SUBJECT = title#设置邮件标题
	FROM = source#发件人的邮箱需先设置开启smtp协议
	TO = email#设置收件人的邮箱（可以一次发给多个人）

	# content = json.loads(content)

	message=MIMEMultipart('alternative')#邮件信息，内容为空  #相当于信封##related表示使用内嵌资源的形式，将邮件发送给对方
	#发送邮件主体到对方邮箱，
	#参数  1.内容必须是字符串
			# 2.内容形式，文本类型默认为plain
			# 3.内容编码使用utf-8
	# message_html=MIMEText('shuai123 消灭不开行','plain','utf-8')
	#将邮件内容，装入邮件信息中
	
	html = ''
	for item in content:
    		html =html + '''
			<main style="width:700px">
			<a style="display:flex;align-items:center;width:100%;height:80px;border:1px solid rgba(222,222,222,0.7);color:black;text-direction:none;" href={url} target="_blank">
				<img src="{img}" style="height:60px;width:60px;"/>
				<div style="width:600px;height:60px;display:flex;flex-direction:column;justify-content:space-between">
				    <div style="display:flex;justify-content:space-between;width:600px">
					   <div style="overflow: hidden;text-overflow:ellipsis;white-space:nowrap;width:80%">{title}</div>
					   <div>{author}</div>
					</div>
					<div style="display:flex;justify-content:space-between;width:100%">
					   <div>¥ {price}</div>
					   <div>{store}</div>
					   <div>{source}</div>
					</div>
				</div>
			</a>
			</main>
			'''.format(img=item['img'],title=item['title'],author=item['author'],
			price=item['price'],source=item['source'],store=item['store'],url=item['url'])

	message.attach(MIMEText(html, 'html','utf-8'))
	
	# ===========发送图片-=============
	# image_data=open('init.jpg','rb')
	# _file = os.path.abspath(__file__)
	# print('dsadsa',_file)
	# with open()
	# message_image = MIMEImage(image_data.read())
	#关闭刚才打开的文件
	# image_data.close()
	# (222)
	# message_image.add_header('Content-ID','small')
	#添加图片文件到邮件信息中去
	# message.attach(message_image)
	#(333)
	# message_image = MIMEText(open('1.gif','rb').read(),'base64','utf-8')
	# message_image['Content-disposition'] = 'attachment;filename="happy.gif"'
	# message.attach(message_image)
	#===========将xlsx文件作为内容发送到对方的邮箱读取excel，rb形式读取，
	# ==对于MIMEText()来说默认的编码形式是base64 对于二进制文件来说没有设置base64，会出现乱码==========
	# message_xlsx = MIMEText(open('table.xlsx','rb').read(),'base64','utf-8')
	# #设置文件在附件当中的名字
	# message_xlsx['Content-Disposition'] = 'attachment;filename="test1111.xlsx"'
	# message.attach(message_xlsx)
	#设置邮件发件人
	message['From']=FROM
	#设置邮件收件人
	message['TO']=TO
	#设置邮件标题
	message['Subject']=SUBJECT
	#获取江建有奖传输协议证书
	try :
		smtpObj= smtplib.SMTP_SSL(HOST)
		smtpObj.connect(HOST,465)# 465 为 SMTP 端口号

		smtpObj.login(FROM, source_key)

		smtpObj.sendmail(FROM, TO, message.as_string())
		response['code'] = 0 
		response['message'] = '成功发送邮件'
		return HttpResponse(json.dumps(response),content_type='application/json')
	except:
		response['code'] = -1
		response['message'] = '邮件发送失败'
		return HttpResponse(json.dumps(response),content_type='application/json')	
 
# email_client = smtplib.SMTP_SSL()
# email_client.connect(HOST,'465')
# #设置发送域名，端口465
# result=email_client.login(FROM,'cquqijpmmpezjegd')#qq

# email_client.sendmail(from_addr=FROM,to_addrs=TO.split(','),msg=message.as_string())
# #关闭邮件发送客户端
# email_client.close()


# 	CREATE TABLE `user` (
#    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
#    `stylist_id` int(11) DEFAULT NULL COMMENT '搭配师id',
#    `mobile` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#    `gender` tinyint(4) DEFAULT NULL COMMENT '10 男  20 女  30 保密',
#    `birthday` datetime DEFAULT NULL COMMENT '生日',
#    `wechat_nickname` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '微信昵称',
#    `wechat_avatar` varchar(600) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '微信头像',
#    `open_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '微信openid',
#    `create_time` datetime NOT NULL COMMENT '创建时间',
#    `update_time` datetime DEFAULT NULL COMMENT '更新时间',
#    `invited_by` int(11) DEFAULT NULL COMMENT '邀请人小B',
#    `vip_survey_result_id` int(11) DEFAULT '0',
#    `height` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#    `weight` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#    `stylist_remark` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#    `blacklist` tinyint(1) DEFAULT '0',
#    `wechat_mobile` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#    `balance` decimal(10,3) DEFAULT '0.000',
#    `real_paid_balance` decimal(10,3) NOT NULL DEFAULT '0.000',
#    `channel_id` int(11) DEFAULT '0',
#    `invitation_code` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#    `superior` int(11) DEFAULT NULL,
#    `points` int(11) DEFAULT '0',
#    `open_gid` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#    PRIMARY KEY (`id`),
#    UNIQUE KEY `mobile` (`mobile`),
#    UNIQUE KEY `invitation_code` (`invitation_code`),
#    UNIQUE KEY `open_id_UNIQUE` (`open_id`),
#    KEY `superior` (`superior`)
#  ) ENGINE=InnoDB AUTO_INCREMENT=31084 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='user'