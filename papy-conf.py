# -*- coding: utf-8 -*-

FILENAME = "myPreset.xml"

SCHEMA = '<?xml version="1.0" encoding="utf-8"?>\n'
YAW_ANGLE = 360

ROWS = [1, 8, 15, 15, 15]
PITCH = [90, 70, 35, 0, -40]
PRESET_NAME = r"My D3100 preset"
TOOLTIP = '''18 мм на APS-C (x1.6)
			Нодальная точка - 23мм(1 мм перед кольцом) от поверхности объектива (22мм при 25мм)
			Всего кадров: {0}:
				{1}
			После съемки желательно снять надир (пол)'''
PICT_TAG = '<pict yaw="{0}" pitch="{1}" />'
DOC_TEMPLATE = '''{_schema}
<papywizard>
	<preset name="{_preset_name}">
		<tooltip>
			{_tooltip}
		</tooltip>
		<shoot>
			{_shoots}
		</shoot>
	</preset>
</papywizard>
'''

shoots = []
shoots_count = 0
shoots_info = []
num_rows = len(ROWS)

for i in xrange(num_rows):
    yaw_delta = YAW_ANGLE / ROWS[i]
    num_shoots = YAW_ANGLE / yaw_delta
    shoots_count += num_shoots
    yaw_delta = yaw_delta % 360 # angle must be less than 360 degrees

    shoot_range = xrange(num_shoots)
    if i % 2 == 0: shoot_range = reversed(shoot_range)
    shoots.append('%s<!-- ROW %d -->' % ( ('' if i == 0 else '\n\t\t\t'), (i + 1) ))

    for shoot in shoot_range:
        shoots.append(PICT_TAG.format(yaw_delta * (shoot), PITCH[i]))

    if num_shoots == 1:
        shoot_plural = "снимок"
    elif num_shoots in [2, 3, 4]:
        shoot_plural = "снимка"
    else:
        shoot_plural = "снимков"

    shoot_info_string = "{0} {1} на {2} градусов c шагом {3}".format(
        num_shoots, shoot_plural, PITCH[i], yaw_delta)
    shoots_info.append(shoot_info_string)

shoots_str = "\n\t\t\t".join(shoots)
shoots_info_string = "\n\t\t\t\t".join(shoots_info)

output = DOC_TEMPLATE.format(_schema=SCHEMA,
                             _preset_name=PRESET_NAME,
                             _tooltip=TOOLTIP.format(shoots_count, shoots_info_string),
                             _shoots=shoots_str)

f = open(FILENAME, "w")
f.write(output)
f.close()