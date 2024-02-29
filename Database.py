import sqlite3



class sqlite3_Database():
    def __init__(self):
        self.conn = sqlite3.connect('mydatabase.db')
        self.cursor = self.conn.cursor()

        # Kullanıcılar tablosunu oluştur
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
                           id INTEGER PRIMARY KEY,
                           PersonalID INTEGER,
                           username TEXT, 
                           email TEXT, 
                           password TEXT
                           )''')

        # Günlük girişler tablosunu oluştur
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS UserStats(
                           PersonalID INTEGER,
                           Today INTEGER,
                           Yesterday INTEGER,
                           ThisMonth INTEGER,
                           ThisYear INTEGER)''')

    def add_user(self, personal_id,username, email, password):
        self.cursor.execute(f"SELECT COUNT(*) FROM Users WHERE PersonalID = {personal_id}")
        count = self.cursor.fetchone()[0]
        if count > 0:
            print("Bu ID'ye sahip bi kullanıcı zaten var!")
            return False
        else:
            print("Görünüşe göre bu yeni bi ID!")
        self.cursor.execute("SELECT COUNT(*) FROM Users WHERE email = ?", (email,))
        count = self.cursor.fetchone()[0]
        if count > 0:
            print("Bu Emaile sahip bi kullanıcı zaten var!")
            return False
        else:
            print("Görünüşe göre bu yeni bi email!")


        self.cursor.execute("INSERT INTO Users (PersonalID,username, email, password) VALUES (?, ?, ?, ?)",
                            (personal_id, username, email, password))
        self.create_user_stats(personal_id, None, None, None, None)
        self.conn.commit()
        return True


    # Günlük girişleri veritabanına ekleme işlemi
    def create_user_stats(self,PersonalID,Today, Yesterday, ThisMonth, ThisYear):
        self.cursor.execute("INSERT INTO UserStats (PersonalID,Today, Yesterday, ThisMonth,ThisYear) VALUES (?, ?, ?, ?, ?)",
                            (PersonalID, Today, Yesterday, ThisMonth, ThisYear))
        self.conn.commit()
    def update_user_stats(self ,PersonalID,Today, Yesterday, ThisMonth, ThisYear):
        self.cursor.execute(f"SELECT COUNT(*) FROM Users WHERE PersonalID = {PersonalID}")
        count = self.cursor.fetchone()[0]
        if count > 0:
            print("Kullanıcı Bulundu!")
        else:
            print("Kullanıcı bulunamadı!")
            return

        self.cursor.execute("UPDATE UserStats SET Today = ?, Yesterday= ?, ThisMonth= ?, ThisYear= ? WHERE PersonalID = ?",
                       (Today, Yesterday, ThisMonth, ThisYear,PersonalID))
        self.conn.commit()


    def update_user_infos(self,store_visits, id):
        self.cursor.execute("UPDATE DailyVisits SET store_visits = ? WHERE id = ?", (store_visits, id))
        self.conn.commit()
    def show_table(self):
        self.cursor.execute("SELECT * FROM UserStats")
        user_stats = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM Users")
        user_informations = self.cursor.fetchall()
        print("User Informations: ", user_informations)
        print("\nUserStats:", user_stats)
    def choose_from_name(self, Name):
        self.cursor.execute("SELECT * FROM Users WHERE username = ?", (Name,))
        user_info = self.cursor.fetchone()
        if user_info:
            print("Kullanıcı Bilgileri:")
            print("ID:", user_info[1])
            print("Kullanıcı Adı:", user_info[2])
            print("E-posta:", user_info[3])
            print("Password:", user_info[4])
            self.cursor.execute("SELECT * FROM UserStats WHERE PersonalID = ?", (user_info[0],))
            user_stats = self.cursor.fetchone()
            if user_stats:
                print("Kullanıcı İstatistikleri:")
                print("ID:", user_info[0])
                print("Bugünkü Müşteri Sayısı:", user_stats[1])
                print("Dünkü Müşteri Sayısı:", user_stats[2])
                print("Bu Ayki Müşteri Sayısı:", user_stats[3])
                print("Bu Yılki Müşteri Sayısı:", user_stats[4])
        else:
            print(Name, "İsimli kullanıcı bulunamadı")
    def choose_from_personalID(self, personalID):
        user_info_dict = {
              "ID": None,
              "Username": None,
              "Email": None,
             "Password": None
        }
        user_stats_dict = {
            "ID": None,
            "Today": None,
            "Yesterday": None,
            "ThisMonth":None,
            "ThisYear": None
        }
        self.cursor.execute("SELECT * FROM Users WHERE PersonalID = ?", (personalID,))
        user_info = self.cursor.fetchone()
        if user_info:
            print("Kullanıcı Bilgileri:")
            user_info_dict["ID"] = user_info[1]
            user_info_dict["Username"] = user_info[2]
            user_info_dict["Email"] = user_info[3]
            user_info_dict["Password"] = user_info[4]
            self.cursor.execute("SELECT * FROM UserStats WHERE PersonalID = ?", (user_info[0],))
            user_stats = self.cursor.fetchone()
            if user_stats:
                print("Kullanıcı İstatistikleri:")
                user_stats_dict["ID"] = user_info[0]
                user_stats_dict["Today"] = user_info[1]
                user_stats_dict["Yesterday"] = user_info[2]
                user_stats_dict["ThisMonth"] = user_info[3]
                user_stats_dict["ThisYear"] = user_info[4]

        return user_info_dict, user_stats_dict

    def check_if_ID_used(self, ID):
        self.cursor.execute("SELECT * FROM Users WHERE PersonalID = ?", (ID,))
        user_info = self.cursor.fetchone()
        if user_info:
            return False
        else:
            return True
    def check_if_username_exist(self, username):
        self.cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        user_info = self.cursor.fetchone()
        if user_info:
            return False
        else:
            return True
    def check_if_email_exist(self, email):
        self.cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
        user_info = self.cursor.fetchone()
        if user_info:
            return False
        else:
            return True





if __name__ == '__main__':
 x = sqlite3_Database()
 x.show_table()
 x.conn.close()
