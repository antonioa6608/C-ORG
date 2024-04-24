
from mechanic_site.util import get_car_image


def test_get_car_image():
    assert len(get_car_image("ford fiesta", ""))    > 0