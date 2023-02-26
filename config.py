import configparser

config = configparser.ConfigParser()
config.read('config.ini')

caliber = config.getfloat("10m_target", "caliber")
ex_target_diam = config.getint("10m_target","ex_target_diam")
ten_diam = config.getint("10m_target","ten_diam")
ten_x_diam = config.getint("10m_target","ten_x_diam")
cam_n = config.getint("10m_target","cam")
min = config.getint("10m_target","min")
max = config.getint("10m_target","max")
blur = config.getint("10m_target","blur")
tenth = round((ex_target_diam / 2 - ten_diam / 2) / 89, 2)   #mm per 0.1

ring_diam = tenth * 10
