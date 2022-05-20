from views import Index, About

# Здесь набор привязок: путь-контроллер
routes = {
    '/': Index(),

    # не забываем / в конце
    '/about/': About(),
}
