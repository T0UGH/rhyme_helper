import pymysql
import sys


WIDE_GROUP_AMOUNT = 24
GROUP_AMOUNT = 34


def extract_config_line(line):
    return line[line.find("=")+1:-2]


def get_config():
    configs = []
    with open('rhyme_config.cfg', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            configs.append(extract_config_line(line))
    return configs


def print_usage():
    print("Usage: python3 rhyme_helper.py ChineseWords [wide/nowide] [amount]")
    print("Eg: python3 rhyme_helper.py 网 wide 20")


def words2group_id(words, cursor, is_wide=False):
    """
    将终端得到的汉字序列转换为group_id.
    :param words: 汉字序列
    :param cursor: 游标对象用来执行sql语句
    :param is_wide: 是否放宽搜索范围
    :return: group_id
    """
    try:
        group_amount = WIDE_GROUP_AMOUNT if is_wide else GROUP_AMOUNT
        group_id = 0
        for index in range(len(words)):
            sql = "SELECT %s FROM words WHERE word_value = '%s'" % ('wide_group_id' if is_wide else 'group_id', words[index])
            cursor.execute(sql)
            result = cursor.fetchone()
            group_id += result[0] * pow(group_amount, index)
        return group_id
    except Exception as err:
        print(err)
        return None


def find_rhyme_words(group_id, cursor, word_length, is_wide=False, word_amount=None):
    """
    根据group_id搜索所有的同组词
    :param group_id:
    :param cursor: 游标对象用来执行sql语句
    :param word_length: 词的长度
    :param is_wide: 是否放宽搜索范围
    :param word_amount: 最多返回多少个词
    :return: 由同组词组成的list
    """
    append_str = '' if None is word_amount or not word_amount.isdigit() else 'LIMIT 0, %d' % int(word_amount)
    try:
        sql = "SELECT word_value " \
              "FROM words " \
              "WHERE %s = %d AND word_length = %d " \
              "ORDER BY word_frequency %s" % ('wide_group_id' if is_wide else 'group_id', group_id, word_length, append_str)
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except TypeError as terr:
        print("Usage Error:the character not support")
        print_usage()
    except Exception as err:
        print(err)
        return None


def main():
    """
    main函数不多哔哔
    """
    try:
        db_config = get_config()
        db = pymysql.connect(*db_config)
        cursor = db.cursor()
        is_wide = len(sys.argv) >= 3 and 'wide' == sys.argv[2]
        group_id = words2group_id(sys.argv[1], cursor, is_wide=is_wide)
        word_length = len(sys.argv[1])
        word_amount = None if len(sys.argv) < 4 else sys.argv[3]
        results = find_rhyme_words(group_id, cursor, word_length, is_wide=is_wide, word_amount=word_amount)
        for result in results:
            print(result[0], end=' ')
        print()
        db.close()
    except IndexError as ierr:
        print("Usage Error:not enough param")
        print_usage()


if __name__ == '__main__':
    main()


