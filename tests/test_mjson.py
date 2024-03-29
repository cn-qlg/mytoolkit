import unittest

from mytoolkit.mjson import MJson

json_str = """
{
    "products":[
        {
            "id":1,
            "title":"iPhone 9",
            "description":"An apple mobile which is nothing like apple",
            "price":549,
            "discountPercentage":12.96,
            "rating":4.69,
            "stock":94,
            "brand":"Apple",
            "category":"smartphones",
            "thumbnail":"https://dummyjson.com/image/i/products/1/thumbnail.jpg",
            "images":[
                "https://dummyjson.com/image/i/products/1/1.jpg",
                "https://dummyjson.com/image/i/products/1/2.jpg",
                "https://dummyjson.com/image/i/products/1/3.jpg",
                "https://dummyjson.com/image/i/products/1/4.jpg",
                "https://dummyjson.com/image/i/products/1/thumbnail.jpg"
            ]
        },
        {
            "id":2,
            "title":"iPhone X",
            "description":"SIM-Free, Model A19211 6.5-inch Super Retina HD display with OLED technology ...",
            "price":899,
            "discountPercentage":17.94,
            "rating":4.44,
            "stock":34,
            "brand":"Apple",
            "category":"smartphones",
            "thumbnail":"https://dummyjson.com/image/i/products/2/thumbnail.jpg",
            "images":[
                "https://dummyjson.com/image/i/products/2/1.jpg",
                "https://dummyjson.com/image/i/products/2/2.jpg",
                "https://dummyjson.com/image/i/products/2/3.jpg",
                "https://dummyjson.com/image/i/products/2/thumbnail.jpg"
            ]
        },
        {
            "id":3,
            "title":"Samsung Universe 9",
            "description":"Samsung's new variant which goes beyond Galaxy to the Universe",
            "price":1249,
            "discountPercentage":15.46,
            "rating":4.09,
            "stock":36,
            "brand":"Samsung",
            "category":"smartphones",
            "thumbnail":"https://dummyjson.com/image/i/products/3/thumbnail.jpg",
            "images":[
                "https://dummyjson.com/image/i/products/3/1.jpg"
            ]
        },
        {
            "id":4,
            "title":"OPPOF19",
            "description":"OPPO F19 is officially announced on April 2021.",
            "price":280,
            "discountPercentage":17.91,
            "rating":4.3,
            "stock":123,
            "brand":"OPPO",
            "category":"smartphones",
            "thumbnail":"https://dummyjson.com/image/i/products/4/thumbnail.jpg",
            "images":[
                "https://dummyjson.com/image/i/products/4/1.jpg",
                "https://dummyjson.com/image/i/products/4/2.jpg",
                "https://dummyjson.com/image/i/products/4/3.jpg",
                "https://dummyjson.com/image/i/products/4/4.jpg",
                "https://dummyjson.com/image/i/products/4/thumbnail.jpg"
            ]
        },
        {
            "id":5,
            "title":"Huawei P30",
            "description":"Huawei’s re-badged P30 Pro New Edition was officially unveiled yesterday in Germany ...",
            "price":499,
            "discountPercentage":10.58,
            "rating":4.09,
            "stock":32,
            "brand":"Huawei",
            "category":"smartphones",
            "thumbnail":"https://dummyjson.com/image/i/products/5/thumbnail.jpg",
            "images":[
                "https://dummyjson.com/image/i/products/5/1.jpg",
                "https://dummyjson.com/image/i/products/5/2.jpg",
                "https://dummyjson.com/image/i/products/5/3.jpg"
            ]
        }
    ],
    "total":100,
    "skip":0,
    "limit":5
}
"""


class TestMjson(unittest.TestCase):
    def test_loads(self):
        value = MJson.loads(json_str)
        self.assertIsInstance(value, MJson)

    def test_common_function_of_dict(self):
        value = MJson.loads(json_str)

        # get value by key directly
        self.assertEqual(value["total"], 100)

        # length
        self.assertEqual(len(value["products"]), 5)

        # if key not existed, will raise KeyError
        with self.assertRaises(KeyError):
            value["not_existed_key"]

        # test get function
        self.assertIsNone(value.get("not_existed_key"))
        self.assertEqual(value.get("not_existed_key", "defalut_value"), "defalut_value")

        # iteration, only check keys because values are quite long
        keys = ["products", "total", "skip", "limit"]
        for k, _ in value.items():
            self.assertTrue(k in keys)
        self.assertEqual(len(keys), len(value.items()))

        # interation sub items
        for index, product in enumerate(value["products"]):
            self.assertEqual(index+1, product["id"])

    def test_long_index_key(self):
        value = MJson.loads(json_str)
        self.assertEqual(value[["products", 0, "id"]], 1)
        self.assertEqual(value[["products", 1, "title"]], "iPhone X")

        self.assertEqual(value.get(["products", 6, "title"], "iPhone XXX"), "iPhone XXX")

        for _, image in enumerate(value["products", 0, "images"]):
            self.assertTrue(image.startswith("https://dummyjson.com/image/i/products/1/"))

    def test_find_by_key(self):
        value = MJson.loads(json_str)
        self.assertEqual(value.find_by_key("id"), [1, 2, 3, 4, 5])

    def test_find_one_by_key(self):
        value = MJson.loads(json_str)
        self.assertEqual(value.find_one_by_key("id"), 1)

    def test_get_value(self):
        value = MJson.loads(json_str)
        self.assertTrue(isinstance(value["products", 0, "images"], MJson))
        self.assertTrue(isinstance(value.get_value(["products", 0, "images"]), list))


if __name__ == '__main__':
    unittest.main()
