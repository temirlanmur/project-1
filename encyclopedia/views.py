from django.shortcuts import render, redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_detail(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry_detail.html", {
            "title": title,
            "content": util.convert_to_html(entry)
        })
    
    return redirect('not_found')


def not_found(request):
    return render(request, 'encyclopedia/not_found.html')