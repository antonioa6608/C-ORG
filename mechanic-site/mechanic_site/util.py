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
    gis = GoogleImagesSearch('AIzaSyBAOevRbZDIyCp11IPMfpwn59em_jPISiI', 'autobookr-422903')
    gis.search(search_params=_search_params)
    print(gis.results())
    return gis.results()[0].url

#103498754758089273863
#833ea130148644653