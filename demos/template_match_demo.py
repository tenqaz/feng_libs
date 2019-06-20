# -*- coding: utf-8 -*-

__author__ = 'Jim'

from feng_libs.image_libs.template_match import TemplateMatch

base_path = "F:\\tmp\\dnf_image_test"
TemplateMatch.find_template_pos_debug(f"{base_path}\\map.png", f"{base_path}\\monster_white_2.png", score=0.47)
# TemplateMatch.find_template_pos_test_method(f"{base_path}\\map.png", f"{base_path}\\TEST.PNG")
