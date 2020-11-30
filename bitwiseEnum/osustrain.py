#!/usr/bin/python3.5
import sys
import pyttanko
import matplotlib.pyplot as plt
import matplotlib
import time
import io


def get_strains(bmap_file, mods:int=0):
    """Uses strain values from each hitobject 
    to create lists of strains in a way 
    I see fit"""
    bmap = get_pyttanko(bmap_file, mods)
    speed, aim, total, times = [], [], [], []
    seek = 0
    while seek <= bmap.hitobjects[-1].time:
        window = []
        for obj in bmap.hitobjects:
            if (obj.time >= seek and obj.time <= seek + 3000):
                window.append(obj.strains)
        wspeed, waim, wtotal = [], [], []
        for strain in window:
            wspeed.append(strain[0])
            waim.append(strain[1])
            wtotal.append(sum(strain))
        speed.append(sum(wspeed) / max(len(window), 1))
        aim.append(sum(waim) / max(len(window), 1))
        total.append(sum(wtotal) / max(len(window), 1))
        times.append(seek)
        seek += 500
    return speed, aim, total, times

def graph(bmap_file, title, mods:int=0):
    """Creates a graph of the strains over time"""
    speed, aim, total, times = get_strains(bmap_file, mods)
    times

    fig = plt.figure()
    fig.patch.set_facecolor("#36393f")
    l1, = plt.plot(times, speed, color = "#87cefa", label = "Speed")
    l2, = plt.plot(times, aim, color = "#7289da", label = "Aim")
    l3, = plt.plot(times, total, color = "#99aab5", label = "Overall")
    legend = plt.legend(handles=[l1, l2, l3])
    for text in legend.get_texts():
        text.set_color("#ffffff")
    frame = legend.get_frame()
    frame.set_facecolor('#36393f')
    frame.set_edgecolor('#36393f')
    plt.title(title)


    #plt.show()
    ax = plt.gca()
    
    formatter = matplotlib.ticker.FuncFormatter(lambda s, x: time.strftime('%M:%S', time.gmtime(s // 1000)))
    ax.xaxis.set_major_formatter(formatter)

    ax.set_facecolor("#36393f")
    ax.spines['bottom'].set_color('#ffffff')
    ax.spines['top'].set_color('#36393f') 
    ax.spines['right'].set_color('#36393f')
    ax.spines['left'].set_color('#36393f')
    ax.tick_params(axis='x', colors='#ffffff')
    ax.tick_params(axis='y', colors='#36393f')
    ax.yaxis.label.set_color('#36393f')
    ax.xaxis.label.set_color('#ffffff')
    ax.title.set_color('#ffffff')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=200)
    buf.seek(0)
    return buf

def get_pyttanko(bmap_file, mods:int):
    """Uses pyttanko to parse the map 
    each hitobject contains the strain values. 
    Thanks Francesco"""
    bmap = pyttanko.parser().map(open(bmap_file, encoding="utf8"))
    stars = pyttanko.diff_calc().calc(bmap, mods=mods)
    return bmap

if __name__ == '__main__':
    """Graphs the strains using matplotlib"""
    if len(sys.argv) < 2:
        sys.stderr.write("You need to provide a path to a .osu\n")
        sys.exit()
    mods = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    sys.stdout.write("Analyzing beatmap...\n")
    speed, aim, total, times = get_strains(sys.argv[1], mods)
    for i in range(len(speed)):
        sys.stdout.write('{:>8}: {:>8} |{:>8} |{:>8}\n'.format(times[i], 
                                                               round(speed[i], 2), 
                                                               round(aim[i], 2), 
                                                               round(total[i], 2)))

