import unittest

from crm_creator.parsers.drbd_parser import DrbdConfig
from crm_creator.parsers.virsh_parser import VirshConfig


DRBD_UP = """
  1:orb1-g-dev1  Connected Primary/Secondary UpToDate/UpToDate C r----- *orb1-g-dev1 vda virtio 
  2:orb1-g-cm1   Connected Primary/Secondary UpToDate/UpToDate C r----- *orb1-g-cm1  vda virtio 
  3:orb1-g-ad1   Connected Primary/Secondary UpToDate/UpToDate C r----- *orb1-g-ad1  vda virtio 
  4:orb1-g-igw1  Connected Primary/Secondary UpToDate/UpToDate C r----- *orb1-g-igw1 vda virtio 
  5:orb1-g-igw2  Connected Primary/Secondary UpToDate/UpToDate C r----- 
  6:orb1-g-egw1  Connected Primary/Secondary UpToDate/UpToDate C r----- 
  7:orb1-g-egw2  Connected Primary/Secondary UpToDate/UpToDate C r----- 
"""


DRBD_SYNC = """
  1:msk1-g-dev1  Connected  Primary/Secondary UpToDate/UpToDate     C r----- *msk1-g-dev1 vda virtio 
  2:msk1-g-cm1   Connected  Primary/Secondary UpToDate/UpToDate     C r----- *msk1-g-cm1  vda virtio 
  3:msk1-g-ad1   Connected  Primary/Secondary UpToDate/UpToDate     C r----- *msk1-g-ad1  vda virtio 
  4:msk1-g-igw1  Connected  Primary/Secondary UpToDate/UpToDate     C r----- *msk1-g-igw1 vda virtio 
  5:msk1-g-igw2  SyncSource Primary/Secondary UpToDate/Inconsistent C r----- 
    [===============>....] sync'ed: 84.5% (796/5116)Mfinish: 0:00:12 speed: 66,964 (65,100) K/sec
  6:msk1-g-egw1  SyncSource Primary/Secondary UpToDate/Inconsistent C r----- 
    [==============>.....] sync'ed: 78.9% (1084/5116)Mfinish: 0:00:17 speed: 65,248 (65,576) K/sec
  7:msk1-g-egw2  Connected  Primary/Secondary UpToDate/UpToDate     C r----- 
"""

VIRSH_LIST = """
 Id Name                 State
----------------------------------
 15 msk1-g-igw1          running
 16 msk1-g-ad1           running
 18 msk1-g-dev1          running
 19 msk1-g-cm1           running
"""

class TestDrbdConfig(unittest.TestCase):
    
    def test_parse_up(self):
        config = DrbdConfig(DRBD_UP)
        self.assertTrue(config)
    
    def test_parse_sync(self):
        config = DrbdConfig(DRBD_SYNC)
        self.assertTrue(config)


class TestVirshList(unittest.TestCase):
    
    def test_parse(self):
        config = VirshConfig(VIRSH_LIST)
        self.assertTrue(config)

if __name__ == '__main__':
    unittest.main()