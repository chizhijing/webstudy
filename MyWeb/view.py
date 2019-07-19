from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from .forms_forex import SymbolSelectForm
from django.forms import formset_factory
from random import randint

# def hello(request):
#     # return HttpResponse("Hello world ! ")
#     context={}
#     context['hello']='Hello World!'
#     return render(request,'hello.html',context)

def hello(request):
    d={'总利润':100,'交易次数':10}
    s_key=list(d.keys())
    s_value=list(d.values())
    context={}

    context['account_title'] = '账户信息分析'
    context['statics_key']=s_key
    context['statics_value']=s_value

    return render(request,'hello.html',context)

class MyForm(forms.Form):
    user=forms.CharField(label='用户名')
    age = forms.IntegerField(label='年龄')
    email = forms.EmailField()
    user.label='111'
    def set_label(self,l='xxx'):
        MyForm.user.label=l

class ForexAccountForm(forms.Form):
    plat_choice=forms.ChoiceField(label='账户选择',choices=(('Aus-11','澳汇'),('IB-12','盈透')))
    s_test=forms.BooleanField(label='XAUUSD',required=False)

    symbol_select=['XAUUSD','USDJPY']
    symbol_bool=[forms.BooleanField(label=s, required=True) for s in symbol_select]

def account(request):
    if request.method=='POST':
        form_account=ForexAccountForm(request.POST)
        if form_account.is_valid():
            return HttpResponse('外汇账户统计')
    else:
        form_account=ForexAccountForm()
        return  render(request,'forex_account.html',{'form_account':form_account})


def reg2(request):
    if request.method=='POST':
        form_post=MyForm(request.POST)
        if form_post.is_valid():
            msg='用户名:'+form_post.cleaned_data['user']
            return HttpResponse('提交成功'+msg)
    else:
        form_obj=MyForm()
        form_obj.set_label()
        return render(request,'reg2.html',{'form_obj':form_obj})

def manage_symbols(request):
    if request.method=='POST':
        SymbolFormSet = formset_factory(SymbolSelectForm)
        formset=SymbolFormSet(request.POST)
        if formset.is_valid():
            pass
    else:
        # num1=randint(4,8)
        # num2=randint(2,6)
        symbols=['XAUUSD','EURUSD','USDJPY','GBPUSD','AUDUSD','NZDUSD','USDCAD']
        num1 = len(symbols)
        num2 = len(symbols)
        SymbolFormSet = formset_factory(SymbolSelectForm, extra=num1, max_num=num2)
        formset=SymbolFormSet()

        result =[(s,foo) for foo,s in zip(formset,symbols)]

        return render(request, 'manage_symbol.html', {'result': result})
        # return render(request,'manage_symbol.html',{'formset':formset,'s_list':symbols})