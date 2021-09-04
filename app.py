from typing import Optional

import streamlit as st
from sqlmodel import Field, Session, SQLModel, create_engine, select


# class Hero(SQLModel, table=True, extend_existing=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     secret_name: str
#     age: Optional[int] = None

sqlite_file_name = 'database.db'
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    with Session(engine) as session:    
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        session.commit()


def select_heros():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        print('='*60)
        print(heroes)
        print('='*60)



def main():
    st.text('🦄 SQLModel Demo')
    if st.button('Create db'): 
        st.text('hi')
        #create_db_and_tables()
    if st.button('Add heros'): 
        st.text('hi')
        #create_heroes()
    if st.button('Select Heroes'):
        st.text('hi')
        #select_heros()


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
