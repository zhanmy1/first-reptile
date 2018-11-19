# -*- coding: UTF-8 -*-

import random

data_root_path = 'D:/sublime/avro/'

rep = 'apache/avro'

tokens = [
    "token a70854771f861dc5d7f9ebe817b33f75637b901d",
    "token 24ce6aec37b0ceb39424fdb24dc77f840582a93d",
    "token fa3b7cb248d9f94fbf9561175945ecb31f62a37f",
    "token d8ced087bcd5a39d97c833a802e2d28a0212c03b",
    "token f67e79c8fcd20aaa0898ea53c02ade3100b890b2",
    "token 310ff8f54b153954b2136a288229b9ddf0d6b91b",
    "token 925ed31b7e3998def743eb60184e0e040c296240",
    "token 5c173f6502708e2754970036f516cc18a7894f31",
    "token 9d051ef2ac8f96cde73922f637747bc881243b7c",
]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'Authorization': random.choice(tokens),
           'Content-Type': 'application/json',
           'Accept': 'application/json'
           }