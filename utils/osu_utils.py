from bitwiseEnum.pyttanko import mods_from_str
import urllib3
import ossapi
import config
import pyttanko as pyt
import time
http = urllib3.PoolManager(num_pools=2)

BEATMAP_STATUS = {
    '4': 'Loved',
    '3': 'Qualified',
    '2': 'Approved',
    '1': 'Ranked',
    '0': 'Pending',
    '-1': 'WIP',
    '-2': 'Graveyard'
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

# Python 3.9 polyfills :pensive:

def remove_pref(s, pre):
    if s.startswith(pre): return s[len(pre):]
    return s

def remove_suff(s, post):
    if s.endswith(post): return s[:-len(post)]
    return s

def get_beatmap_by_link(link):
    if link.endswith("/"): link = remove_suff(link, "/")
    if link.startswith("https://osu.ppy.sh/beatmapsets/"):
        t0 = remove_pref(link, "https://osu.ppy.sh/beatmapsets/")
        t1 = t0.partition('#')
        if not is_a_number(t1[0]):
            # Invalid link! :grimace
            return None
        if t1[1]:
            if not t1[2].startswith("osu/"):
                return None # Not osu!std map
            t2 = t1[2].partition("/")[2]
            return get_beatmap_by_id(t2)
        else:
            # It's a map ID and we have to get diff
            mapset = OSU_API_0.get_beatmaps({'s': t1[0]})
            return BeatmapEx(mapset[-1])
    elif link.startswith("https://osu.ppy.sh/b/"):
        t0 = remove_pref(link, "https://osu.ppy.sh/b/")
        if not is_a_number(t0):
            return None
        return get_beatmap_by_id(t0)

def get_beatmap_by_id(id):
    return BeatmapEx(OSU_API_0.get_beatmaps({'b': int(id)})[0])

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
        f = http.request('GET', 'https://osu.ppy.sh/osu/' + str(u['beatmap_id'])).data.decode('utf-8')
        p = pyt.parser()
        self.pyt_bm = p.map(f.splitlines()) # Abusing python's weak typing system

    def sr(self, mods = ""):
        if self.cached_sr != None: return self.cached_sr
        sr = pyt.diff_calc().calc(self.pyt_bm, mods_from_str(mods))
        self.cached_sr = sr.total
        return sr.total
    
    def status_str(self):
        return BEATMAP_STATUS[self.underlying["approved"]]
    
    def pp(self, accuracy, combo, mods, misses, c300 = -1, c100 = -1, c50 = -1):
        combo = int(combo)
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
        return { "ar": round(stats[1], 2), "od": round(stats[2], 2), "cs": round(stats[3], 2), "hp": round(stats[4], 2) }
