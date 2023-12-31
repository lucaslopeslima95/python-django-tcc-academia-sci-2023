import os
from datetime import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from weasyprint import HTML
from Purchase.models import info_utils


def generate_pdf(nameUser, purchase_itens, total, date, hour):
    template = get_template('emails/confirm_purchase_pdf.html')
    context = {'nome': nameUser, 'purchase_itens': purchase_itens,
               'total': total, 'date': date, 'hour': hour}
    html = template.render(context)
    pdf_file_path = 'comprovante.pdf'
    HTML(string=html).write_pdf(target=pdf_file_path)
    return pdf_file_path


@shared_task()
def confirm_purchase(email, nameUser,
                     purchase_itens):
    try:
        total = 0
        is_ticket = False
        is_shirt = False
        for product in purchase_itens.items():
            if (product[1]['price'] and product[1]['quantity']):
                total += (product[1]['price']*product[1]['quantity'])
                if product[1]['category'] == 'Ingressos':
                    is_ticket = True
                if product[1]['category'] == 'Camisetas':
                    is_shirt = True

        email_to = []
        email_to.append(email)
        if is_ticket:
            email_to.append(info_utils.objects.get(id=1).email_rh)

        if is_shirt:
            email_to.append(info_utils.objects.get(id=1).email_marketing)
        now = datetime.now()
        data_hora_formatada = now.strftime("%d/%m/%Y %H:%M")
        date, hour = data_hora_formatada.split(" ")
        html_content = render_to_string(
            'emails/confirm_purchase.html',
            {'nome': nameUser, 'purchase_itens': purchase_itens,
             'total': total, 'date': date, 'hour': hour})
        text_cotent = strip_tags(html_content)
        email = EmailMultiAlternatives(
            'Comprovante de Compras',
            text_cotent,
            settings.EMAIL_HOST_USER,
            email_to,
            )
        path_to_pdf = generate_pdf(
            nameUser=nameUser,
            purchase_itens=purchase_itens,
            total=total, date=date, hour=hour)
        email.attach_file(path_to_pdf)
        email.attach_alternative(html_content, "text/html")
        email.send()
        delete_pdf(path_to_pdf)
    except Exception as e:
        print(f" Exceção ao tentar enviar um email - {e}")


def delete_pdf(path_to_pdf):
    if os.path.exists(path_to_pdf):
        os.remove(path_to_pdf)
        print(f"Email enviado Com sucesso\
              e Arquivo {path_to_pdf} foi excluído com sucesso.")
    else:
        print(f"O arquivo {path_to_pdf} não existe.")
