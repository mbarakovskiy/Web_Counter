#!/usr/bin/env python3

from aiohttp import web
from PIL import Image, ImageDraw
import glob
import os
import io


PATH = '../server'


class App:
    def __init__(self):
        self.dict = {'my_server': 1}

    def increment(self, current_id):
        self.dict[current_id] += 1

    async def get_stats(self, request):
        try:
            current_id = request.query['site']
            count = self.check_stats(current_id)
            text = str(count)
            response = web.Response()
            response.content_type = 'Image/png'
            byte_img = create_response_with_image(text, (20, 20))
            response.body = get_bytes_from_image(byte_img)
            return response
        except Exception:
            response_obj = f'status: failed\nreason: no site \nname mentioned'
            response = web.Response()
            response.content_type = 'Image/png'
            response.body = get_bytes_from_image(create_response_with_image(response_obj, (100, 100)))
            return response

    def check_stats(self, current_id):
        if not self.dict.__contains__(current_id):
            return 0
        return self.dict.get(current_id)

    async def get_image(self, request):
        try:
            current_id = request.query['id']
            if self.dict.__contains__(current_id):
                self.increment(current_id)
            else:
                self.dict[current_id] = 1
            response = web.Response()
            response.content_type = 'Image/png'
            byte_img = Image.open('Images/img.png')
            response.body = get_bytes_from_image(byte_img)
            return response
        except Exception:
            response_obj = f'status: failed\nreason: no picture \nid mentioned'
            response = web.Response()
            response.content_type = 'Image/png'
            response.body = get_bytes_from_image(create_response_with_image(response_obj, (100, 100)))
            return response

    def get_app(self):
        new_app = web.Application()
        new_app.router.add_static('/Images', path=PATH, name='Images', show_index=True)
        new_app.router.add_get('/api/stat', self.get_stats)
        new_app.router.add_get('/api/picture', self.get_image)
        return new_app


def create_response_with_image(text, size):
    img = Image.new('RGB', size, (255, 0, 0))
    drawer = ImageDraw.Draw(img)
    drawer.text((5, 5), text=text, fill=(255, 255, 0))
    return img


def get_bytes_from_image(img):
    byte_io = io.BytesIO()
    img.save(byte_io, format='PNG')
    return bytes(byte_io.getvalue())


app = App().get_app()


if __name__ == '__main__':
    web.run_app(app, port=3030)
