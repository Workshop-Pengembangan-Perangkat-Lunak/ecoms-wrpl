import random
from django import template

register = template.Library()

@register.simple_tag
def random_image():
    images = [
        "https://media.istockphoto.com/id/1473676063/photo/red-apples-on-the-market-stall.webp?b=1&s=170667a&w=0&k=20&c=25yQ_LAs2hj38E4-EOZ_FtBF3HERWQ-V-4ZNM0mayOI=",
        'https://plus.unsplash.com/premium_photo-1690291012110-e631a9d7c11d?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTd8fGxlbW9uJTIwc3F1ZWV6ZXxlbnwwfHwwfHx8MA%3D%3D',
        'https://media.istockphoto.com/id/1482149278/photo/fresh-avocado-on-white.webp?b=1&s=170667a&w=0&k=20&c=PMqxdJzrLwH-mJccYnTWhuo8He07H76Y5pwDt0nz9tc=',

        'https://image.uniqlo.com/UQ/ST3/id/imagesgoods/466732/item/idgoods_09_466732.jpg?width=494',
        'https://image.uniqlo.com/UQ/ST3/AsianCommon/imagesgoods/468563/item/goods_67_468563.jpg?width=494'
    ]
    return random.choice(images)