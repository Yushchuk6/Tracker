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


async def consumer_handler(websocket, path):
    async for message in websocket:
        message = json.loads(message)

        if message['type'] == 'target':
            message = controller.get_target()
        elif message['type'] == 'guess':
            message = controller.get_target_guess()
        
        await websocket.send(message)
        


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

    # asyncio.create_task(inf_wrap(websocket, controller.get_target, 0.2))
    # asyncio.create_task(inf_wrap(websocket, controller.get_target_guess, 1))

    # pending = asyncio.all_tasks()
    # await asyncio.gather(*pending)


async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task]
    )
    # for task in pending:
    #     task.cancel()

start_server = websockets.serve(handler, 'localhost', 8080)
loop.run_until_complete(start_server)
loop.run_forever()
