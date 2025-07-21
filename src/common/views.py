
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def render_messages_view(request: HttpRequest) -> HttpResponse:
    """
    View simples que apenas renderiza as mensagens pendentes.
    É chamada pelo HTMX quando o evento 'display-message' é disparado.
    """
    return render(request, 'shared/messages.html')
