import asyncio

async def start_strongman(name, power, time_coeff = 2.0):
    number_balls = 5
    print(f' Силач {name} начал соревнования.')
    for i in range(1, number_balls+1):
        await asyncio.sleep(5 / power * time_coeff)
        print(f'Силач {name} поднял {i} шар')
    print(f'Силач {name} закончил соревнования.')


async def start_tournament():
    task1 = asyncio.create_task(start_strongman(name1, power1))
    task2 = asyncio.create_task(start_strongman(name2, power2))
    task3 = asyncio.create_task(start_strongman(name3, power3))
    await task1
    await task2
    await task3

name1= "Vasya"
name2 = "Georg"
name3 = "David"
power1 = 5
power2 = 4
power3 = 3

asyncio.run(start_tournament())