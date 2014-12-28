# from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from products.models import Keyword


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
