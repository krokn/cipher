import random


async def generate_new_levels():
    NUMBER_LEVELS = 100
    new_levels = []
    for _ in range(NUMBER_LEVELS // 10):
        levels = []
        for _ in range(3):
            levels.append({
                "code_length": random.randint(5, 6),
                "attempts": random.randint(5, 10),
                "degree_hint": random.randint(1, 2)
            })
        for _ in range(4):
            levels.append({
                "code_length": random.randint(4, 5),
                "attempts": random.randint(8, 12),
                "degree_hint": random.randint(1, 2)
            })
        for _ in range(3):
            levels.append({
                "code_length": random.randint(3, 4),
                "attempts": random.randint(10, 15),
                "degree_hint": random.randint(1, 2)
            })

        random.shuffle(levels)
        new_levels.extend(levels)

    return new_levels





