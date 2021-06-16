import shutil, psutil
import signal
import pickle

from pyrogram import idle
from bot import app
from os import execl, kill, path, remove
from sys import executable
from datetime import datetime
import pytz
import time

from telegram import ParseMode, BotCommand
from telegram.ext import CommandHandler, run_async
from bot import dispatcher, updater, botStartTime, IMAGE_URL
from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper import button_build
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, shell, eval, anime, stickers, search, delete, speedtest, usage, mediainfo, count

now=datetime.now(pytz.timezone('Asia/Jakarta'))


@run_async
def stats(update, context):
    currentTime = get_readable_time(time.time() - botStartTime)
    current = now.strftime('%Y/%m/%d %I:%M:%S %p')
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>Bot's Alive Time:</b> {currentTime}\n' \
            f'<b>Start Time:</b> {current}\n' \
            f'<b>Total Dick Space:</b> {total}\n' \
            f'<b>Filled with trash space:</b> {used}  ' \
            f'<b>Wasted space:</b> {free}\n\n' \
            f'📊Data Usage📊\n<b>Upload:</b> {sent}\n' \
            f'<b>Download:</b> {recv}\n\n' \
            f'<b>Potato CPU Usage:</b> {cpuUsage}%\n' \
            f'<b>RAM:</b> {memory}%\n' \
            f'<b>DISK:</b> {disk}%'
    update.effective_message.reply_photo(IMAGE_URL, stats, parse_mode=ParseMode.HTML)


@run_async
def start(update, context):
    start_string = f'''
This bot can mirror all your pirated games, porns, Samsung Sam R34 to Google drive!
Type /{BotCommands.HelpCommand} to get a delicious menu of available commands
'''
    buttons = button_build.ButtonMaker()
    buttons.buildbutton("Where this bot was kanged from", "https://github.com/jhunrey7870/therealmirrorbot")
    buttons.buildbutton("Where to mirror your garbages", "https://t.me/joinchat/c91DOIRzhIJkOWU1")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(2))
    LOGGER.info('UID: {} - UN: {} - MSG: {}'.format(update.message.chat.id, update.message.chat.username, update.message.text))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        if update.message.chat.type == "private" :
            sendMessage(f"Hey I'm alive and no longer fapping while sleeping", context.bot, update)
        else :
            update.effective_message.reply_photo(IMAGE_URL, start_string, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    else :
        sendMessage(f"Oops! not an Authorized user.", context.bot, update)


@run_async
def restart(update, context):
    restart_message = sendMessage("Rebooting from FlameOS, wait plox you fatass!", context.bot, update)
    LOGGER.info(f'Restarting this bot...')
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")


@run_async
def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Penk", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


@run_async
def log(update, context):
    sendLogFile(context.bot, update)


@run_async
def bot_help(update, context):
    help_string_adm = f'''
/{BotCommands.HelpCommand}: To get this useless and hard to understand help list message 

/{BotCommands.MirrorCommand} [download_url][magnet_link]: Start mirroring your pornos and FlameOS bullshits to Google Drive.

/{BotCommands.UnzipMirrorCommand} [download_url][magnet_link]: Starts mirroring and if downloaded FlameOS file is any archive, extracts it to Google Drive

/{BotCommands.TarMirrorCommand} [download_url][magnet_link]: Start mirroring and upload the archived (.tar) version of the downloaded MarvelOS S9 Port or something else

/{BotCommands.CloneCommand}: Copy porno file/hentai folder to Google Drive

/{BotCommands.CountCommand}: Count how many bullshit file/folder of Google Drive Links

/{BotCommands.DeleteCommand} [link]: Delete any useless cunt file from Google Drive (Only Owner & Sudo)

/{BotCommands.WatchCommand} [youtube-dl supported link]: Mirror through youtube-dl. Click /{BotCommands.WatchCommand} for more useless and pointless help.

/{BotCommands.TarWatchCommand} [youtube-dl supported link]: Mirror through youtube-dl and tar before uploading

/{BotCommands.CancelMirror}: Reply to the gay message by which the FlameOS download was initiated and that cunt download will be cancelled

/{BotCommands.StatusCommand}: Shows a status of all the cunt downloads

/{BotCommands.ListCommand} [search term]: Searches the search term (for example FlameOS M31 Port) in the Google Drive, if found I will replies with the link

/{BotCommands.StatsCommand}: Show Stats of the free gayroku server with CC this cunt bot is hosted on

/{BotCommands.AuthorizeCommand}: Gib perms to a chat or a user for using the bot (Can only be invoked by Owner & Soupdo of the bot)

/{BotCommands.UnAuthorizeCommand}: Take perms away a chat or a user that can use the bot (Can only be invoked by Owner & Soupdo of the bot)

/{BotCommands.AuthorizedUsersCommand}: Show authorized powerful gays (Only Owner & Soupdo)

/{BotCommands.AddSudoCommand}: Add soupdo users (Only the gay Owner)

/{BotCommands.RmSudoCommand}: Nuke a soupdo user (Only the gay Owner)

/{BotCommands.LogCommand}: Get a pointless and confusing log file of this cunt bot. Handy for getting crash reports (unless you're too dumb to fucking understand or don't know how to read)

/{BotCommands.UsageCommand}: To see Gayroku free CC Dyno Stats (Owner & Soupdo only).

/{BotCommands.SpeedCommand}: Check Gayroku server's Speed of kang, if high then you can kang i mean mirror files faster

/shell: Run commands in Shell (Terminal).

/mediainfo: Get detailed info about replied porn or Sam R34.

/tshelp: Get help for cunt Torrent search module.

/weebhelp: Get help for Anime, Manga, and Character module. (useful to find KnY yaoi or Sam R34)

/stickerhelp: Get help for the cunt Stickers module.
'''

    help_string = f'''
/{BotCommands.HelpCommand}: To get this bullshit confusing message

/{BotCommands.MirrorCommand} [download_url][magnet_link]: Start mirroring the FlameOS money shortened link to Google Drive.

/{BotCommands.UnzipMirrorCommand} [download_url][magnet_link]: Starts kanging i mean mirroring and if downloaded file is any archive, extracts it to Google Drive

/{BotCommands.TarMirrorCommand} [download_url][magnet_link]: Start mirroring and reupload the archived (.tar) version of the download, just like kangerd in Exy7870

/{BotCommands.CloneCommand}: Copy JAV file/hentai folder to Google Drive

/{BotCommands.CountCommand}: Count porn file/yaoi folder of Google Drive Links

/{BotCommands.WatchCommand} [youtube-dl supported link]: Kang i mean mirror through youtube-dl. Click /{BotCommands.WatchCommand} for more help.

/{BotCommands.TarWatchCommand} [youtube-dl supported link]: Mirror through youtube-dl and tar before uploading your porn

/{BotCommands.CancelMirror}: Reply to the cunt message by which the porn download was initiated and that download will be cancelled

/{BotCommands.StatusCommand}: Shows a status of all the porno downloads

/{BotCommands.ListCommand} [search term]: Searches the search term in the Google Drive, if found replies with the cunt link

/{BotCommands.StatsCommand}: Show Stats of the Gayroku free CC host the bot is staying in

/{BotCommands.SpeedCommand}: Check Internet Speed of the Gayroku's server, if speeds are high then kanging will be easier

/mediainfo: Get detailed info about replied porn.

/tshelp: Get help for the cunt Torrent search module.

/weebhelp: Get help for Anime, Manga, and Character module. (Sam R34 or some yaoi bullshits)

/stickerhelp: Get help for the cunt Stickers module.
'''

    if CustomFilters.sudo_user(update) or CustomFilters.owner_filter(update):
        sendMessage(help_string_adm, context.bot, update)
    else:
        sendMessage(help_string, context.bot, update)


botcmds = [
BotCommand(f'{BotCommands.MirrorCommand}', 'Start Kanging i mean Mirroring'),
BotCommand(f'{BotCommands.TarMirrorCommand}','Upload tar (kanged i mean zipped) file'),
BotCommand(f'{BotCommands.UnzipMirrorCommand}','Extract your cunt files'),
BotCommand(f'{BotCommands.CloneCommand}','Copy porno file/folder to Drive'),
BotCommand(f'{BotCommands.CountCommand}','Count porno file/folder of Drive link'),
BotCommand(f'{BotCommands.WatchCommand}','Mirror cunt YT-DL support link'),
BotCommand(f'{BotCommands.TarWatchCommand}','Mirror sex Youtube playlist link as tar'),
BotCommand(f'{BotCommands.CancelMirror}','Cancel a kanging mission'),
BotCommand(f'{BotCommands.CancelAllCommand}','Cancel all kanging tasks'),
BotCommand(f'{BotCommands.DeleteCommand}','Delete file from Drive'),
BotCommand(f'{BotCommands.ListCommand}',' [query] Searches cunt files in Drive'),
BotCommand(f'{BotCommands.StatusCommand}','Get Kanging i mean Mirroring Status message'),
BotCommand(f'{BotCommands.StatsCommand}','This fatass Bot Usage Stats'),
BotCommand(f'{BotCommands.HelpCommand}','Get Detailed and unhelpful Help'),
BotCommand(f'{BotCommands.SpeedCommand}','Check Speed of the Gayroku host'),
BotCommand(f'{BotCommands.LogCommand}','Confusing AF Bot Log [owner/soupdo only]'),
BotCommand(f'{BotCommands.RestartCommand}','Restart this cunt fatass bot [owner/sudo only]')]


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("Rebooted from FlameOS Successfully!")
        LOGGER.info('Rebooted Successfully without YumiProtection spoofing the Flamey kang!')
        remove('restart.pickle')

    bot.set_my_commands(botcmds)

    start_handler = CommandHandler(BotCommands.StartCommand, start)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling()
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)

app.start()
main()
idle()
