- DB: PostgreSQL-mlflow: surkov/32+J45tf1b3C97Xvy
- S3
  - account: mlflow_account
    - Access Key ID: 4pkcZCweajoJijr2ZxAjec
    - Secret Key: 5YqnuFqvMEBN1dp3rmpCTF6ovzp1GEVUMuyw9nssHeHP
- Launch MLflow
  - /etc/environment
    - первый вариант на машине с conda
      ```text
        MLFLOW_S3_ENDPOINT_URL=https://hb.bizmrg.com
        MLFLOW_TRACKING_URI=http://10.0.0.129:8000
      ```
    - второй вариант на машине без conda
      ```text
        MLFLOW_S3_ENDPOINT_URL=https://hb.bizmrg.com
        MLFLOW_TRACKING_URI=http://10.0.0.73:8000
      ```
  - ~/.aws/credentials
    ```text
    [default]
    aws_access_key_id = 4pkcZCweajoJijr2ZxAjec
    aws_secret_access_key = 5YqnuFqvMEBN1dp3rmpCTF6ovzp1GEVUMuyw9nssHeHP
    ```
  - Запуск mlflow
    Строка шаблон:
    ```text
    mlflow server --backend-store-uri postgresql://pg_user:pg_password@REPLACE_WITH_INTERNAL_IP_POSTGRESQL/db_name --default-artifact-root s3://REPLACE_WITH_YOUR_BUCKET/REPLACE_WITH_YOUR_DIRECTORY/ -h 0.0.0.0 -p 8000
    ```
    Строка после изменения
    ```text
    mlflow server --backend-store-uri postgresql://surkov:32+J45tf1b3C97Xvy@10.0.0.249/PostgreSQL-mlflow --default-artifact-root s3://mlflow_bucket_123/mlflow_dir/ -h 0.0.0.0 -p 8000
    ```
    
    !!! Чтобы был доступ к mlflof надо добавить в Настройки firewall правило: Все протоколы + Свой IP
- sudo nano /etc/systemd/system/mlflow-tracking.service
  ```text
  [Unit]
  Description=MLflow Tracking Server
  After=network.target
  [Service]
  Environment=MLFLOW_S3_ENDPOINT_URL=https://hb.bizmrg.com
  Restart=on-failure
  RestartSec=30
  StandardOutput=file:/home/ubuntu/mlflow_logs/stdout.log
  StandardError=file:/home/ubuntu/mlflow_errors/stderr.log
  User=ubuntu
  ExecStart=/bin/bash -c 'PATH=/user/bin/python3/:$PATH exec mlflow server --backend-store-uri postgresql://surkov:32+J45tf1b3C97Xvy@10.0.0.249/PostgreSQL-mlflow --default-artifact-root s3://mlflow_bucket_123/mlflow_dir/ -h 0.0.0.0 -p 8000' 
  [Install]
  WantedBy=multi-user.target
  ```
  !!! Eсли будет ошибка о том, что не найден mlflow, то надо проверить(which python3) куда устоновлен python3 и указать его в переменную PATH(ExecStart)
      + установить mlflow через sudo
- https://tljh.jupyter.org/en/latest/install/custom-server.html
