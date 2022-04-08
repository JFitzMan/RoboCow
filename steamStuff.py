
import steam
profileURL = 'https://steamcommunity.com/profiles/76561197998013968/'

def getID(URL):
    return steam.SteamID.from_url(URL).id

print(getID(profileURL))
