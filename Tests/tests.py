from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from server.main import App, get_bytes_from_image, create_response_with_image


class TestApp(AioHTTPTestCase):
    async def get_application(self):
        return App().get_app()

    def test_init_app(self):
        app = App()
        self.assertIsInstance(app, App)
        self.assertIsInstance(app.dict, dict)

    @unittest_run_loop
    async def test_get_image(self):
        resp = await self.client.request('GET', '/api/picture?id=1')
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.content_type, 'Image/png')

    @unittest_run_loop
    async def test_get_image_with_stats(self):
        resp = await self.client.request('GET', '/api/stat?site=111')
        app = App().get_app()
        data = '0'
        byte_img = get_bytes_from_image(create_response_with_image(data, (20, 20)))
        resp_byte_img = await resp.read()
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.content_type, 'Image/png')
        self.assertEqual(resp_byte_img, byte_img)

    @unittest_run_loop
    async def test_get_incorrect_stats(self):
        resp = await self.client.request('GET', '/api/stat')
        resp_exc = await resp.read()
        exc_message = f'status: failed\nreason: no site \nname mentioned'
        img_exc = get_bytes_from_image(create_response_with_image(exc_message, (100, 100)))
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.content_type, 'Image/png')
        self.assertEqual(resp_exc, img_exc)

    @unittest_run_loop
    async def test_get_incorrect_query(self):
        resp = await self.client.request('GET', '/api/stast?id=11')
        self.assertEqual(resp.status, 404)