luCommand("r1", "ls -l /", "xhopps", "fail", "Look for xhopps")
luCommand("r1", "ls -l /home/chopps", "chopps", "pass", "Look for chopps")
luCommand("r1", "ls -l /", "root", "pass", "Look for root")

luCommand("host1", "ls -l /", "xhopps", "fail", "Look for xhopps")
luCommand("host1", "ls -l /home/chopps", "chopps", "pass", "Look for chopps")
luCommand("host1", "ls -l /", "root", "pass", "Look for root")
