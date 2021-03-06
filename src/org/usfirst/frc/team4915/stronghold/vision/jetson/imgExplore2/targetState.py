#
# TargetState:
#   encapsulates state associated with our analysis of the
#   state of the targets.
#
# microsoft lifecam hd-3000 specs:
#   720p: 1280/720
#   diagonal fov: 68.5 degress (diagonal)
#
# But with tegra's opencv+python, we can only capture at 640x480
# so we measured the hfov to be 54 degrees. Which would  give us
# a dfov of 67.5 
#       800 = math.sqrt(w*w  + h*h)
#       1.25 =  800 / 640 
#       67.5  = 1.25 * 54

import sys

class TargetState:
    def __init__(self, visTab):
        self.m_visTab = visTab
        self.m_kp = None
        self.m_lastKp = None
        self.m_res =  (640, 480)
        ar = self.m_res[0] / float(self.m_res[1])
        self.m_fov = (54., 54. / ar)  # full angles
        self.m_center = (self.m_res[0]/2, self.m_res[1]/2)
        self.m_visTab.putString("~TYPE~", "Vision")
        self.m_visTab.putInt("TargetsAcquired", 0)

    # a key-point sorter:
    #   We wish to find the most relevant keypoints.
    #   The approach is up for debate:
    #       - currently we'll look at maximum size
    #       - a distance from last good kp might be wise
    # keypoint fields:
    #   Point2f pt
    #   float   size  (diameter)
    #   float   angle (degrees) (-1 means NA)
    #   float   response
    #   int     octave  (pyramid layer)
    #   int     class_id  (as with a cluster_id)
    @staticmethod
    def kpcompare(kp1, kp2):
        if kp1.size > kp2.size:  # sort bigger to front of list
            return -1
        elif kp1.size == kp2.size:
            return 0
        else:
            return 1
    
    def SetFPS(self, fps):
        self.m_visTab.putInt("FPS", fps)

    def NewLines(self, lines):
        return lines

    def NewKeypoints(self, kplist):
        if len(kplist) > 0:
            kplist.sort(self.kpcompare)
            self.m_kp = kplist[0]
            if 0:
                # print out our keypoints for debugging
                for kp in kplist:
                    sys.stdout.write("%d "%kp.size);
                sys.stdout.write("\n")
        else:
            self.m_kp = None
        self.updateVisionTable()
        return kplist

    def updateVisionTable(self):
        kp = self.m_kp
        if not kp:
            self.m_visTab.putInt("TargetsAcquired", 0)
        else:
            theta = self.pixelToAngle(kp.pt)
            self.m_visTab.putInt("TargetsAcquired", 1)
            self.m_visTab.putInt("TargetX", int(.5+theta[0]))
            self.m_visTab.putInt("TargetY", int(.5++theta[1]))
            self.m_visTab.putNumber("TargetSize", int(.5+kp.size))
            self.m_visTab.putNumber("TargetResponse", kp.response)
            self.m_visTab.putInt("TargetClass", kp.class_id)

    def pixelToAngle(self, pt):
        x = self.m_fov[0] * (pt[0] - self.m_center[0]) / self.m_res[0];
        y = self.m_fov[1] * (pt[1] - self.m_center[1]) / self.m_res[1];
        return (x,y)

