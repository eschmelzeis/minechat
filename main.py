from twitchio.ext import commands
import random
import json
import time

# User data storage
def load_user_data():
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_data(user_data):
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

user_data = load_user_data()

# Shop items
shop_items = {
    'Wooden Pickaxe': 10,
    'Stone Pickaxe': 20,
    'Iron Pickaxe': 30,
    'Diamond Pickaxe': 40,
    'Netherite Pickaxe': 50,
    'XPBooster': 100,
    'CoinBooster': 100
}

# Mining worlds
mining_worlds = {
    'Overworld': 1,
    'Nether': 20,
    'End': 35
}

# Ores
world_ores = {
    'Overworld': {
        'Wooden Pickaxe': {
            'Stone': 0.8,
            'Coal': 0.2
        },
        'Stone Pickaxe': {
            'Coal': 0.7,
            'Iron': 0.3
        },
        'Iron Pickaxe': {
            'Iron': 0.6,
            'Gold': 0.4
        },
        'Diamond Pickaxe': {
            'Gold': 0.5,
            'Diamond': 0.5
        },
        'Netherite Pickaxe': {
            'Diamond': 0.4,
            'Netherite': 0.6
        }
    },
    'Nether': {
        'Wooden Pickaxe': {
            'Netherrack': 0.8,
            'Quartz': 0.2
        },
        'Stone Pickaxe': {
            'Quartz': 0.7,
            'Glowstone': 0.3
        },
        'Iron Pickaxe': {
            'Glowstone': 0.6,
            'Magma': 0.4
        },
        'Diamond Pickaxe': {
            'Magma': 0.5,
            'Soul Sand': 0.5
        },
        'Netherite Pickaxe': {
            'Soul Sand': 0.4,
            'Netherite': 0.6
        }
    },
    'End': {
        'Wooden Pickaxe': {
            'End Stone': 0.8,
            'Purpur': 0.2
        },
        'Stone Pickaxe': {
            'Purpur': 0.7,
            'End Rod': 0.3
        },
        'Iron Pickaxe': {
            'End Rod': 0.6,
            'Dragon Egg': 0.4
        },
        'Diamond Pickaxe': {
            'Dragon Egg': 0.5,
            'Ender Pearl': 0.5
        },
        'Netherite Pickaxe': {
            'Ender Pearl': 0.4,
            'Elytra': 0.6
        }
    }
}

# Ore values
ore_values = {
    'Stone': 1,
    'Coal': 2,
    'Iron': 3,
    'Gold': 4,
    'Diamond': 5,
    'Netherite': 6,
    'Netherrack': 1,
    'Quartz': 2,
    'Glowstone': 3,
    'Magma': 4,
    'Soul Sand': 5,
    'End Stone': 1,
    'Purpur': 2,
    'End Rod': 3,
    'Dragon Egg': 4,
    'Ender Pearl': 5,
    'Elytra': 6
}

# XP values for each ore
ore_xp_values = {
    'Stone': 1,
    'Coal': 2,
    'Iron': 3,
    'Gold': 4,
    'Diamond': 5,
    'Netherite': 6,
    'Netherrack': 1,
    'Quartz': 2,
    'Glowstone': 3,
    'Magma': 4,
    'Soul Sand': 5,
    'End Stone': 1,
    'Purpur': 2,
    'End Rod': 3,
    'Dragon Egg': 4,
    'Ender Pearl': 5,
    'Elytra': 6
}

# Command descriptions for !help (using pastebin)
command_descriptions = {
    'mine': 'Mines ores based on your current pickaxe and world',
    'upgrade': 'Upgrades your pickaxe if you have enough coins',
    'shop': 'Displays the items available in the shop',
    'buy': 'Buys an item from the shop',
    'sell': 'Sells a specified quantity of an ore',
    'sellall': 'Sells all ores in your inventory',
    'inventory': 'Displays the contents of your inventory',
    'stats': 'Displays your stats, or the stats of another user',
    'world': 'Switches your mining world',
    'help': 'Displays this help message',
    'leaderboard': 'Displays the top 5 users with the most coins',
    'guess': 'Plays a guessing game where you guess a number between 1 and 10. If you guess correctly, you win a random amount of coins between 1 and 10',
    'trade': 'Trades a specified amount of your coins to another user',
    'worlds': 'Lists the available worlds and the levels at which they are unlocked',
    'prestige': 'Prestige when you reach level 50 to reset your level and increase your prestige',
    'about': 'Displays information about the bot and its creator'
}

# Store last command time for cooldowns
last_command_time = {}

# Set the cooldown time in seconds
cooldown_seconds = 30

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=config['token'], prefix=config['prefix'], initial_channels=config['initial_channels'])

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    @commands.command(name='mine')
    async def mine(self, ctx):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'mine' in last_command_time[user] and time.time() - last_command_time[user]['mine'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !mine command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['mine']):.0f} seconds.")
            return
        if user not in user_data:
            user_data[user] = {'ores': {'Stone': 0, 'Coal': 0, 'Iron': 0, 'Gold': 0, 'Diamond': 0, 'Netherite': 0, 'Netherrack': 0, 'Quartz': 0, 'Glowstone': 0, 'Magma': 0, 'Soul Sand': 0, 'End Stone': 0, 'Purpur': 0, 'End Rod': 0, 'Dragon Egg': 0, 'Ender Pearl': 0, 'Elytra': 0}, 'pickaxe': 'Wooden Pickaxe', 'coins': 0, 'xp': 0, 'level': 1, 'boosts': {}, 'world': 'Overworld', 'prestige': 0}
        pickaxe = user_data[user]['pickaxe']
        world = user_data[user]['world']
        ores = world_ores[world][pickaxe]
        mined_ore = random.choices(list(ores.keys()), weights=ores.values(), k=1)[0]
        user_data[user]['ores'][mined_ore] += 1
        xp_gain = ore_xp_values[mined_ore]
        if 'XPBooster' in user_data[user]['boosts'] and time.time() < user_data[user]['boosts']['XPBooster']:  # Check if the XP Booster is active
            xp_gain *= 2  # Double the XP gain
        user_data[user]['xp'] += xp_gain
        if user_data[user]['xp'] >= 10 * user_data[user]['level']:
            user_data[user]['xp'] = 0
            user_data[user]['level'] += 1
        # Check if the Coin Booster is active
        if 'CoinBooster' in user_data[user]['boosts'] and time.time() < user_data[user]['boosts']['CoinBooster']:
            user_data[user]['coins'] += ore_values[mined_ore] * 2  # Double the coin gain
        else:
            user_data[user]['coins'] += ore_values[mined_ore]
        save_user_data(user_data)
        # Check if any boosters have expired
        for booster in list(user_data[user]['boosts']):
            if time.time() > user_data[user]['boosts'][booster]:
                del user_data[user]['boosts'][booster]
        # If a booster is active, display the remaining time
        if 'XPBooster' in user_data[user]['boosts']:
            remaining_time = int((user_data[user]['boosts']['XPBooster'] - time.time()) / 60)  # Convert to minutes
            await ctx.send(f"@{ctx.author.name} mined 1 {mined_ore}! XP: {user_data[user]['xp']} Level: {user_data[user]['level']} XP Booster: {remaining_time} minutes remaining")
        elif 'CoinBooster' in user_data[user]['boosts']:
            remaining_time = int((user_data[user]['boosts']['CoinBooster'] - time.time()) / 60)  # Convert to minutes
            await ctx.send(f"@{ctx.author.name} mined 1 {mined_ore}! XP: {user_data[user]['xp']} Level: {user_data[user]['level']} Coin Booster: {remaining_time} minutes remaining")
        else:
            await ctx.send(f"@{ctx.author.name} mined 1 {mined_ore}! XP: {user_data[user]['xp']} Level: {user_data[user]['level']}")
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['mine'] = time.time()

    @commands.command(name='upgrade')
    async def upgrade(self, ctx):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'upgrade' in last_command_time[user] and time.time() - last_command_time[user]['upgrade'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !upgrade command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['upgrade']):.0f} seconds.")
            return
        if user not in user_data:
            user_data[user] = {'ores': {'Stone': 0, 'Coal': 0, 'Iron': 0, 'Gold': 0, 'Diamond': 0, 'Netherite': 0, 'Netherrack': 0, 'Quartz': 0, 'Glowstone': 0, 'Magma': 0, 'Soul Sand': 0, 'End Stone': 0, 'Purpur': 0, 'End Rod': 0, 'Dragon Egg': 0, 'Ender Pearl': 0, 'Elytra': 0}, 'pickaxe': 'Wooden Pickaxe', 'coins': 0, 'xp': 0, 'level': 1, 'boosts': {}, 'world': 'Overworld', 'prestige': 0}
        if user_data[user]['coins'] >= shop_items[user_data[user]['pickaxe']]:
            user_data[user]['coins'] -= shop_items[user_data[user]['pickaxe']]
            pickaxe_list = list(shop_items.keys())
            user_data[user]['pickaxe'] = pickaxe_list[pickaxe_list.index(user_data[user]['pickaxe'])+1]
            save_user_data(user_data)
            await ctx.send(f"@{ctx.author.name} upgraded their pickaxe! Pickaxe level: {user_data[user]['pickaxe']}")
        else:
            await ctx.send(f"@{ctx.author.name} doesn't have enough coins to upgrade!")
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['upgrade'] = time.time()

    @commands.command(name='shop')
    async def shop(self, ctx):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'shop' in last_command_time[user] and time.time() - last_command_time[user]['shop'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !shop command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['shop']):.0f} seconds.")
            return
        if user not in user_data:
            user_data[user] = {'ores': {'Stone': 0, 'Coal': 0, 'Iron': 0, 'Gold': 0, 'Diamond': 0, 'Netherite': 0, 'Netherrack': 0, 'Quartz': 0, 'Glowstone': 0, 'Magma': 0, 'Soul Sand': 0, 'End Stone': 0, 'Purpur': 0, 'End Rod': 0, 'Dragon Egg': 0, 'Ender Pearl': 0, 'Elytra': 0}, 'pickaxe': 'Wooden Pickaxe', 'coins': 0, 'xp': 0, 'level': 1, 'boosts': {}, 'world': 'Overworld', 'prestige': 0}
        shop_message = "Shop items: "
        for item, price in shop_items.items():
            shop_message += f"{item}: {price} coins, "
        await ctx.send(shop_message)
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['shop'] = time.time()

    @commands.command(name='buy')
    async def buy(self, ctx, *item):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'buy' in last_command_time[user] and time.time() - last_command_time[user]['buy'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !buy command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['buy']):.0f} seconds.")
            return
        item = ' '.join(item)  # Join all arguments into a single string
        if user not in user_data:
            user_data[user] = {'ores': {'Stone': 0, 'Coal': 0, 'Iron': 0, 'Gold': 0, 'Diamond': 0, 'Netherite': 0, 'Netherrack': 0, 'Quartz': 0, 'Glowstone': 0, 'Magma': 0, 'Soul Sand': 0, 'End Stone': 0, 'Purpur': 0, 'End Rod': 0, 'Dragon Egg': 0, 'Ender Pearl': 0, 'Elytra': 0}, 'pickaxe': 'Wooden Pickaxe', 'coins': 0, 'xp': 0, 'level': 1, 'boosts': {}, 'world': 'Overworld', 'prestige': 0}
        if item in shop_items and user_data[user]['coins'] >= shop_items[item]:
            if 'Booster' in item:
                if item in user_data[user]['boosts'] and user_data[user]['boosts'][item] > time.time():  # Check if the booster is already active
                    await ctx.send(f"@{ctx.author.name} already has an active {item}!")
                else:
                    user_data[user]['boosts'][item] = time.time() + 1800  # Set the expiration time to 30 minutes from now
                    await ctx.send(f"@{ctx.author.name} activated a {item}!")
            elif shop_items[item] > shop_items[user_data[user]['pickaxe']]:
                user_data[user]['coins'] -= shop_items[item]
                user_data[user]['pickaxe'] = item
                await ctx.send(f"@{ctx.author.name} bought a {item}!")
            else:
                await ctx.send(f"@{ctx.author.name} cannot downgrade their pickaxe!")
        else:
            await ctx.send(f"@{ctx.author.name} doesn't have enough coins to buy {item}!")
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['buy'] = time.time()

    @commands.command(name='sell')
    async def sell(self, ctx, ore, quantity: int = 1):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'sell' in last_command_time[user] and time.time() - last_command_time[user]['sell'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !sell command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['sell']):.0f} seconds.")
            return
        ore = ore.title()
        if user not in user_data:
            user_data[user] = {'ores': {'Stone': 0, 'Coal': 0, 'Iron': 0, 'Gold': 0, 'Diamond': 0, 'Netherite': 0, 'Netherrack': 0, 'Quartz': 0, 'Glowstone': 0, 'Magma': 0, 'Soul Sand': 0, 'End Stone': 0, 'Purpur': 0, 'End Rod': 0, 'Dragon Egg': 0, 'Ender Pearl': 0, 'Elytra': 0}, 'pickaxe': 'Wooden Pickaxe', 'coins': 0, 'xp': 0, 'level': 1, 'boosts': {}, 'world': 'Overworld', 'prestige': 0}
        if ore in user_data[user]['ores'] and user_data[user]['ores'][ore] >= quantity:
            user_data[user]['coins'] += ore_values[ore] * quantity
            user_data[user]['ores'][ore] -= quantity
            save_user_data(user_data)
            await ctx.send(f"@{ctx.author.name} sold {quantity} {ore} for {ore_values[ore] * quantity} coins!")
        else:
            await ctx.send(f"@{ctx.author.name} doesn't have enough {ore} to sell!")
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['sell'] = time.time()

    @commands.command(name='sellall')
    async def sellall(self, ctx):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'sellall' in last_command_time[user] and time.time() - last_command_time[user]['sellall'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !sellall command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['sellall']):.0f} seconds.")
            return
        if user not in user_data:
            user_data[user] = {'ores': {'Stone': 0, 'Coal': 0, 'Iron': 0, 'Gold': 0, 'Diamond': 0, 'Netherite': 0, 'Netherrack': 0, 'Quartz': 0, 'Glowstone': 0, 'Magma': 0, 'Soul Sand': 0, 'End Stone': 0, 'Purpur': 0, 'End Rod': 0, 'Dragon Egg': 0, 'Ender Pearl': 0, 'Elytra': 0}, 'pickaxe': 'Wooden Pickaxe', 'coins': 0, 'xp': 0, 'level': 1, 'boosts': {}, 'world': 'Overworld', 'prestige': 0}
        total_coins = 0
        for ore, quantity in user_data[user]['ores'].items():
            if quantity > 0:
                total_coins += ore_values[ore] * quantity
                user_data[user]['ores'][ore] = 0
        user_data[user]['coins'] += total_coins
        save_user_data(user_data)
        await ctx.send(f"@{ctx.author.name} sold all ores for {total_coins} coins!")
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['sellall'] = time.time()

    @commands.command(name='inventory')
    async def inventory(self, ctx):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'inventory' in last_command_time[user] and time.time() - last_command_time[user]['inventory'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !inventory command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['inventory']):.0f} seconds.")
            return
        if user not in user_data:
            user_data[user] = {'ores': {'Stone': 0, 'Coal': 0, 'Iron': 0, 'Gold': 0, 'Diamond': 0, 'Netherite': 0, 'Netherrack': 0, 'Quartz': 0, 'Glowstone': 0, 'Magma': 0, 'Soul Sand': 0, 'End Stone': 0, 'Purpur': 0, 'End Rod': 0, 'Dragon Egg': 0, 'Ender Pearl': 0, 'Elytra': 0}, 'pickaxe': 'Wooden Pickaxe', 'coins': 0, 'xp': 0, 'level': 1, 'boosts': {}, 'world': 'Overworld', 'prestige': 0}
        ores_str = ', '.join(f"{ore}: {quantity}" for ore, quantity in user_data[user]['ores'].items() if quantity > 0)
        inventory_message = f"{ctx.author.name}'s inventory: Ores: {ores_str} Pickaxe: {user_data[user]['pickaxe']} Coins: {user_data[user]['coins']} Prestige: {user_data[user]['prestige']}"
        await ctx.send(inventory_message)
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['inventory'] = time.time()

    @commands.command(name='stats')
    async def stats(self, ctx, other_user=None):
        if other_user is None:
            user = str(ctx.author.name)
        else:
            user = other_user.replace('@', '').lower()
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'stats' in last_command_time[user] and time.time() - last_command_time[user]['stats'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !stats command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['stats']):.0f} seconds.")
            return
        if user in user_data:
            ores_str = ', '.join(f"{ore}: {quantity}" for ore, quantity in user_data[user]['ores'].items() if quantity > 0)
            ores_str = ores_str if ores_str else 'None'  # If the user has no ores, set ores_str to 'None'
            stats_message = f"@{user}'s stats: Ores: {ores_str} Pickaxe level: {user_data[user]['pickaxe']} Coins: {user_data[user]['coins']} XP: {user_data[user]['xp']} Level: {user_data[user]['level']} Boosts: {', '.join(user_data[user]['boosts'])} World: {user_data[user]['world']}"
            await ctx.send(stats_message)
        else:
            await ctx.send(f"{user} doesn't exist!")
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['stats'] = time.time()

    @commands.command(name='world')
    async def switch(self, ctx, world):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'world' in last_command_time[user] and time.time() - last_command_time[user]['world'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !world command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['world']):.0f} seconds.")
            return
        if user not in user_data:
            user_data[user] = {'ores': {'Stone': 0, 'Coal': 0, 'Iron': 0, 'Gold': 0, 'Diamond': 0, 'Netherite': 0, 'Netherrack': 0, 'Quartz': 0, 'Glowstone': 0, 'Magma': 0, 'Soul Sand': 0, 'End Stone': 0, 'Purpur': 0, 'End Rod': 0, 'Dragon Egg': 0, 'Ender Pearl': 0, 'Elytra': 0}, 'pickaxe': 'Wooden Pickaxe', 'coins': 0, 'xp': 0, 'level': 1, 'boosts': [], 'world': 'Overworld'}
        if world in mining_worlds:
            if user_data[user]['level'] >= mining_worlds[world]:
                user_data[user]['world'] = world
                save_user_data(user_data)
                await ctx.send(f"@{ctx.author.name} switched to {world}!")
            else:
                await ctx.send(f"@{ctx.author.name} is not at a high enough level to switch to {world}!")
        else:
            await ctx.send(f"@{ctx.author.name} tried to switch to an unknown world!")
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['world'] = time.time()

    @commands.command(name='help')
    async def help(self, ctx):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'help' in last_command_time[user] and time.time() - last_command_time[user]['help'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !help command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['help']):.0f} seconds.")
            return
        help_message = "View a list of commands and more info at this link: https://pastebin.com/raw/wJVTxDKm"
        await ctx.send(help_message)
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['help'] = time.time()

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'leaderboard' in last_command_time[user] and time.time() - last_command_time[user]['leaderboard'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !leaderboard command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['leaderboard']):.0f} seconds.")
            return
        leaderboard = sorted(user_data.items(), key=lambda x: x[1]['coins'], reverse=True)[:5]
        leaderboard_message = "Leaderboard: " + "\n".join(f"{i+1}. @{user[0]}: {user[1]['coins']} coins " for i, user in enumerate(leaderboard))
        await ctx.send(leaderboard_message)
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['leaderboard'] = time.time()

    @commands.command(name='guess')
    async def guess(self, ctx, user_guess: int):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'guess' in last_command_time[user] and time.time() - last_command_time[user]['guess'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !guess command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['guess']):.0f} seconds.")
            return
        correct_number = random.randint(1, 10)
        if user_guess == correct_number:
            coins_won = random.randint(1, 10)
            user_data[user]['coins'] += coins_won
            save_user_data(user_data)
            await ctx.send(f"Congratulations @{ctx.author.name}, you guessed the correct number! You won {coins_won} coins.")
        else:
            await ctx.send(f"Sorry @{ctx.author.name}, that's not correct. The correct number was {correct_number}.")
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['guess'] = time.time()

    @commands.command(name='trade')
    async def trade(self, ctx, recipient_name: str, amount: int):
        sender = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if sender in last_command_time and 'trade' in last_command_time[sender] and time.time() - last_command_time[sender]['trade'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !trade command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[sender]['trade']):.0f} seconds.")
            return
        recipient = recipient_name.replace('@', '').lower()
        if sender not in user_data or recipient not in user_data:
            await ctx.send("Either the sender or recipient does not exist.")
            return
        if user_data[sender]['coins'] < amount:
            await ctx.send(f"@{sender} does not have enough coins to trade.")
            return
        user_data[sender]['coins'] -= amount
        user_data[recipient]['coins'] += amount
        save_user_data(user_data)
        await ctx.send(f"@{sender} has successfully traded {amount} coins to {recipient_name}")
        # Update the last command time for the user
        if sender not in last_command_time:
            last_command_time[sender] = {}
        last_command_time[sender]['trade'] = time.time()

    @commands.command(name='worlds')
    async def worlds(self, ctx):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'worlds' in last_command_time[user] and time.time() - last_command_time[user]['worlds'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !worlds command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['worlds']):.0f} seconds.")
            return
        worlds_message = "Available worlds: " + ", ".join(f"{world}: Level {level}" for world, level in mining_worlds.items())
        await ctx.send(worlds_message)
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['worlds'] = time.time()

    @commands.command(name='prestige')
    async def prestige(self, ctx):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'prestige' in last_command_time[user] and time.time() - last_command_time[user]['prestige'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !prestige command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['prestige']):.0f} seconds.")
            return
        if user not in user_data:
            user_data[user] = {'ores': {'Stone': 0, 'Coal': 0, 'Iron': 0, 'Gold': 0, 'Diamond': 0, 'Netherite': 0, 'Netherrack': 0, 'Quartz': 0, 'Glowstone': 0, 'Magma': 0, 'Soul Sand': 0, 'End Stone': 0, 'Purpur': 0, 'End Rod': 0, 'Dragon Egg': 0, 'Ender Pearl': 0, 'Elytra': 0}, 'pickaxe': 'Wooden Pickaxe', 'coins': 0, 'xp': 0, 'level': 1, 'boosts': {}, 'world': 'Overworld', 'prestige': 0}
        if user_data[user]['level'] >= 50:
            user_data[user]['level'] = 1
            user_data[user]['prestige'] += 1
            save_user_data(user_data)
            await ctx.send(f"@{ctx.author.name} has prestiged! Current prestige level: {user_data[user]['prestige']}")
        else:
            await ctx.send(f"@{ctx.author.name} needs to reach level 50 to prestige. Current level: {user_data[user]['level']}")
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['prestige'] = time.time()
    
    @commands.command(name='about')
    async def about(self, ctx):
        user = str(ctx.author.name)
        # Check if the user is in the dictionary and if enough time has passed
        if user in last_command_time and 'about' in last_command_time[user] and time.time() - last_command_time[user]['about'] < cooldown_seconds:
            await ctx.send(f"@{ctx.author.name}, the !about command is on cooldown. Try again in {cooldown_seconds - (time.time() - last_command_time[user]['about']):.0f} seconds.")
            return
        about_message = "This bot was created by twitch.tv/1ayover . It's a mining game where you can mine ores, sell them for coins, upgrade your pickaxe, and more!"
        await ctx.send(about_message)
        # Update the last command time for the user
        if user not in last_command_time:
            last_command_time[user] = {}
        last_command_time[user]['about'] = time.time()

bot = Bot()
bot.run()