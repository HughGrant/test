# from django.shortcuts import render
import json
from django.http import JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from products.models import *


class UpdateByModel(View):

    def get(self, request):
        jr = {'status': True, 'message': ''}
        data = {}
        email = request.GET['email']
        pid = request.GET['pid']
        model = request.GET.get('model')

        df = DifferentPrice.objects.filter(model=model)
        if not df.exists():
            jr['status'] = False
            jr['message'] = '没有产品型号:%s' % model
            return JsonResponse(jr)

        ext = df.get().extend

        if not ext.content:
            jr['status'] = False
            jr['message'] = '没有型号产品%s的正文' % model
            return JsonResponse(jr)

        title = data['name'] = ext.title_by_email_model(email, model, pid)
        data['keywords'] = ext.keywords()
        data['model'] = model
        data['extend_id'] = ext.id
        data['basic_id'] = ext.basic.id
        data['category'] = ext.category.slug_name().split('>')

        data['attrs'] = []
        for attr in ext.attr_set.filter(Q(model=model) | Q(model='')):
            data['attrs'].append([attr.name, attr.value])
        data['attrs'].append(['Model Number', model])

        s = '3-7 days based on destination, shipping by DHL/FedEx/UPS etc.'
        data['consignment_term'] = s
        data['packaging_desc'] = 'standard export packaging, safe and secure'
        data['port'] = 'NingBo'
        default_payment_terms = 'T/T,Western Union,MoneyGram,PayPal'
        data['payment_terms'] = default_payment_terms.split(',')

        data['min_order_quantity'] = ext.moq.min_order_quantity
        data['min_order_unit'] = ext.moq.min_order_unit

        # USD
        data['money_type'] = 1
        dp = ext.basic.differentprice_set.filter(model=model)[0]
        data['price_range_min'] = dp.min_profit()
        data['price_range_max'] = dp.max_profit()
        # set/sets
        data['price_unit'] = 20

        data['supply_quantity'] = ext.supply_ability.supply_quantity
        data['supply_unit'] = ext.supply_ability.supply_unit
        data['supply_period'] = ext.supply_ability.supply_period
        data['rich_text'] = ext.content.replace('{{title}}', title)

        jr['data'] = data
        return JsonResponse(jr)

    def post(self, request):
        pass

    @method_decorator(login_required(login_url='/login_required_jr/'))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CaptureView(View):

    def get(self, request):
        jr = {'status': False, 'message': ''}
        pk = request.GET.get('id')
        model = request.GET.get('model')

        ext = Extend.objects.get(pk=int(pk))
        data = {}
        data['extend_id'] = ext.id
        data['basic_id'] = ext.basic.id
        data['model'] = model
        data['category'] = ext.category.slug_name().split('>')

        data['attrs'] = []
        for attr in ext.attr_set.all():
            data['attrs'].append([attr.name, attr.value])

        s = '3-7 days based on destination, shipping by DHL/FedEx/UPS etc.'
        data['consignment_term'] = s
        data['packaging_desc'] = 'standard export packaging, safe and secure'
        data['port'] = 'NingBo'
        default_payment_terms = 'T/T,Western Union,MoneyGram,PayPal'
        data['payment_terms'] = default_payment_terms.split(',')

        data['min_order_quantity'] = ext.moq.min_order_quantity
        data['min_order_unit'] = ext.moq.min_order_unit

        # USD
        data['money_type'] = 1
        dp = ext.basic.differentprice_set.filter(model=model)[0]
        data['price_range_min'] = dp.min_profit()
        data['price_range_max'] = dp.max_profit()
        # set/sets
        data['price_unit'] = 20

        data['supply_quantity'] = ext.supply_ability.supply_quantity
        data['supply_unit'] = ext.supply_ability.supply_unit
        data['supply_period'] = ext.supply_ability.supply_period
        data['rich_text'] = ext.content

        jr['status'] = True
        jr['data'] = data
        return JsonResponse(jr)

    def post(self, request):
        jr = {'status': False}
        if not request.user.has_perm('products.add_extend'):
            raise PermissionDenied()

        pd = json.loads(request.POST['json'])

        ext = Extend(user=request.user)
        ext.category = Category.auto_create(pd['category'])

        ext.moq = MOQ.objects.get_or_create(
            min_order_quantity=pd['min_order_quantity'],
            min_order_unit=pd['min_order_unit'])[0]

        ext.supply_ability = SupplyAbility.objects.get_or_create(
            supply_quantity=pd['supply_quantity'],
            supply_unit=pd['supply_unit'],
            supply_period=pd['supply_period'])[0]

        ext.save()

        for attr in pd['attrs']:
            Attr(extend=ext, name=attr[0], value=attr[1]).save()

        jr['status'] = True
        return JsonResponse(jr)

    @method_decorator(login_required(login_url='/login_required_jr/'))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TitleKeywordView(View):

    def post(self, request):
        model = request.POST['model']
        words = request.POST.getlist('words[]')
        kws = []
        for word in words:
            kw = TitleKeyword(model=model, word=word, user=request.user)
            try:
                kw.validate_unique()
            except ValidationError:
                pass
            else:
                kws.append(kw)
        if kws:
            TitleKeyword.objects.bulk_create(kws)
        return JsonResponse({'status': True})

    def get(self, request):
        model = request.GET['model']
        data = {'title': '', 'word': ''}
        tk = TitleKeyword.get_pair(model)
        if tk:
            data['title'] = tk.title
            data['word'] = tk.word
        return JsonResponse(data)

    @method_decorator(login_required(login_url='/login_required_jr/'))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
