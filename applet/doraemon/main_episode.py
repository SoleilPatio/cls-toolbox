import re

if __name__ == '__main__':
    po = re.compile("(\d\d\d\d)\.(\d+).*?\s+(\S+)\s+(.*)",re.M|re.I)
    episode_file = r"doraemon_episode_list.txt"
    
    episode_count = 0
    ep_year_dict = dict()
    ep_month_dict = dict()
    with open(episode_file, "r") as in_file:
        for line in in_file:
            line = line.strip("\n\r ")
#             print line
            mo = po.match(line)
            
            if mo:
                episode_count += 1
                ep_year = mo.group(1)
                ep_month = int(mo.group(2))
                ep_cht = mo.group(3)
                ep_jpn = mo.group(4)
                
#                 for i in range(1, len( mo.groups())+1 ):
#                     print "\t", mo.group(i)
#                     pass
                yc = ep_year_dict.get(ep_year, 0)
                ep_year_dict[ep_year] = yc + 1
                
                mc = ep_month_dict.get(ep_month, 0)
                ep_month_dict[ep_month] = mc + 1
                

            else:
                print "[WARNNING] no match:", line
            
            
        
    print "[INFO] %d episode processed" % episode_count
    
    for year in sorted(ep_year_dict.keys()):
        print year ,":%2d"%ep_year_dict[year], "*"*ep_year_dict[year]
        
    for mo in sorted(ep_month_dict.keys()):
        print "%2d"%mo ,":%3d"%ep_month_dict[mo], "-"*ep_month_dict[mo]
    
    pass