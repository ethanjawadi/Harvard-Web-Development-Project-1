from django.shortcuts import render, redirect
import markdown2
import random
from . import util

def markdown_to_html(markdown_content):
    return markdown2.markdown(markdown_content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {"message": "The requested page was not found."})
    else:
        html_content = markdown_to_html(content)
        return render(request, "encyclopedia/entry.html", {'title': title, 'content': html_content})

def search(request):
    query = request.GET.get('q', '').strip()
    entries = util.list_entries()
    if query in entries:
        return redirect('entry', title=query)
    else:
        matches = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, 'encyclopedia/search_results.html', {'matches': matches})

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {"message": "An entry with this title already exists."})
        util.save_entry(title, content)
        return redirect('entry', title=title)
    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect('entry', title=title)

    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {"message": "The requested page does not exist."})
    html_content = markdown_to_html(content)
    return render(request, "encyclopedia/edit_page.html", {'title': title, 'content': html_content})

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)
