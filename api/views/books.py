
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
	title = "hey~葛朗台的算板来信"
	email = ""
	content = ""
	source = '****@qq.com'
	source_key = '*****'
	response = {}
	try :
		if body_data['title']:
			 title = body_data['title']
		else:
			 title = 'hey~（葛朗台的算板）来信'
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
	
	html = '<h2 style="width:700px;display:flex;justify-content:center;align-items:center">点击进行跳转</h2>'
	for item in content:
    		html =html + '''
			<main style="width:700px;box-sizing:border-box;margin-top:20px;">
			<a style="display:flex;align-items:center;width:100%;height:80px;border:1px solid rgba(222,222,222,0.7);color:black;text-decoration:none;" href={url} target="_blank">
				<img src="{img}" style="height:60px;width:60px;margin:0 20px;"/>
				<div style="width:580px;padding-right:20px;height:60px;display:flex;flex-direction:column;justify-content:space-between">
				    <div style="display:flex;justify-content:space-between;width:580px">
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
 
