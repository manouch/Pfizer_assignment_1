import uuid
from cassandra.cqlengine import columns
from models.base import Base
from datetime import datetime

class Files(Base):
    id = columns.UUID(primary_key=True, default=uuid.uuid4())
    file_name = columns.Text()
    date = columns.Text(default=str(datetime.utcnow()))
    status = columns.Text()

    def get_data(self):
        return {
            "id": str(self.id),
            "file_name": self.file_name,
            "date": str(self.date)
        }

    def __repr__(self):
        return '<all_files %r>' % self.id
