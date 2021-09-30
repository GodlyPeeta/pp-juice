from bitwiseEnum.pyttanko import mods_from_str
import urllib3
import ossapi
import config
import pyttanko as pyt
import time
http = urllib3.PoolManager(num_pools=2)

BEATMAP_STATUS = {
    4: 'Loved',
    3: 'Qualified',
    2: 'Approved',
    1: 'Ranked',
    0: 'Pending',
    -1: 'WIP',
    -2: 'Graveyard'
}

OSU_API_N = []
for i in config.OSU_TOKEN:
    OSU_API_N.append(ossapi.Ossapi(i))

OSU_API_0 = OSU_API_N[0] # Compat with previous code

def is_a_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_beatmap_by_link(link):
    # It is a link
    tmp = link.partition("https://osu.ppy.sh/beatmapsets/")
    if not tmp[1]:
        return None # Invalid link!
    spl = tmp[2].partition('#')
    if not is_a_number(spl[0]):
        # Invalid link! :grimace
        return None
    if spl[1]:
        if not spl[2].startswith("osu/"):
            return None # Not osu!std map 
        return BeatmapEx(OSU_API_0.get_beatmaps(beatmap_id=int(spl[2].partition("/")[2]))[0])
    else:
        # It's a map ID and we have to get diff
        mapset = OSU_API_0.get_beatmaps(beatmapset_id=spl[0])
        return BeatmapEx(mapset[-1])

def get_beatmap_by_id(id):
    return BeatmapEx(OSU_API_0.get_beatmaps(beatmap_id=int(id)))

def get_letter_rank(n300, n100, n50, n0):
    portion = n300 / (n300 + n100 + n50 + n0)
    if n0:
        if portion == 1.0: return "S"
        elif portion > 0.9: return "A"
        elif portion > 0.8: return "B"
        elif portion > 0.6: return "C"
        else: return "D"
    else:
        if portion == 1.0: return "SS"
        elif portion > 0.9: return "S"
        elif portion > 0.8: return "A"
        elif portion > 0.7: return "B"
        else: return "D"

def get_emote_for_letterrank(rank):
    pass

def get_emotes_for_modstring(mods):
    pass

# Mods are always a string
# If you give non string mods you are stinky poopoo
class BeatmapEx:
    def __init__(self, u):
        self.underlying = u
        self.cached_sr = None
        f = http.request('GET', 'https://osu.ppy.sh/osu/' + u.id).data.decode('utf-8')
        p = pyt.parser()
        self.pyt_bm = p.map(f.splitlines()) # Abusing python's weak typing system

    def sr(self, mods):
        if self.cached_sr != None: return self.cached_sr
        sr = pyt.diff_calc().calc(self.pyt_bm, mods_from_str(mods))
        self.cached_sr = sr.total
        return sr.total
    
    def status_str(self):
        return BEATMAP_STATUS[self.status]
    
    def pp(self, accuracy, combo, mods, misses, c300 = -1, c100 = -1, c50 = -1):
        if c300 == -1:
            temp = pyt.acc_round(accuracy, self.pyt_bm.ncircles + self.pyt_bm.nsliders + self.pyt_bm.nspinners, misses)
            c300 = temp[0]
            c100 = temp[1]
            c50 = temp[2]
        sr = pyt.diff_calc().calc(self.pyt_bm, mods_from_str(mods))
        pp, aim_pp, speed_pp, acc_pp, _ = pyt.ppv2(sr.aim, sr.speed, bmap=self.pyt_bm, combo=combo, nmiss=misses, n50=c50, n100=c100, n300=c300, mods=pyt.mods_from_str(mods))
        return pp, aim_pp, speed_pp, acc_pp
    
    def stats(self, mods):
        stats = pyt.mods_apply(mods_from_str(mods), ar=self.pyt_bm.ar, od=self.pyt_bm.od, cs=self.pyt_bm.cs, hp=self.pyt_bm.hp)
        return { "ar": stats[1], "od": stats[2], "cs": stats[3], "hp": stats[4] }
    
    def make_embed(self):
        b = self.underlying
        title = f'{b.artist} - {b.title} [{b.version}] {round(self.sr(), 2)}\u2605'
        desc = ''
        desc += f"**Map Length:** {time.strftime('%M:%S', time.gmtime(int(b.total_length)))}"
        desc += f" **BPM:** {b.bpm}"
        desc += f" **Combo:** {b.max_combo}\n"
        desc += f"**CS:** {b.diff_size}"
        desc += f" **OD:** {b.diff_overall}"
        desc += f" **AR:** {b.diff_approach}"
        desc += f" **HP:** {b.diff_drain}\n"
        desc += f"[download](https://beatconnect.io/b/{b.beatmapset_id})\n"
        footer = ""
        if b.approved_date == None:
            footer = f"\u25b6 {b.playcount}  \u2764 {b.favourite_count} | Not approved | Mapped by {b.creator}"
        else:
            footer = f"\u25b6 {b.playcount}  \u2764 {b.favourite_count} | {self.status_str()} on {b.approved_date[:10]} | Mapped by {b.creator}"
        return title, desc, footer
    
    def make_embed_lite(self):
        b = self.underlying
        title = f'{b.artist} - {b.title}'
        desc = ''
        desc += f"**Map Length:** {time.strftime('%M:%S', time.gmtime(int(b.total_length)))}"
        desc += f" **BPM:** {b.bpm}"
        desc += f" **Mapped By:** {b.creator}"
        desc += f"[download](https://beatconnect.io/b/{b.beatmapset_id})"
        footer = f"\u25b6 {b.playcount}  \u2764 {b.favourite_count}"
        return title, desc, footer
