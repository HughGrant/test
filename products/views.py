# from django.shortcuts import render
import json
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import F
from products.models import *


class CaptureView(View):

    def get(self, request):
        jr = {'status': False, 'message': 'test ok'}
        pk = request.GET.get('id')
        if not pk:
            jr['message'] = 'lack of id'
            return JsonResponse(jr)

        ext = Extend.objects.get(pk=int(pk))
        data = {}
        data['extend_id'] = ext.id
        data['name'] = ext.basic.name
        data['category'] = ext.category.slug_name().split('>')
        data['port'] = ext.port
        data['consignment_term'] = ext.consignment_term
        data['packaging_desc'] = ext.packaging_desc

        data['attrs'] = []
        for attr in ext.attr_set.all():
            data['attrs'].append([attr.name, attr.value])

        data['photos'] = []
        for photo in ext.picture_set.all():
            data['photos'].append(photo.url)

        data['payment_terms'] = ext.payment_terms.split(',')

        data['min_order_quantity'] = ext.moq.min_order_quantity
        data['min_order_unit'] = ext.moq.min_order_unit

        data['money_type'] = ext.fob_price.money_type
        data['price_range_min'] = ext.fob_price.price_range_min
        data['price_range_max'] = ext.fob_price.price_range_max
        data['price_unit'] = ext.fob_price.price_unit

        data['supply_quantity'] = ext.supply_ability.supply_quantity
        data['supply_unit'] = ext.supply_ability.supply_unit
        data['supply_period'] = ext.supply_ability.supply_period
        data['rich_text'] = ext.rich_text

        jr['status'] = True
        jr['data'] = data
        return JsonResponse(jr)

    def post(self, request):
        jr = {'status': False}
        pd = json.loads(request.POST['json'])

        basic = Basic(user=request.user)
        basic.name = pd['name']
        basic.save()

        ext = Extend(basic=basic)
        ext.category = Category.auto_create(pd['category'])
        ext.url = pd['url']
        ext.port = pd['port']
        ext.consignment_term = pd['consignment_term']
        ext.packaging_desc = pd['packaging_desc']
        ext.payment_terms = ','.join(pd['payment_terms'])

        ext.moq = MOQ.objects.get_or_create(
            min_order_quantity=pd['min_order_quantity'],
            min_order_unit=pd['min_order_unit'])[0]

        ext.fob_price = FobPrice.objects.get_or_create(
            money_type=pd['money_type'],
            price_range_min=pd['price_range_min'],
            price_range_max=pd['price_range_max'],
            price_unit=pd['price_unit'])[0]

        ext.supply_ability = SupplyAbility.objects.get_or_create(
            supply_quantity=pd['supply_quantity'],
            supply_unit=pd['supply_unit'],
            supply_period=pd['supply_period'])[0]

        ext.save()

        has_voltage = False
        for attr in pd['attrs']:
            Attr(extend=ext, name=attr[0], value=attr[1]).save()
            if attr[0].lower() == 'voltage':
                has_voltage = True

        if has_voltage:
            basic.voltage = 220
            basic.save()

        for photo in pd['photos']:
            Picture(extend=ext, url=photo).save()

        jr['status'] = True
        return JsonResponse(jr)

    @method_decorator(login_required(login_url='/login_required_jr/'))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UploaderView(View):

    def post(self, request):
        eid = request.POST['extend_id']
        Extend.objects.filter(pk=eid).update(
            upload_count=F('upload_count') + 1)
        return JsonResponse({'status': True})

    def get(self, request):
        jr = {'status': False}
        return JsonResponse(jr)

    @method_decorator(login_required(login_url='/login_required_jr/'))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class KeywordView(View):

    def post(self, request):
        name = request.POST['name']
        words = request.POST.getlist('words[]')
        kws = []
        for word in words:
            if word != name:
                kw = Keyword(name=name, word=word)
                try:
                    kw.validate_unique()
                except ValidationError:
                    pass
                else:
                    kws.append(kw)
        if kws:
            Keyword.objects.bulk_create(kws)
        return JsonResponse({'status': True})

    def get(self, request):
        jr = {'status': False}
        name = request.GET['name'].lower()
        count = int(request.GET['count'])

        # TODO possible optimization in the future
        re = Keyword.objects.filter(name=name).order_by('count')[:count]
        if re.count() == count:
            jr['status'] = True
            jr['result'] = []
            for kw in re:
                jr['result'].append(kw.word)
                kw.count += 1
                kw.save()

        return JsonResponse(jr)

    @method_decorator(login_required(login_url='/login_required_jr/'))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
