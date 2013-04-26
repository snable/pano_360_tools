# -*- coding: utf-8 -*-

from math import degrees, atan, ceil


class Shoot():
    def __init__(self, yaw, pitch):
        self.yaw = yaw
        self.pitch = pitch

    def __str__(self):
        return 'yaw="{:3.2f}" pitch="{:3.2f}"'.format(self.yaw, self.pitch)
        #__repr__ = __str__


class FOV():
    @staticmethod
    def calc(size, focal):
        return degrees(2. * atan(size / 2. / focal))

    def __init__(self, fov, overlap):
        self.fov = fov
        self.overlap = overlap

    def effective(self):
        return self.fov * (1. - self.overlap)

    def real(self, anglesRange):
        numShoots = self.numShoots(anglesRange)
        if numShoots <= 1:
            return 0
        return anglesRange / (numShoots - 1)

    def offset(self):
        return self.effective() / 2.

    def numShoots(self, anglesRange, not_continuous=1):
        eff = self.effective()
        if anglesRange < (eff / 2):
            return 1
        return int(ceil(anglesRange / eff)) + not_continuous


class Head():
    def __init__(self, vMax=70., vMin=-40.):
        if vMax < vMin: vMax, vMin = vMin, vMax
        self.vMax = vMax if vMax < 90. else 90.
        self.vMin = vMin if vMin > -90. else -90.


class Lens():
    def __init__(self, focal=18, hSize=23.6, vSize=15.8, crop=None, portrait=True):
        if portrait:
            hSize, vSize = vSize, hSize
        if crop is not None:
            hSize /= crop
            vSize /= crop
        self.hFOV = FOV.calc(hSize, focal)
        self.vFOV = FOV.calc(vSize, focal)
        self.focal = focal
        self.hSize = hSize
        self.vSize = vSize


class Preset():
    def __init__(self, head=Head(), lens=Lens(),
                 vMin=-90., vMax=90.,
                 hOverlap=.25, vOverlap=.25):

        self.hOverlap = hOverlap if hOverlap < 0.8 else 0.8
        self.vOverlap = vOverlap if vOverlap < 0.8 else 0.8

        if vMax < vMin: vMax, vMin = vMin, vMax
        self.vMax = vMax if vMax < 90. else 90.
        self.vMin = vMin if vMin > -90. else -90.

        self.head = head
        self.lens = lens

    def Build(self):
        shoots = []

        vFOV = FOV(self.lens.vFOV, self.vOverlap)
        hFOV = FOV(self.lens.hFOV, self.hOverlap)

        vMax = min(self.vMax - vFOV.offset(), self.head.vMax)
        vMin = max(self.vMin + vFOV.offset(), self.head.vMin)
        anglesRange = vMax - vMin

        for v in xrange(vFOV.numShoots(anglesRange)):
            pitch = (-v) * vFOV.real(anglesRange) - vFOV.offset() + self.vMax
            hShoots = xrange(hFOV.numShoots(360., 0))
            for h in hShoots if v % 2 == 0 else reversed(hShoots):
                shoots.append(Shoot(h * hFOV.real(anglesRange), pitch))

        self.shoots = shoots
        return self.shoots

    def WriteToXML(self, filename="preset.xml"):
        import lxml.etree as ET

        root = ET.Element("papywizard")
        preset = ET.SubElement(root, "preset")
        preset.set("name", "My Preset")
        tooltip = ET.SubElement(preset, "tooltip")
        tooltip.text = '''
      {focal}mm on {hSize:3.2f}x{vSize:3.2f}
      Total shoots: {totalShoots}
    '''.format(
            focal=self.lens.focal,
            hSize=self.lens.hSize,
            vSize=self.lens.vSize,
            totalShoots=len(self.shoots))
        shoot = ET.SubElement(preset, "shoot")
        for s in xrange(len(self.shoots)):
            pict = ET.SubElement(shoot, "pict")
            pict.set("yaw", "%3.2f" % self.shoots[s].yaw)
            pict.set("pitch", "%3.2f" % self.shoots[s].pitch)
        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8",
                   xml_declaration=True, pretty_print=True)


def main():
    preset = Preset(Head(70, -40), Lens(18))
    preset.Build()
    preset.WriteToXML("my_preset.xml")


if __name__ == "__main__":
    main()