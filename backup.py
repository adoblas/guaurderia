from datetime import datetime
import os
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


hoy = datetime.now().date().strftime("%d_%m_%Y")

shutil.make_archive(hoy, 'zip', "/home/guaurderia/web2py/applications/guaurderia/databases")
ruta_zip = "/home/guaurderia/" + hoy + ".zip"

username = "aliasali257@gmail.com"
password = "furlteaqbsagfryi"
mail_from = "aliasali257@gmail.com"
mail_to = "aliasali257@gmail.com"
mail_subject = "Backup de " + hoy
mail_body = "Este es el zip que contiene la base de datos"
mail_attachment=ruta_zip
mail_attachment_name=hoy + ".zip"

mimemsg = MIMEMultipart()
mimemsg['From']=mail_from
mimemsg['To']=mail_to
mimemsg['Subject']=mail_subject
mimemsg.attach(MIMEText(mail_body, 'plain'))

with open(mail_attachment, "rb") as attachment:
    mimefile = MIMEBase('application', 'octet-stream')
    mimefile.set_payload((attachment).read())
    encoders.encode_base64(mimefile)
    mimefile.add_header('Content-Disposition', "attachment; filename= %s" % mail_attachment_name)
    mimemsg.attach(mimefile)
    connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
    connection.starttls()
    connection.login(username,password)
    connection.send_message(mimemsg)
    connection.quit()

if os.path.exists(hoy + ".zip"):
  os.remove(hoy + ".zip")
  print("Fichero borrado")
else:
  print("The file does not exist")