from pymysql import connect as pyconnect
from jieba import analyse, load_userdict, cut

load_userdict("./static/dict_baidu_utf8.txt")
load_userdict("./static/dict_tencent_utf8.txt")
load_userdict("./static/LOL.txt")
stopwords = {}.fromkeys([line.rstrip() for line in open('./static/Stopword.txt', encoding='UTF-8')])

def get_data(index_news):

    db = pyconnect(host='127.0.0.1', port=3306, user='root', password='123', db='2019_database', charset='utf8')

    cursor = db.cursor()
    sql_1 = "SELECT * FROM ID"+ str(index_news) + " where comment != '[]'"
    cursor.execute(sql_1)
    rows = cursor.fetchall()
    db.close()

    k = 0
    comment = []
    for row in rows:
        row = list(row)
        comment.append(row[3])
        k += 1

    # db = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123',db='2019_database',charset='utf8',cursorclass = pymysql.cursors.DictCursor)
    #
    # cursor = db.cursor()
    #
    # sql_1 = "select comment_num from ID" + str(index_news) + " where comment_num=(select max(comment_num) from ID" + str(index_news) + ")"
    #
    # cursor.execute(sql_1)
    #
    # index1 = cursor.fetchall()
    #
    # index = index1[0]['comment_num']

    fo="./static/data_full.dat"
    with open(fo,"w") as f:
        for n in range(1, k):

            result = []

            result_middle = comment[n-1]
            seg = cut(result_middle)

            for i in seg:
                if i.strip() not in stopwords:
                    if i != '':
                        if i != '\t':
                            if i != '\r\n':
                                if i != '\n':
                                    result.append(i)

            for j in result:
                f.write(j)
                f.write(' ')

            f.write('\n')
            n += 1

def keywords(self):
    tfidf = analyse.extract_tags

    fo = "./static/data_keywords.dat"
    with open(fo,"w") as f:
        for line in open("./static/data_full.dat"):
            text = line
            keywords = tfidf(text,
                             allowPOS=('ns', 'nr', 'nt', 'nz', 'nl', 'n', 'vn', 'vd', 'vg', 'v', 'vf', 'a', 'an', 'i'))

            result = []
            for keyword in keywords:
                result.append(keyword)
            for j in result:
                f.write(j)
                f.write(' ')
            f.write('\n')
# if __name__ == '__main__':
#
#
#     get_data(5756404150)
#     print("Done!")






