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

        data['money_type'] = ext.fob_price.money_type
        data['price_range_min'] = ext.fob_price.price_range_min
        data['price_range_max'] = ext.fob_price.price_range_max
        data['price_unit'] = ext.fob_price.price_unit

        data['supply_quantity'] = ext.supply_ability.supply_quantity
        data['supply_unit'] = ext.supply_ability.supply_unit
        data['supply_period'] = ext.supply_ability.supply_period
        data['rich_text'] = ext.richtext_set.filter(model=model).get().content

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
        ext.port = pd['port']
        if pd['rich_text']:
            ext.rich_text = pd['rich_text']

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

        for attr in pd['attrs']:
            Attr(extend=ext, name=attr[0], value=attr[1]).save()

        jr['status'] = True
        return JsonResponse(jr)

    @method_decorator(login_required(login_url='/login_required_jr/'))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class KeywordView(View):

    def post(self, request):
        basic_id = request.POST['basic_id']
        words = request.POST.getlist('words[]')
        kws = []
        for word in words:
            kw = Keyword(basic_id=basic_id, word=word)
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
        pass
        # basic_id = int(request.GET['basic_id'])
        # kws = Basic.objects.filter(pk=basic_id).get().keywords()
        # return JsonResponse(kws)

    @method_decorator(login_required(login_url='/login_required_jr/'))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TitleKeyView(View):

    def post(self, request):
        pass

    def get(self, request):
        model = request.GET['model']
        email = request.GET['email']
        data = {'name': 'no model find %s' % model, 'keywords': []}
        rt = RichText.objects.filter(model=model)
        if rt.exists():
            ext = rt.get().extend
            data['name'] = ext.title_by_email_model(email, model)
            data['keywords'] = ext.basic.keywords()
        return JsonResponse(data)

    @method_decorator(login_required(login_url='/login_required_jr/'))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TrackingListView(View):

    def get(self, request):
        pass

    def post(self, request):
        plist = json.loads(request.POST['json'])
        tls = []
        edit = 0
        for p in plist:
            q = TrackingList.objects.filter(
                account=p['account'], title=p['title'], model=p['model'])
            if q.exists():
                t = q.get()
                # first, set pid for those uploaded product
                if not t.pid:
                    t.pid = p['pid']
                    t.save()
                    edit += 1
                else:
                    # second, upate by pid for already tracked product
                    if t.title != p['title'] or t.model != p['model']:
                        t.title = p['title']
                        t.model = p['model']
                        t.save()
                        edit += 1
            else:
                # last, append these not tracked products
                tls.append(TrackingList(**p))
        if tls:
            TrackingList.objects.bulk_create(tls)
        msg = '成功检索并添加%d个, 更新%d产品' % (len(tls), edit)
        return JsonResponse({'status': True, 'msg': msg})

    @method_decorator(login_required(login_url='/login_required_jr/'))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
