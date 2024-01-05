from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.template import Template, Context

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

def only_client_permited(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser or not request.user.is_authenticated:
            return redirect("/usuarios/login")
        else:
            return view_func(request, *args, **kwargs)

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


def do_pagination(number_page, itens_key, itens, number_of_itens):    

    paginator = Paginator(itens, number_of_itens)
    
    return {   
        itens_key : paginator.page(number_page).object_list,
        'pagination' : Template(process_template_string()).render(
            Context({
                'page': paginator.page(number_page),
                'lower_limit': max(paginator.page(number_page).number - 5, 1),
                'upper_limit': min(paginator.page(number_page).number + 5, paginator.num_pages)
            }))
    }
    
def process_template_string():
    return '''
    {% if page.paginator.num_pages > 1 %}
        <div class="row mt-4">
            <nav aria-label="Page navigation example">
                <ul class="pagination justify-content-center">
                 
                    {% if page.has_previous %}
                        <li class="page-item m-1">
                            <a class="page-link text-dark border border-dark pe-4 ps-4 rounded-5 fw-bold"
                                href="?page={{ page.previous_page_number }}" tabindex="-1"><i class="fa-solid fa-caret-left"></i></a>
                        </li>
                    {% endif %}
                    {% for num in page.paginator.page_range %}
                        {% if num == page.number %}
                            <li class="page-item m-1"><a class="page-link active border border-dark rounded-5 fw-bold"
                                href="?page={{ page.number }}">{{ num }}</a></li>
                        {% elif num > lower_limit and num < upper_limit %}
                            <li class="page-item m-1"><a
                                class="page-link   text-dark border border-dark rounded-5 fw-bold" href="?page={{ num }}">{{num}}</a></li>
                        {% endif %}
                    {% endfor %}
                    {% if page.has_next %}
                        <li class="page-item m-1">
                            <a class="page-link  text-dark border border-dark  pe-4 ps-4 rounded-5 fw-bold"
                                href="?page={{ page.next_page_number }}"><i class="fa-solid fa-caret-right"></i></a>
                        </li>
                    {% endif %}
            
                </ul>
            </nav>
        </div>
    {% endif %}
    '''