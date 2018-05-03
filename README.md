# Amocrm Daemon

Производит запись CDR, полученного по AMI в БД для тех случаев, когда хранение в CDR в MySQL напрямую невозможно.

## Установка

```
./bin/contrib/install.centos
cp ./bin/contrib/init.d/amocrm /etc/init.d
```

При запросе пароля нажать ENTER.

Внести настройки в settings.py:
  * AMI_SETTINGS - настройка доступа к AMI
  * MYSQL_SETTINGS - настройки доступа к mysql
  * MYSQL_MAPPING - соответствие полей cdr_manager и БД mysql

```
/etc/init.d/amocrm start
chkconfig amocrm on
```
