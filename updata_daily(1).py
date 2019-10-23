# coding:UTF-8
from public.common import *
import datetime

class Dailyupdate():
    def __init__(self, time, id_card):
        self.time = time
        self.id_card = id_card
        # 获取年月日
        dt = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        self.year = dt.year
        self.month = dt.month
        self.day = dt.day
        self.mofidy_time = dt + datetime.timedelta(hours=10)
        self.ymdtime = time.split()[0]
        # print(dt.year, dt.month, dt.day, self.mofidy_time, self.ytime)

    def updata_daily_sign(self):
        """
        修改用户上班卡时间
        create_time: 2019-08-25 05:49:49
        :return:
        """

        # 查询customer_center_id
        sql = "SELECT id FROM staff_customer_center WHERE id_card = '{0}' ORDER BY id DESC LIMIT 1".format(
            self.id_card)
        id = condb_staff(sql)[0]['id']
        # print(id)

        # 更新打卡周期表中时间
        sql_upsign = "UPDATE staff_customer_daily_attendance SET create_time = '{0}',update_time='{1}' WHERE customer_center_id = '{2}' ORDER BY id DESC limit 1".format(
            self.time, self.time, id)
        condb_staff(sql_upsign)

        # 更新打卡记录表中上班打卡时间
        sql_uprecord = "UPDATE staff_customer_daily_sign_record SET create_time ='{0}',update_time = '{1}'WHERE attendance_id=\
        (SELECT id FROM staff_customer_daily_attendance WHERE customer_center_id ='{2}' ORDER BY id DESC limit 1)".format(
            self.time, self.time, id)
        condb_staff(sql_uprecord)

    def undata_daily_audit(self):
        """
        修改打卡日期以及日薪申请日期
        :return:
        """
        # 查询attendance_id
        sql = "SELECT id FROM staff_customer_daily_attendance WHERE customer_center_id = (SELECT id FROM staff_customer_center WHERE id_card = '{0}') ORDER BY id DESC LIMIT 1".format(
            self.id_card)
        id = condb_staff(sql)[0]['id']

        # 更新打卡周期表中日期及时间
        sql_updata = "UPDATE staff_customer_daily_attendance SET attendance_day = '{0}',create_time = '{1}',update_time = '{2}' WHERE id = {3}".format(
            self.day, self.time, self.mofidy_time, id)
        condb_staff(sql_updata)

        # 更新打卡记录表中上班打卡时间
        sql_punchIn = "UPDATE staff_customer_daily_sign_record SET create_time = '{0}',update_time = '{1}' WHERE attendance_id = '{2}' and sign_type = 'PUNCH_IN'".format(
            self.time, self.time, id)
        condb_staff(sql_punchIn)

        # 更新打卡记录表中下班打卡时间
        sql_punchOut = "UPDATE staff_customer_daily_sign_record SET create_time = '{0}',update_time = '{1}' WHERE attendance_id = '{2}' and sign_type = 'PUNCH_OUT'".format(
            self.mofidy_time, self.mofidy_time, id)
        condb_staff(sql_punchOut)

        # 更新日薪审核表中申请日期及打卡时间
        sql_audit = "UPDATE dispatch_daily_salary_audit SET apply_date = '{0}',on_work_time ='{1}',off_work_time='{2}' WHERE id_card = '{3}' ORDER BY id DESC LIMIT 1".format(
            self.ymdtime, self.time, self.mofidy_time, self.id_card)
        condb_dispatch(sql_audit)


if __name__ == '__main__':
    # 传入日期和身份证号
    a = Dailyupdate('2019-10-23 05:00:00', '34292119960118002X')

    # 修改用户上班卡时间
    a.updata_daily_sign()

    # 修改打卡日期以及日薪申请日期
    # a.undata_daily_audit()
