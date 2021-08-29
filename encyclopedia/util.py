import re
from . import markdown2

from django import forms
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


class EntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(widget=forms.Textarea, label="Content")

    def hide_title(self):
        self.fields['title'].widget.attrs['readonly'] = True


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


# Some custom functions

def convert_to_html(md_content):
    """
    Converts the markdown-formatted text to html using markdown2 module.
    """
    return markdown2.markdown(md_content)


def entry_exists(title):
    """
    Checks the existence of encyclopedia entry, given the title.
    """
    if default_storage.exists(f"entries/{title}.md"):
        return True
    return False