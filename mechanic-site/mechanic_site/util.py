from google_images_search import GoogleImagesSearch

def get_car_image(make, model_number):
    _search_params = {
    'q': "ford fiesta",
    'num': 10,
    'fileType': 'png',
    'safe': 'safeUndefined', ##
    'imgType': 'photo', ##
    'imgSize': 'medium', ##
    'imgDominantColor': 'imgDominantColorUndefined', ##
    'imgColorType': 'imgColorTypeUndefined' ##
}
    gis = GoogleImagesSearch('AIzaSyBl_wAq3K--DmwySXuAzyIWnexYzuT26hg', '833ea130148644653')
    gis.search(search_params=_search_params)
    print(gis.results())
    return gis.results()[0].url