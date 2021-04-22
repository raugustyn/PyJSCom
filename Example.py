#  -*- coding: utf-8 -*-
__author__ = "kubik.augustyn@post.cz"
"""
This example shows how python HTTP server receives data and fires callback function in a JavaScript client.
"""

from COM.COM import Communication
import time

data = [
    {
        "type": "header",
        "text": "Hello.",
        "tag": "h1"
    },
    {
        "type": "progressBar",
        "progress": 0,
        "width": 1000,
    },
    {
        "type": "text",
        "text": "Hello..."
    },
    {
        "type": "table",
        "fullWidth": "true",
        "HTML": [
            [
                {
                    "type": "text",
                    "text": "Hello..."
                },
                {
                    "type": "progressBar",
                    "progress": 0,
                    "width": 100,
                },
                {
                    "type": "header",
                    "text": "Hello.",
                    "tag": "h1"
                }
            ],
            [
                {
                    "type": "text",
                    "text": "How are you?"
                },
                {
                    "type": "text",
                    "text": "How are you?"
                },
                {
                    "type": "text",
                    "text": "How are you?"
                },
            ]
        ]
    },
    {
        "type": "sendData",
        "data": "CreateConsole",
        "buttonText": "Recreate console"
    },
    {
        "type": "sendDataWithInput",
        "buttonText": "Readed 1",
        "placeholder": "What readed",
        "firstPart":"<yournamehere>Is",
        "size": 10,
        "id": "data0"
    }
]

def onReceive(text):
    print(text)

    
if __name__ == '__main__':
    com = Communication(data=data, port=12345)
    com.onReceive = onReceive
    com.run()
    while True:
        time.sleep(1)
        if data[3]["HTML"][0][1]["progress"] == 100:
            break
        data[3]["HTML"][0][1]["progress"] = data[3]["HTML"][0][1]["progress"] + 10
        com.data = data
        com.reloadConsole()
    print("Ended.")
    data[0]["text"] = "Finished"
    com.data = data
com.reloadConsole()
