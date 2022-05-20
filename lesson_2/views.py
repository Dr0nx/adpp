from dr0n_framework.templator import render


class Index:
    def __call__(self):
        # Вызов a() эквивалентен вызову a.__call__().
        return '200 OK', render('index.html')


class About:
    def __call__(self):
        # Вызов a() эквивалентен вызову a.__call__().
        return '200 OK', render('about.html')
