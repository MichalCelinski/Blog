import smtplib
from email.mime.text import MIMEText
from myblog.local_settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER


def send_article(article, form, article_url):
    cleaned_data = form.cleaned_data
    message = MIMEText(u'Przeczytaj <a href="{}">{}</a><br>dodatkowa wiadomość: {}'
                       .format(article_url, article_url, cleaned_data['message']), 'html')
    message['Subject'] = '{} zaprasza do lektury "{}"'.format(cleaned_data['sender'], article)
    message['From'] = cleaned_data['sender']
    message['To'] = cleaned_data['email_receiver']
    smtp_server = smtplib.SMTP('smtp.gmail.com:587')
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.ehlo()
    smtp_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    smtp_server.sendmail(EMAIL_HOST_USER, cleaned_data['email_receiver'], message.as_string())
    smtp_server.quit()
    sent = True
    return sent, message['To']
