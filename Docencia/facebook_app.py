import facebook

facebook_token = "EAAUmfSh3VGABAALokfOhzZBwOJDIMqLtgNntWpKm48IUEB8O7evoUECTZCtZBAicZB8SbutFTos2thK5OZASh3ZBaTeOmiNGLg5RGtuUlEFfoyKHps34VAnu4bAZCBxZBBoiIvVONhbqZANn9fRmSc3WAmmiAGZBtIepGG8bRK1ZBcuOv6Cftqa7ZBMw"
facebook_id = "108435717211122"
graph = facebook.GraphAPI(access_token=facebook_token, version="2.8")
graph.put_object(
    parent_object=facebook_id, 
    connection_name='feed',
    message="Visita nuestro Sitio Web",
    link="https://bartolo.org/noticias/"
)