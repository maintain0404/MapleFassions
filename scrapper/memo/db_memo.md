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
##### 분류 안된 것들
select id, name, category, hsi from item where id in (select id from (select id, count(v) as cnt from (select id, jsonb_object_keys(hsi::jsonb) as v from item) as temp group by id) as temp2 where cnt=1);
색분류 안된 것들 총 51개는 stand1 모션이 없거나 투명템
나중에 따로 태그를 넣어줘야 할 듯
##### 이펙트
무기류, 망토류는 이펙트가 있기 때문에 이펙트 포함, 불포함 두개 만들 필요가 있음
이펙트는 투명도가 있기 때문에 투명도 반영이 필요함
##### 애매한 색깔
색깔이 구분점에서 걸치는 경우 해당 색이 파편화되어서 태깅이 잘 안됨 -> 다중태깅
##### 다중태깅


### 짤팁
jsonb 타입은 json.dumps(사전)으로 넣어주면 됨

최대 컬러 코드(투명 제외 추출) 추출
```sql
select temp1.id, temp1.colorcode, temp3.mcount 
    from (
        select id, (jsonb_each(hsi)::text::ttype).* from item
    ) as temp1 
    inner join (
        select id, max(counts) as mcount 
        from (
            select id, (jsonb_each(hsi)::text::ttype).* 
            from item
        ) as temp2 
        where temp2.colorcode != 0 group by id
    ) as temp3 
    on temp1.id = temp3.id and temp1.counts = temp3.mcount 
order by temp1.id asc;
```
