select * from user
into outfile local 'userData.txt';

show variables like '%max_allowed_packet%';

show variables like '%secure%';

	create view summary as select user.name, user.address, school from user, edu_experience e1 where user.email = e1.email  and school = (select e2.school from edu_experience e2 where e1.email = e2.email order by start_date desc limit 1);


CREATE INDEX usrname ON user(name); 

DELIMITER $$
CREATE TRIGGER after_delete_journal after delete ON journal FOR EACH ROW 
BEGIN 
    delete from comment
    where to_email = OLD.email and to_time = OLD.publish_time;
END
$$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER after_delete_user after delete ON user FOR EACH ROW 
BEGIN 
    delete from work_experience
    where email = OLD.email;
END
$$
DELIMITER ;

create trigger triggerdelete after delete
on user
as
delete from edu_experience
where email in
(select email from deleted)



select e1.school
from edu_experience e1, edu_experience e2
where e1.start_date > e2.start_date and e1.email = e2.email

select school
from edu_experience
order by start_date desc
limit 1;

insert into friend
(usr_email, fri_email, group_name)
values
('', '', '默认分组')

insert into comment
(replyer_email, )
values
()

select * 
from friend
where usr_email = %s and group_name = %s;

update friend set group_name = %s where usr_email = %s and fri_email in (select fri_email from (select fri_email from friend where usr_email = %s and group_name = %s)as T);

select * from friend
where usr_email = %s;

select user.name, title, content from journal, user where journal.email in ( select fri_email from friend where usr_email = %s) and user.email = journal.email;

update journal set body = "" where email = %s and publish_time = %s

update journal set content = "
五散人已经被我打退了，哈哈哈哈哈 


————————————————————来自 杨逍 的评论———————————————————— 
恶贼，你休想！ 
2019-04-11 23:53:25

" where email = "chengkun@163.com" and publish_time = "2019-04-11 10:56:08"

成昆
via (chengkun@163.com)
————————————————————<明教迟早完蛋！>————————————————————
五散人已经被我打退了，哈哈哈哈哈 


————————————————————来自 杨逍 的评论———————————————————— 恶贼，你休想！ 2019-04-11 23:53:25


发布于*2019-04-11 10:56:08

-- insert into journal
-- (email, title, content, publish_time)
-- values
-- ("2", "一起看电影啊", "听说妇联4出了，下午星河影院有没有走起的！！",'2018-11-04 12:23:00');

-- insert into journal
-- (email, title, content, publish_time)
-- values
-- ("2", "美队是不是要领便当了啊", "如题。。。。",'2018-12-04 12:23:01');

-- insert into journal
-- (email, title, content, publish_time)
-- values
-- ("2", "testing...", "文娱部员",'2018-12-04 12:23:10');

-- insert into journal
-- (email, title, content, publish_time)
-- values
-- ("2", "Three-body so cool!", "anyone saw the latest movie?",'2018-12-04 12:24:00');


-- insert into user
-- (name, gender, birth, email, address, passwd)
-- values 
-- ("张无忌", "m", "1997-9-20", "abc@gmail.com", "冰火岛", "123");

-- insert into work_experience
-- (email, workplace, start_date, end_date)
-- values
-- ("2", "Google", "2020-07-01", "2020-09-30"),
-- ("2", "Facebook", "2017-03-01", "2019-03-01");

update user set portrait = "/Users/mohaitao/Desktop/pics/pic9.jpg" where user = "2"

