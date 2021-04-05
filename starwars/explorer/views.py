import uuid

from django.shortcuts import render, get_object_or_404
from petl import fromcsv, rowslice, header, valuecounts, cutout
import petl as etl

from .domain.character import download_collection
from .models import Collections
from .utils import EfficientPagination, get_collection_absolut_path


def index(request):
    if request.method == 'POST':
        filename = f'{uuid.uuid4().hex}.csv'
        Collections.objects.create(filename=filename)
        download_collection(get_collection_absolut_path(filename))

    collections = Collections.objects.values_list('id', 'created')
    return render(request, 'explorer/index.html', {'collections': collections})


def collection(request, collection_id):
    col = get_object_or_404(Collections, id=collection_id)
    table = fromcsv(get_collection_absolut_path(col.filename))
    rows_number = etl.nrows(table)
    paginator = EfficientPagination(request.GET.get('slice'), rows_number)
    table = rowslice(table, paginator.start, paginator.end)
    return render(request, 'explorer/collection.html', {'characters': table,
                                                        'collection_id': col.id,
                                                        'filename': col.filename,
                                                        'paginator': paginator})


def counting(request, collection_id):
    col = get_object_or_404(Collections, id=collection_id)
    table = fromcsv(get_collection_absolut_path(col.filename))
    head = header(table)
    if request.method == 'POST':
        data = dict(request.POST)
        del data['csrfmiddlewaretoken']
        del data['submit']
        table = valuecounts(table, *data.keys())
        table = cutout(table, 'frequency')
    return render(request, 'explorer/counting.html', {'table': table, 'head': head,
                                                      'collection_id': col.id,
                                                      'filename': col.filename})
