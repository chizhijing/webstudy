from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Article
# Create your views here.

def hello_world(request):
    return HttpResponse('Hello World')

def article_content(request):
    article = Article.objects.all()[0]
    title = article.title
    brief_content=article.brief_content
    content=article.content
    id=article.article_id
    p_d=article.publish_date
    return_str='title: %s, brief content: %s, content: %s, id: %s, pd:%s' % (title,brief_content,content,id,p_d)
    return HttpResponse(return_str)

def get_index_page(request):
    all_article = Article.objects.all()
    return render(request, 'blog\index.html', {'article_list':all_article})

def get_detail_page(request,article_id):
    all_article=Article.objects.all()
    current_article=None
    pre_article=None
    next_article=None
    pre_index=0
    next_index=0
    for index,article in enumerate(all_article):
        if index==0:
            pre_index=0
            next_index=index+1
        elif index==len(all_article)-1:
            pre_index=index-1
            next_index=index
        else:
            pre_index=index-1
            next_index=index+1
        if article.article_id==article_id:
            current_article=article
            pre_article = all_article[pre_index]
            next_article = all_article[next_index]
            break

    return render(request, 'blog\detail.html', {'current_article':current_article,
                                                'previous_article':pre_article,
                                                'next_article':next_article})