import xlwt
import datetime

from django.http import HttpResponse, HttpResponseForbidden
from django.db.models.loading import get_models, get_app
from django.template.defaultfilters import slugify


def dump(request):
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=PennCycle-Database-Dump-%s.xls' % (str(datetime.datetime.today()))

    if not request.user.is_staff:
        return HttpResponseForbidden()

    wb = xlwt.Workbook()
    excel_date_fmt = 'M/D/YY h:mm'
    datestyle = xlwt.XFStyle()
    datestyle.num_format_str = excel_date_fmt
    plainstyle = xlwt.XFStyle()

    app = get_app('app')
    models = get_models(app)

    for model in models:
        name = model.__name__
        print name
        if name == 'Plan':
            break
        ws = wb.add_sheet(slugify(name))
        xl_export(model, ws, datestyle, plainstyle)

    wb.save(response)
    return response


def xl_export(model, ws, datestyle, plainstyle):
    fields = model._meta.fields
    headers = [f.name for f in fields]
    for colx, val in enumerate(headers):
        ws.write(0, colx, val)
    queryset = model.objects.all()
    for rowx, obj in enumerate(queryset):
        for colx, field in enumerate(headers):
            if field in headers:
                val = getattr(obj, field)
                print type(val)
                if callable(val):
                    val = val()
                # val = encoding.smart_str(val, encoding='ascii', errors='ignore')
                print type(val)
                fieldtype = fields[colx].get_internal_type()
                if fieldtype in ['IntegerField', 'FloatField', 'AutoField']:
                    print "It's an number!"
                    val = float(val)
                if fieldtype in ['ForeignKey', 'ManyToMany', 'OneToOne', 'ImageField', 'FileField']:
                    val = str(val)
                if fieldtype == 'DateTimeField':
                    thisstyle = datestyle
                else:
                    thisstyle = plainstyle
                print fieldtype
            ws.write(rowx+1, colx, val, thisstyle)
    return None
