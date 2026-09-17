База вынесена в отдельный контейнер (пока)
для ее поднятия на Linux(как на остальных системах поднимать хз): 
~~~bash
    sudo docker-compose up -d --build
~~~
для старта самого приложения:
~~~bash
    uvicorn app.main:app --reload
~~~
Чтобы пересоздать базу данных в Post запросе /db/create_table введите 'drop and create'
