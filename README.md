# 🎮 MineChat for Twitch Chat 🎮

Welcome to the ultimate mining game on Twitch! Mine ores, sell them for coins, upgrade your pickaxe, and more! All within your favorite streaming platform.

## 🛠️ Commands 🛠️

- `!about`: 📜 Shows information about the bot.
- `!mine`: ⛏️ Mines ores.
- `!sell {Ore} {Amount}`: 💰 Sells your ores for coins.
- `!sellall`: 💰 Sells all your ores for coins.
- `!shop`: 🏪 Shows the available items in the shop.
- `!buy`: 💸 Buys an item from the shop.
- `!upgrade`: ⚒️ Upgrades your pickaxe if you have enough coins.
- `!inventory`: 🎒 Displays the contents of your inventory.
- `!stats {@user}`: 📊 Displays your stats, or the stats of another user.
- `!world`: 🌍 Switches your mining world.
- `!help`: ❓ Displays a help message with a list of commands.
- `!leaderboard`: 🏆 Displays the top 5 users with the most coins.
- `!guess`: 🎲 Plays a guessing game where you guess a number between 1 and 10. If you guess correctly, you win a random amount of coins between 1 and 10.
- `!trade {@user}`: 💼 Trades a specified amount of your coins to another user.
- `!worlds`: 🌐 Lists the available worlds and the levels at which they are unlocked.
- `!prestige`: 🏅 Prestige when you reach level 50 to reset your level and increase your prestige.

## 🏪 Shop Items 🏪

- Wooden Pickaxe: 10 coins
- Stone Pickaxe: 20 coins
- Iron Pickaxe: 30 coins
- Diamond Pickaxe: 40 coins
- Netherite Pickaxe: 50 coins
- XP Booster: 100 coins
- Coin Booster: 100 coins

## ⛏️ Mining Worlds ⛏️

- Overworld: Level 1+
- Nether: Level 20+
- End: Level 35+

## ⛏️ Ores ⛏️

- Overworld: 
   - Wooden Pickaxe: Stone (80%), Coal (20%)
   - Stone Pickaxe: Coal (70%), Iron (30%)
   - Iron Pickaxe: Iron (60%), Gold (40%)
   - Diamond Pickaxe: Gold (50%), Diamond (50%)
   - Netherite Pickaxe: Diamond (40%), Netherite (60%)
- Nether: 
   - Wooden Pickaxe: Netherrack (80%), Quartz (20%)
   - Stone Pickaxe: Quartz (70%), Glowstone (30%)
   - Iron Pickaxe: Glowstone (60%), Magma (40%)
   - Diamond Pickaxe: Magma (50%), Soul Sand (50%)
   - Netherite Pickaxe: Soul Sand (40%), Netherite (60%)
- End: 
   - Wooden Pickaxe: End Stone (80%), Purpur (20%)
   - Stone Pickaxe: Purpur (70%), End Rod (30%)
   - Iron Pickaxe: End Rod (60%), Dragon Egg (40%)
   - Diamond Pickaxe: Dragon Egg (50%), Ender Pearl (50%)
   - Netherite Pickaxe: Ender Pearl (40%), Elytra (60%)

## 🔧 Installation Instructions 🔧

- Clone the repository to your local machine.
- Navigate to the project directory.
- Install the required Python module by running `pip install twitchio` in your terminal.
- Open the `config.json` file.
- Set your values in the `config.json` file. 
   - `token`: Your oauth token. You can get this by visiting https://twitchapps.com/tmi/ and connecting your Twitch account.
   - `prefix`: The prefix for the bot commands. Default is `!`.
   - `initial_channels`: The Twitch channels where the bot will be active. This should be a list of channel names.
- Save the `config.json` file.
- Run `main.py` to start the bot.

## 👤 Author 👤

This bot was created by 1ayover on Twitch. Enjoy the game!
