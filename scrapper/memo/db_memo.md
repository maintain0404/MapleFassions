### item
- id: id, int, primary key, not null
- name: 이름, varchar, not null
- category: 장비분류, 2byte int, not null
- set: set 외래키
- image: id기반으로 maplestory.io 이용
- tags: 태그들, string[] 
- HSI: 각 점의 H값 총 Counter, json
- colordetail: HSI 추출값, 외부 링크 or array
```sql
id serial primary key not null,
name varchar not null,
category smallint not null,
set_included smallint, foreign key (set_included) references set(id) on delete set null on update cascade,
tags varchar[],
HSI jsonb
description varchar
```

### set
- ID: serial, not null, primary key
- NAME: 세트이름, varchar, not null
- TYPE: 세트분류, smallint
- DESCRIPTION: 부가설명, varchar, 
```sql
id serial not null primary key,
name varchar not null,
type smallint,
description varchar
```



### 나중에 추가될 예정
- shape: 형태분류(페도라, 벙거지, 머리핀 등등)
- stastics
- user

### 색분류 결과
select id, name, category, hsi from item where id in (select id from (select id, count(v) as cnt from (select id, jsonb_object_keys(hsi::jsonb) as v from item) as temp group by id) as temp2 where cnt=1);
색분류 안된 것들 총 51개는 stand1 모션이 없거나 투명템
나중에 따로 태그를 넣어줘야 할 듯

### 짤팁
jsonb 타입은 json.dumps(사전)으로 넣어주면 됨