import asyncio
import json
import websockets
import pandas as pd

from controller.controller import SimulatorController
from model.simulator import Simulator, err_gen_norm
from model.filters.ewma import ewm
from model.filters.kalman import kalman


# async def inf_wrap(websocket, func, interval):
#     while True:
#         message = func()
#         await websocket.send(message)
#         await asyncio.sleep(interval)


async def consumer_handler(websocket, path):
    async for message in websocket:
        message = json.loads(message)
        _type = message['type']
        _data = message['data']

        if _type == 'target':
            message = controller.get_target_json(_data['time'])
        elif _type == 'guess':
            message = controller.get_target_guess_json(_data['time'])

        await websocket.send(message)


async def producer_handler(websocket, path):
    message = controller.get_path_json()
    await websocket.send(message)
    
    message = controller.get_trackers_json()
    await websocket.send(message)

    # asyncio.create_task(inf_wrap(websocket, controller.get_target, 0.2))
    # asyncio.create_task(inf_wrap(websocket, controller.get_target_guess, 1))

    # pending = asyncio.all_tasks()
    # await asyncio.gather(*pending)


async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))

    await asyncio.wait([consumer_task, producer_task])

if __name__ == '__main__':
    path_df = pd.read_csv('model\\data\\path.csv')
    trackers_df = pd.read_csv('model\\data\\trackers_medium.csv')

    model = Simulator(path_df, trackers_df, err_gen_norm, kalman, 5)
    controller = SimulatorController(model)

    loop = asyncio.get_event_loop()

    start_server = websockets.serve(handler, 'localhost', 8080)
    loop.run_until_complete(start_server)
    loop.run_forever()
