from typing import Optional
import pandas as pd
import streamlit as st
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}  # required for streamlit refreshing
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


sqlite_file_name = 'database.db'
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)

        session.commit()


def get_db_size():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
    return len(heroes)

def select_heros():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        print('='*60)
        print(heroes)
        print('='*60)
        for hero in heroes:
            st.text(hero)
        st.text(len(heroes))


def show_table():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        st.table(pd.DataFrame([s.dict() for s in heroes[:5]]))



def main():
    st.title('🦄 SQLModel Demo')
    if st.button('Create db'): 
        create_db_and_tables()
    if st.button('Add heros'): 
        create_heroes()
    if st.button('Select Heroes'):
        select_heros()
    st.text(f'Database: {get_db_size()} rows')
    show_table()



if __name__ == '__main__':
    st.set_page_config(
        page_title="SQLModel Demo",
        page_icon="🦄",
        layout="centered",
        initial_sidebar_state="auto")
    main()

    #create_db_and_tables()
    #create_heroes()
    #select_heros()
