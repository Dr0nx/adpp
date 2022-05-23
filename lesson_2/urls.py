from views import Index, About, Contacts

# Набор привязок: путь-контроллер
routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
}
