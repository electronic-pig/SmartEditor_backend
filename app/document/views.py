from . import document


@document.route('/')
def index():
    return 'Hello!'
