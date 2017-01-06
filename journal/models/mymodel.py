from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Date,
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    date = Column(Date)
    body = Column(Text)

    def to_json(self):
        """Return string representation of database entries."""
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date.strftime("%M %d, %Y"),
            "body": self.body,
        }

Index('my_index', MyModel.id, unique=True, mysql_length=255)
