from argparse import ArgumentParser
from main import *


def main_func(post_name, page_nums, keywords, tab='main', savepath=os.path.dirname(os.path.realpath(__file__))):
    """
    爬取百度贴吧帖子的主函数
    :param post_name: 贴吧名
    :param page_nums: 爬取的帖子总页数
    :param keywords: 待筛选的关键字，类型为列表
    :param tab: 标签栏目选择，默认为main
    :param savepath: 输出txt文件的保存路径
    :return: 输出多个按关键字命名的TXT文件
    """
    # 循环控制爬取的页数
    keywords = keywords.split('-')
    num = len(keywords)
    for pn in range(int(page_nums)):
        html = get_html(post_name=post_name, tab=tab, pn=pn * 50)
        info = get_post_info(html, pn * 50, keywords)

        # 循环获取每一篇帖子的正文内容
        # 获取每一篇帖子的url
        wb = openpyxl.Workbook()
        for i in range(num):
            res = []
            for each in info[i]:
                content = dict()
                content['content'] = get_content(each)
                content['title'] = each['title']
                content['link'] = each['link']
                res.append(content)
            save2file(wb, res,  keywords[i], ''.join([savepath, '\\post.xlsx']))
            # wb.save(savepath)
        print("当前页面已经保存到本地！")
    print('-------所有帖子下载完成-------')


parser = ArgumentParser()
parser.add_argument('postname', help='贴吧名称')
parser.add_argument('page_num', help='待爬取的总页数')
parser.add_argument('keywords', help='指定关键词，按照 关键词1-关键词2-... 这种格式输入')
parser.add_argument('--tab', help='导航栏标签，默认为main')
parser.add_argument('--savepath', help='输出的txt文件保存路径，精确到文件夹即可。默认为当前文件夹。输出文件按给定的关键字命名。')
args = parser.parse_args()

# python E:\spider\parser.py 王者荣耀 10 交友-排位-处对象
main_func(args.postname, args.page_num, args.keywords)
