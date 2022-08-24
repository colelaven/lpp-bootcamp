from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from models import Bug

class BugNotFoundError(Exception):
    pass

class BugService():

    def __init__(self, file):
        self._file = file
    
    @property
    def bugs(self):
        engine = create_engine(f'sqlite:///./{self._file}')
        session = Session(engine)
        stmt = select(Bug)
        bugs = []
        for bug in session.scalars(stmt).all():
            bugs.append(bug.toDict())
        return bugs

    def addBug(self, name):
        engine = create_engine(f'sqlite:///./{self._file}')
        session = Session(engine)
        newBug = Bug(
            name = name,
            isClosed = False,
        )
        session.add(newBug)
        session.commit()
        return newBug.toDict()
    
    def getBug(self, id):
        engine = create_engine(f'sqlite:///./{self._file}')
        session = Session(engine)
        stmt = select(Bug).where(Bug.id == id)
        if not session.scalar(stmt):
            raise BugNotFoundError
        targetBug = session.scalar(stmt)
        return targetBug.toDict()
    
    def updateBug(self, id, newBug):
        engine = create_engine(f'sqlite:///./{self._file}')
        session = Session(engine)
        stmt = select(Bug).where(Bug.id == id)
        if not session.scalar(stmt):
            raise BugNotFoundError

        targetBug = session.scalar(stmt)

        targetBug.name = newBug['name']
        targetBug.isClosed = newBug['isClosed']

        session.commit()
        return targetBug.toDict()
    
    def deleteBug(self, id):
        engine = create_engine(f'sqlite:///./{self._file}')
        session = Session(engine)
        stmt = select(Bug).where(Bug.id == id)
        if not session.scalar(stmt):
            raise BugNotFoundError
        targetBug = session.scalar(stmt)
        session.delete(targetBug)
        session.commit()