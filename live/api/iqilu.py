import logging
from typing import Optional

from live.api.base import BaseChannel
from live.util.http.http import get_json, get_text
from live.util.m3u8 import update_m3u8_content

logger = logging.getLogger(__name__)

CHANNEL_MAPPING = {
  # 济南
  "jncqxw": [171,2], # 长清新闻
  "jncqsh": [171,6], # 长清生活
  "jnjrtv": [303,1], # 济铁电视台
  "jnjyzh": [85,1], # 济阳综合
  "jnjyys": [85,2], # 济阳影视
  "jnlcxw": [261,1], # 历城新闻综合
  "jnpyzh": [257,1], # 平阴综合
  "jnpyxc": [257,3], # 平阴乡村振兴
  "jnshzh": [97,1], # 商河综合
  "jnshys": [97,2], # 商河影视
  "jnzqzh": [195,1], # 章丘综合
  "jnzqgg": [195,2], # 章丘公共
  # 东营
  "dyxwzh": [537,1], # 东营新闻综合
  "dygg": [537,3], # 东营公共
  "dygg2": [29,90], # 东营公共
  "dykj": [537,7], # 东营科教,
  "dydyqxw": [163,5], # 东营区新闻综合
  "dydyqkj": [163,7], # 东营区科教影视
  "dygrzh": [237,1], # 广饶综合
  "dygrkj": [237,5], # 广饶科教文艺
  "dyklxw": [269,3], # 垦利新闻综合
  "dyljzh": [153,1], # 利津综合
  "dyljwh": [153,3], # 利津文化生活
  # 青岛
  "qdhdzh": [227,1], # 黄岛综合
  "qdhdsh": [227,3], # 黄岛生活
  "qdjmzh": [221,2], # 即墨综合
  "qdjmsh": [221,3], # 即墨生活服务
  "qdjzzh": [305,1], # 胶州综合
  "qdjzsh": [305,3], # 胶州生活
  "qdlc": [173,1], # 李沧TV
  "qdls": [295,1], # 崂山TV
  "qdlxzh": [253,1], # 莱西综合
  "qdlxsh": [253,3], # 莱西生活
  "qdpdxw": [45,4], # 平度新闻综合
  "qdpdsh": [45,5], # 平度生活服务
  # 潍坊
  "wfxwzh": [635,1], # 潍坊新闻综合
  "wfsh": [635,5], # 潍坊生活
  "wfyswy": [635,7], # 潍坊影视综艺
  "wfkjwl": [635,9], # 潍坊科教文旅
  "wfgxq": [421,14], # 潍坊高新区
  "wfaqzh": [137,3], # 安丘综合
  "wfaqms": [137,4], # 安丘民生
  "wfbhxw": [199,1], # 滨海新闻综合
  "wfclzh": [1,3], # 昌乐综合
  "wfcyzh": [47,1], # 昌邑综合
  "wfcyjj": [47,2], # 昌邑经济生活
  "wffzxw": [285,1], # 坊子新闻综合
  "wfgmzh": [71,24], # 高密综合
  "wfgmdj": [71,38], # 高密党建农科
  "wfgxq": [421,14], # 潍坊高新区电视
  "wfhtxw": [133,1], # 寒亭新闻
  "wfkwtv": [127,17], # 奎文电视台
  "wflqxw": [205,39], # 临朐新闻综合
  "wfqzzh": [125,2], # 青州综合
  "wfqzwh": [125,3], # 青州文化旅游
  "wfwc": [15,3], # 潍城TV
  "wfzcxw": [115,23], # 诸城新闻综合
  "wfzcsh": [115,25], # 诸城生活娱乐
  # 烟台
  "ytcd": [175,1], # 长岛TV
  "ytfszh": [189,4], # 福山综合
  "ytfssh": [189,5], # 福山生活(无信号)
  "ythyzh": [255,1], # 海阳综合
  "ytlkzh": [57,1], # 龙口综合
  "ytlksh": [57,2], # 龙口生活
  "ytlszh": [245,4], # 莱山综合
  "ytlsys": [245,6], # 莱山影视
  "ytlyzh": [241,4], # 莱阳综合
  "ytlyms": [241,7], # 莱阳民生综艺
  "ytlzzh": [239,1], # 莱州综合
  "ytmpzh": [281,1], # 牟平综合
  "ytplzh": [109,1], # 蓬莱综合
  "ytplzy": [109,2], # 蓬莱综艺
  "ytqxzh": [165,12], # 栖霞综合
  "ytqxpg": [165,14], # 栖霞苹果
  "ytzyzh": [55,2], # 招远综合
  "ytzyzy": [55,4], # 招远综艺
  # 淄博
  "zbbsxw": [17,8], # 博山新闻
  "zbbstw": [17,9], # 博山图文
  "zbgqzh": [61,1], # 高青综合
  "zbgqys": [61,2], # 高青影视
  "zbht1": [23,15], # 桓台综合
  "zbht2": [23,16], # 桓台影视
  "zblzxw": [151,6], # 临淄新闻综合
  "zblzsh": [151,7], # 临淄生活服务
  "zbyyzh": [203,6], # 沂源综合
  "zbyysh": [203,7], # 沂源生活
  "zbzcxw": [75,1], # 淄川新闻
  "zbzcsh": [75,2], # 淄川生活
  "zbzd1": [101,1], # 张店综合
  "zbzd2": [101,6], # 张店2
  "zbzctv1": [259,1], # 周村新闻
  "zbzctv2": [259,3], # 周村生活
  # 枣庄
  "zzstzh": [243,1], # 山亭综合
  "zzszzh": [233,1], # 枣庄市中综合
  "zztezxw": [185,2], # 台儿庄新闻综合
  "zztzzh": [103,2], # 滕州综合
  "zztzms": [103,3], # 滕州民生
  "zzxcxw": [37,8], # 薛城新闻综合
  "zzyczh": [209,1], # 峄城综合
  # 滨州
  "bzbctv": [249,35], # 滨城TV
  "bzbxzh": [207,3], # 博兴综合
  "bzbxsh": [207,4], # 博兴生活
  "bzhmzh": [211,2], # 惠民综合
  "bzhmys": [211,3], # 惠民影视
  "bzwdzh": [169,1], # 无棣综合
  "bzwdzy": [169,21], # 无棣综艺
  "bzyxxw": [217,1], # 阳信新闻综合
  "bzzhzh": [277,1], # 沾化综合
  "bzzhzy": [277,9], # 沾化综艺
  "bzzpzh": [11,15], # 邹平综合
  "bzzpms": [11,16], # 邹平民生
  # 德州
  "dzxwzh": [179,1], # 德州新闻综合
  "dzjjsh": [179,2], # 德州经济生活
  "dztw": [179,9], # 德州图文
  "dzlczh": [215,6], # 陵城综合
  "dzllxw": [267,1], # 乐陵新闻综合
  "dzllcs": [267,5], # 乐陵城市生活
  "dzly1": [49,3], # 临邑1
  "dzly2": [49,4], # 临邑2
  "dznjzh": [193,1], # 宁津综合
  "dzpyzh": [19,2], # 平原综合
  "dzqhzh": [251,8], # 齐河综合
  "dzqyzh": [5,9], # 庆云综合
  "dzqysh": [5,7], # 庆云生活
  "dzwczh": [33,4], # 武城综合
  "dzwczy": [33,6], # 武城综艺影视
  "dzxjzh": [223,1], # 夏津综合
  "dzxjgg": [223,2], # 夏津公共
  "dzyczh": [235,1], # 禹城综合
  "dzyczy": [235,3], # 禹城综艺
  # 菏泽
  "hzcwzh": [131,1], # 成武综合
  "hzcwzy": [131,2], # 成武综艺
  "hzcxzh": [87,2], # 曹县综合
  "hzdmxw": [111,2], # 东明新闻综合
  "hzdt1": [27,7], # 定陶新闻
  "hzdt2": [27,8], # 定陶综艺
  "hzjczh": [141,186], # 鄄城综合
  "hzjyxw": [139,1], # 巨野新闻
  "hzmdxw": [219,6], # 牡丹区新闻综合
  "hzmdzy": [219,17], # 牡丹区综艺
  "hzsxzh": [155,2], # 单县综合
  "hzycxw": [135,3], # 郓城新闻
  "hzyczy": [135,2], # 郓城综艺
  # 济宁
  "jijiazh": [273,1], # 嘉祥综合
  "jijiash": [273,3], # 嘉祥生活
  "jijxzh": [129,2], # 金乡综合
  "jijxsh": [129,4], # 金乡生活
  "jilszh": [89,1], # 梁山综合
  "jiqfxw": [13,1], # 曲阜新闻综合
  "jircxw": [73,8], # 任城新闻综合
  "jircys": [73,9], # 任城影视娱乐
  "jissxw": [117,5], # 泗水新闻综合
  "jisswh": [117,6], # 泗水文化生活
  "jiws1": [53,4], # 微山综合
  "jiws2": [53,5], # 微山2套
  "jiwszh": [301,1], # 汶上综合
  "jiwssh": [301,3], # 汶上生活
  "jiytxw": [63,5], # 鱼台新闻
  "jiytsh": [63,15], # 鱼台生活
  "jiyzxw": [231,1], # 兖州新闻
  "jiyzsh": [231,3], # 兖州生活
  "jizczh": [181,1], # 邹城综合
  "jizcwh": [181,4], # 邹城文化生活
  # 聊城
  "lccpzh": [31,6], # 茌平综合
  "lccpsh": [31,8], # 茌平生活
  "lcdczh": [265,1], # 东昌综合
  "lcdezh": [95,22], # 东阿综合
  "lcdezy": [95,29], # 东阿综艺
  "lcgtzh": [43,1], # 高唐综合
  "lcgtzy": [43,5], # 高唐综艺
  "lcgxzh": [79,1], # 冠县综合
  "lclqzh": [65,2], # 临清综合
  "lclqjj": [65,5], # 临清经济信息
  "lcsxzh": [183,1], # 莘县综合
  "lcsxsh": [183,5], # 莘县生活
  "lcygzh": [81,1], # 阳谷综合
  "lcygys": [81,10], # 阳谷影视
  # 临沂
  "lyzh": [145,39], # 临沂综合
  "lygg": [145,41], # 临沂公共
  "lynk": [145,43], # 临沂农科
  "lyfxzh": [41,119], # 费县综合
  "lyfxsh": [41,117], # 费县生活
  "lyhdys": [191,1], # 河东影视
  "lyhdzh": [191,2], # 河东综合
  "lyjnzh": [105,4], # 莒南综合
  "lyjnys": [105,5], # 莒南影视
  "lyllzh": [113,1], # 兰陵综合
  "lyllgg": [113,2], # 兰陵公共
  "lylszh": [201,1], # 兰山综合
  "lyls1": [167,3], # 临沭综合
  "lyls2": [167,4], # 临沭生活
  "lylzzh": [147,1], # 罗庄综合
  "lylzys": [147,17], # 罗庄影视
  "lymy1": [161,13], # 蒙阴综合
  "lymy2": [161,15], # 蒙阴2套
  "lypyzh": [345,4], # 平邑综合
  "lypysh": [345,14], # 平邑生活
  "lytc1": [83,1], # 郯城综合
  "lytc2": [83,2], # 郯城2套
  "lyynzh": [177,6], # 沂南综合
  "lyynys": [177,7], # 沂南红色影视
  "lyys1": [145,1], # 沂水综合
  "lyys2": [145,2], # 沂水生活
  # 日照
  "rzjx1": [159,23], # 莒县综合
  "rzjx2": [159,27], # 莒县2套
  "rzls": [289,1], # 岚山TV
  "rzwlzh": [299,10], # 五莲综合
  "rzwlwh": [299,12], # 五莲文化旅游
  # 泰安
  "tadpzh": [187,9], # 东平综合
  "tadpms": [187,11], # 东平民生
  "tady": [293,1], # 岱岳TV
  "tafczh": [51,3], # 肥城综合
  "tafcsh": [51,6], # 肥城生活
  "tany1": [123,1], # 宁阳综合
  "tany2": [123,7], # 宁阳2套
  "tats": [263,1], # 泰山TV
  "taxtzh": [59,2], # 新泰综合
  "taxtxc": [59,3], # 新泰乡村
  # 威海
  "whxwzh": [157,1], # 威海新闻综合
  "whdssh": [157,3], # 威海都市生活
  "whhy": [157,12], # 威海海洋
  "whhczh": [213,5], # 威海环翠综合
  "whrczh": [77,10], # 荣成综合
  "whrcsh": [77,11], # 荣成生活
  "whrszh": [143,8], # 乳山综合
  "whrssh": [143,9], # 乳山生活
  "whwd1": [91,7], # 文登TV1
  "whwd2": [91,8], # 文登TV2
}


class IQiLu(BaseChannel):

    headers = {"Referer": "https://v.iqilu.com/"}

    async def get_play_url(self, video_id: str) -> Optional[str]:
        if video_id not in CHANNEL_MAPPING:
            logger.error(f"Invalid Video ID: {video_id}")
            return None

        org_id, channel_id = CHANNEL_MAPPING[video_id]

        params = {
            'orgid': org_id
        }

        json_data = await get_json("https://app.iqilu.com/v1/app/play/tv/live", params=params)
        data = json_data.get('data', [])
        print(data)
        for item in data:
            print(item)
            if channel_id == item['id']:
               stream = item['stream']
               text = await get_text(stream, headers=self.headers)
               lines = text.splitlines()
               for line in lines:
                  if not line.startswith("#") and "m3u8" in line:

                      m3u8_content = await get_text(line, headers=self.headers)

                      modified_m3u8_content = update_m3u8_content(line, m3u8_content, True)

                      return modified_m3u8_content


        return None


site = IQiLu()
