from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.shortcuts import redirect

def superuser_required(view_func):
    """
    Decorator que verifica se o usuário é um superusuário.
    Redireciona para uma página de acesso negado caso contrário.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("/usuarios/login")

    return _wrapped_view


def send_code_by_email(instance, code):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587 
    smtp_username = 'durvaljunior117@gmail.com'
    smtp_password = 'zfmn gqqm unvr wfxj'

    sender_email = smtp_username
    receiver_email =  instance.email
    subject = 'Codígo de Acesso a Conta'
    body = f'''
        <html>
            <head>
                <style>
                    /* Adicione estilos CSS aqui, se necessário */
                </style>
            </head>
            <body>
                <h1>Olá {instance.first_name}!</h1>
                <p>
                    Você foi cadastrado como usuário na plataforma Na Mosca! O código abaixo é sua senha, a qual permite que você possa se autenticar no sistema. Após estar autenticado, você pode alterar sua senha ao entrar em seu perfil.
                </p>
                <p>
                    <strong>Código:</strong> {code}
                </p>
                <p>
                    <a href="http://127.0.0.1:8000/usuarios/perfil/">Acesse o sistema aqui!</a>
                </p>
            </body>
        </html>
    '''

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
