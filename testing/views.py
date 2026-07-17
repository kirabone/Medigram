from django.shortcuts import render

def router(request):
    return render(request, 'testing/router.html')

def uploadPost(request):
    return render(request, 'testing/uploadPost.html')

def feed(request):
    return render(request, 'testing/feed.html')

def like(request):
    return render(request, 'testing/like.html')