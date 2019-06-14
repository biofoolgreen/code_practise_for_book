'''
@Description: python面向对象编程-chap8-设计模式
@Version: 
@Author: liguoying
@Date: 2019-06-14 18:30:57
'''
##################################
####          模板模式         ####
##################################

# 创建示例数据库
import sqlite3
import datetime
import os
# conn = sqlite3.connect(r"python_object_oriented_programing\chap8_design_pattern\sales.db")

# conn.execute(
#     "CREATE TABLE Sales (salesperson text, "
#     "amt currency, year integer, model text, new boolean)"
# )

# conn.execute(
#     "INSERT INTO Sales values"
#     " ('Tim', 16000, 2010, 'Honda Fit', 'true')"
# )
# conn.execute(
#     "INSERT INTO Sales values"
#     " ('Tim', 9000, 2006, 'Ford Focus', 'false')"
# )
# conn.execute(
#     "INSERT INTO Sales values"
#     " ('Gayle', 8000, 2004, 'Dodge Neon', 'false')"
# )
# conn.execute(
#     "INSERT INTO Sales values"
#     " ('Gayle', 28000, 2009, 'Ford Mustang', 'true')"
# )
# conn.execute(
#     "INSERT INTO Sales values"
#     " ('Gayle', 50000, 2010, 'Lincoln Navigator', 'true')"
# )
# conn.execute(
#     "INSERT INTO Sales values"
#     " ('Don', 20000, 2008, 'Toyota Prius', 'false')"
# )

# conn.commit()
# conn.close()


class QueryTemplate:

    def connect(self):
        self.conn = sqlite3.connect(r"python_object_oriented_programing\chap8_design_pattern\sales.db")
    
    def construct_query(self):
        """子类必须实现该方法"""
        raise NotImplementedError()
    
    def do_query(self):
        results = self.conn.execute(self.query)
        self.results = results.fetchall()
    
    def format_results(self):
        output = []
        for row in self.results:
            row = [str(i) for i in row]
            output.append(", ".join(row))
        self.formatted_results = "\n".join(output)
    
    def output_results(self):
        raise NotImplementedError()
    
    def process_format(self):
        """外部客户端调用的主要方法"""
        self.connect()
        self.construct_query()
        self.do_query()
        self.format_results()
        self.output_results()
    


class NewVehicleQuery(QueryTemplate):
    def construct_query(self):
        self.query = "select * from Sales where new='true'"
    
    def output_results(self):
        print(self.formatted_results)


class UserGrossQuery(QueryTemplate):
    def construct_query(self):
        self.query = "select salesperson, sum(amt) from Sales group by salesperson"
    
    def output_results(self):
        filename = "gross_sales_{0}".format(
            datetime.date.today().strftime("%Y%m%d")
        )
        with open(os.path.join(os.getcwd(), filename), 'w') as f:
            f.write(self.formatted_results)


if __name__ == '__main__':
    nvq = NewVehicleQuery()
    ugq = UserGrossQuery()
    nvq.process_format()
    ugq.process_format()