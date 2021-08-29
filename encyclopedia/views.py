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


def edit_entry(request, title):
    if not util.get_entry(title):
        return redirect('not_found')

    if request.method == "POST":
        form = util.EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]             
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('entry_detail', title)         
    else:
        data = {'title': title,
                'content': util.get_entry(title)}
        form = util.EntryForm(initial=data)
        form.hide_title()
    
    return render(request, 'encyclopedia/edit_entry.html', {
        'title': title,
        'form': form
    })


def not_found(request):
    return render(request, 'encyclopedia/not_found.html')