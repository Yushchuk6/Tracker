import asyncio
import json
import websockets
import pandas as pd

from main import err_gen_norm, ewm, SimTragetController

loop = asyncio.get_event_loop()

path_df = pd.read_csv('path.csv')
trackers_df = pd.read_csv('trackers_medium.csv')

controller = SimTragetController(path_df, trackers_df, err_gen_norm, ewm)


async def inf_wrap(websocket, func, interval):
    while True:
        message = func()
        await websocket.send(message)
        await asyncio.sleep(interval)


async def producer_handler(websocket, path):
    message = controller.get_path_json()
    await websocket.send(message)

    message = controller.get_path_center_json()
    await websocket.send(message)

    # message = {
    #     'type': 'slider',
    #     'data': {
    #         'min': 0,
    #         'max': 69,
    #         'step': 0.1,
    #     }
    # }
    # await websocket.send(json.dumps(message))

    asyncio.create_task(inf_wrap(websocket, controller.get_target, 0.2))
    asyncio.create_task(inf_wrap(websocket, controller.get_target_guess, 1))

    pending = asyncio.all_tasks()
    await asyncio.gather(*pending)


start_server = websockets.serve(producer_handler, 'localhost', 8080)
loop.run_until_complete(start_server)
loop.run_forever()
