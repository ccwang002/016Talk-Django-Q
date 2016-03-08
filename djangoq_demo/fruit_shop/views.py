import logging
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django_q.humanhash import humanize
from django_q.models import OrmQ
from django_q.tasks import async, Task

logger = logging.getLogger(__name__)


def home(request):
    if request.method == 'POST':
        # Parse the form params
        try:
            fruit = request.POST.get('fruit_type', '')
            num_fruit = int(request.POST.get('num_fruit', '1'))
        except ValueError:
            return HttpResponseBadRequest('Invalid fruit request!')
        # Create async task
        task_id = async(
            'fruit_shop.tasks.order_fruit',
            fruit=fruit, num_fruit=num_fruit
        )
        messages.info(
            request,
            'You ordered {fruit:s} x {num_fruit:d} (task: {task})'
            .format(fruit=fruit, num_fruit=num_fruit, task=humanize(task_id))
        )

    # Select orders in queue
    queue_orders = OrmQ.objects.all().order_by('lock')

    # Select finished orders
    complete_orders = Task.objects.all().filter(
        func__exact='fruit_shop.tasks.order_fruit',
    )
    return render(request, 'index.html', {
            'queue_orders': queue_orders,
            'complete_orders': complete_orders
    })
