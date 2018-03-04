
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_init import Base


class DBInteractor():
    def __init__(self, SQLclass, database='sqlite:///InventoryCategories.db'):
        engine = create_engine(database)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        self.SQLclass = SQLclass
        self.query = self.session.query(self.SQLclass)

    def add(self, **columns):
        entry = self.SQLclass(**columns)
        self.session.add(entry)
        self.session.commit()
        return entry

    def read(self):
        return self.query.all()

    def filter(self, **attribute):
        return self.query.filter_by(**attribute)

    def delete(self, **attribute):
        delete_this = self.filter(**attribute).one()
        self.session.delete(delete_this)
        self.session.commit()

    def update(self, attribute, need_update):
        self.filter(**attribute).update(need_update)
        self.session.commit()

    def flush_all(self):
        for row in self.read():
            self.session.delete(row)

    def printThis(self):
        output = ""
        index = 1
        for row in self.read():
            row_dict = {k: v for k, v in self.iteritems(row.__dict__) if k[0] != '_'}
            output += "Row {}:\n".format(str(index))
            for k, v in self.iteritems(row_dict):
                output += "    {}: {}\n".format(k, v).encode('utf-8')
            index += 1
            output += "\n"
        print(output)

    def flaskThis(self):
        output = ""
        index = 1
        for row in self.read():
            row_dict = {k: v for k, v in self.iteritems(row.__dict__) if k[0] != '_'}
            output += "Row {}:<br>".format(str(index))
            for k, v in self.iteritems(row_dict):
                output += "    {}: {}<br>".format(k, v)
            index += 1
            output += "<br>"
        return output

    @staticmethod
    def iteritems(dct):
        return ((k, dct[k]) for k in dct)


if __name__ == "__main__":
    from database_init import InventoryType, Category
    restDB = DBInteractor(InventoryType)
    menuDB = DBInteractor(Category)
    menuDB.printThis()
    restDB.printThis()
