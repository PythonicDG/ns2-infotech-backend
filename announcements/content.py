"""Keep simple announcement formatting while excluding executable markup."""
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit


class AnnouncementHTML(HTMLParser):
    tags = {'p', 'br', 'strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li', 'h2', 'h3', 'h4', 'blockquote', 'a'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.tags:
            return
        attributes = ''
        if tag == 'a':
            href = dict(attrs).get('href', '')
            try:
                safe = urlsplit(href).scheme.lower() in {'', 'http', 'https', 'mailto', 'tel'}
            except ValueError:
                safe = False
            if href and safe:
                attributes = f' href="{escape(href, quote=True)}" rel="noopener noreferrer"'
        self.output.append(f'<{tag}{attributes}>')

    def handle_endtag(self, tag):
        if tag in self.tags and tag != 'br':
            self.output.append(f'</{tag}>')

    def handle_data(self, data):
        self.output.append(escape(data).replace('\n', '<br />'))


def safe_announcement_html(value):
    parser = AnnouncementHTML()
    parser.feed(value or '')
    parser.close()
    return ''.join(parser.output)
