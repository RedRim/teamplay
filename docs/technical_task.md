# Техническое задание
## На разработку информационной системы по проведению киберспортивных мероприятий
1)	Общая информация о проекте
Основной целью проекта является разработать информационную систему для проведения мероприятий, связанных с киберспортом и компьютерными играми. Данные мероприятия могут проводится как онлайн, такие как видео трансляции, так и на заранее обговоренном месте, такие как турнир на арене со зрителями. Целевой аудиторией будут как обычные игроки различных компьютерных игр, так и профессиональные геймеры. Также системой будут пользоваться организаторы мероприятий, компании, размещающие свою рекламу на турнирах и персонал, отвечающий за корректное функционирование системы, например, менеджеры и модераторы.
4.	Требования
 -	Работа с БД через сайт должна осуществляться посредством администраторского веб-интерфейса
 -	Все данные сайта должны храниться в структурированном виде под управлением реляционной СУБД
5.	Функциональность
 -	Регистрация и авторизация пользователей. Возможность регистрации через Steam
 -	Возможность сброса, восстановления пароля через почту, указываемой при регистрации (при регистрации не через Steam). Также нужно подтверждение регистрации аккаунта через почту.
 -	Взаимодействие между пользователями должно обеспечиваться следующими возможностями: 
    +	Добавление в друзья через запрос на дружбу. Один пользователь отправляет запрос, другой должен принять запрос в специальном разделе.
    +	Каждый пользователь должен иметь свой профиль, где будут отображаться его подробная информация: его группы, друзья, игры, в которые он играет, мероприятия, в которых он принимал участия.
    +	Возможность создавать группы, в которые можно приглашать других пользователей. Владелец группы может приглашать участников группы на мероприятия или в комнаты с игрой.
    +	Пользователь может приглашать своих друзей в комнату с игрой. Если пользователь является владельцем группы, он может приглашать всех, кто состоит в этой группе.
    +	Каждый пользователь может заходить к другим пользователями в профиль и просматривать доступную информацию
-	Создание мероприятия, на которое можно приглашать друзей или одногруппников. Мероприятие может быть турниром с призовым фондом или без него.
-	Должна быть лента новостей, отображаемая на специально выделенной странице. Пользователь сможет видеть новости, написанные их друзьями или владельцами групп, в которых состоит пользователь.
-	Возможность создание команды из зарегистрированных пользователей для возможности регистрации команды в турнире.
-	Для каждой команды должен быть отдельный профиль, где будет отображаться информация о состоящих в ней игроках, расписании матчей.
-	Для каждого турнира должна быть страница с информацией о месте проведения, участвующих командах, расписании матчей
-	Сделать страницу «Аллея славы» для отображения информации о состоявшихся турниров.
6.	Требования к реализации
-	Сайт должен быть написан на языке программирование Python с применением веб-фреймворка FastAPI.
-	Реляционная СУБД должна быть PostgreSQL
-	Использовать Redis для кеширования данных.




