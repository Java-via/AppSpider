# _*_ coding: utf-8 _*_

import sys
from demos_apps.app_z_360 import main_360
from demos_apps.app_z_baidu import main_baidu
from demos_apps.app_z_wdj import main_wdj
from demos_apps.app_z_yyb import main_yyb
from demos_apps.app_z_aso100 import main_aso
from demos_apps.app_z_z import add_exclude

if sys.argv[1] == "360":
    main_360()
elif sys.argv[1] == "baidu":
    main_baidu()
elif sys.argv[1] == "wdj":
    main_wdj()
elif sys.argv[1] == "yyb":
    main_yyb()
elif sys.argv[1] == "aso":
    main_aso()
elif sys.argv[1] == "exclude":
    add_exclude()

exit()
