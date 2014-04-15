# -*- coding: utf-8 -*-

import unittest


class TestAgent(unittest.TestCase):

    def test_agent(self):
        FP = [
            "P505i DoCoMo/1.0/P505i/c20/TB/W20H10",
            "J-PHONE/3.0/J-SH09_a",
            "KDDI-HI31 UP.Browser/6.2.0.5 (GUI) MMP/2.0",
        ]
        from ua.agents import agent
        for a in FP:
            ag = agent(a)
            print ag.__class__,
            self.assertTrue(ag.COOKIELESS)

        print

        SP = [
            "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25",
            "Mozilla/5.0 (iPod; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3",
            "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; FujitsuToshibaMobileCommun; IS12T; KDDI)",
        ]
        for a in SP:
            ag = agent(a)
            print ag.__class__,
            self.assertFalse(ag.COOKIELESS)
        print

        PC = [
            "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT)",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:9.0.1) Gecko/20100101 Firefox/9.0.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) AppleWebKit/536.25 (KHTML, like Gecko) Version/6.0 Safari/536.25",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; ja) Presto/2.10.289 Version/12.00",
            "Mozilla/5.0 (compatible; Konqueror/3.3; Linux) (KHTML, like Gecko)",
        ]
        for a in PC:
            ag = agent(a)
            print ag.__class__,
            self.assertFalse(ag.COOKIELESS)
        print

        OT = [
            "Mozilla/5.0 (PLAYSTATION 3; 1.00)",
            "Mozilla/4.0 (PSP PlayStation Portable); 2.00)",
        ]
        for a in OT:
            ag = agent(a)
            print ag.__class__,
            self.assertFalse(ag.COOKIELESS)
        print

if __name__ == '__main__':
    unittest.main()
