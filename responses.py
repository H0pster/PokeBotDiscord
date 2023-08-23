import random

import PokeRPS


async def handle_response(message, text) -> any:
    p_message = text.lower()

    if p_message == 'roll':
        return str(random.randint(1,6))

    if p_message[0:7] == 'pokerps':
        await PokeRPS.run_rps(message.channel, p_message)
        return

    return 'I don\'t understand'
