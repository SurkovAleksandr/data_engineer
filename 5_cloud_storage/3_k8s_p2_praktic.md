#### [Практический курс по запуску Spark в K8S](https://lab.karpov.courses/learning/355/module/3435/lesson/32847/91389/433224/)
- Тот же [конспект на русском](https://habr.com/ru/companies/vk/articles/549052/)

- Мастройка виртуальной машины и кубернейтса зависит от первой практики. Основное это выставление свойства.
  ```shell
  export KUBECONFIG=~/kube_config/kubernetes-cluster-5599_kubeconfig.yaml
  ```
  
  Так же надо удалить taint
  - kubectl taint nodes <название вашей мастер-ноды> CriticalAddonsOnly:NoSchedule-
    `kubectl taint nodes kubernetes-cluster-8578-master-0 CriticalAddonsOnly:NoSchedule-`
    kubectl taint nodes <название вашей мастер-ноды> dedicated:NoSchedule-
    `kubectl taint nodes kubernetes-cluster-8578-master-0 dedicated:NoSchedule-`

- [Видео с инструкцией](https://www.youtube.com/watch?v=23TTLmUnwj0)
- [Инструкция](https://github.com/stockblog/webinar_spark_k8s)


#### Последовательность шагов
- Клонируем репозиторий spark-on-k8s-operator
  Не работает ~~`git clone https://github.com/GoogleCloudPlatform/spark-on-k8s-operator.git`~~
- Устанавливаем spark-operator-chart
  Не работает ~~`helm install my-release spark-on-k8s-operator/charts/spark-operator-chart --namespace spark-operator --create-namespace --set webhook.enable=true --version 1.1.25`~~
- Новый вариант(изменил имя на )
  ```shell
    helm repo add spark-operator https://kubeflow.github.io/spark-operator
    helm repo update
    helm install my-release spark-operator/spark-operator --namespace spark-operator --create-namespace --set webhook.enable=true --version 1.1.25
  ```
- create service account, role and rolebinding for spark(отступы слева делать не надо)
```shell
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: spark-role
rules:
- apiGroups: [""]
  resources: ["*"]
  verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: spark-role-binding
  namespace: default
subjects:
- kind: ServiceAccount
  name: spark
  namespace: default
roleRef:
  kind: Role
  name: spark-role
  apiGroup: rbac.authorization.k8s.io
EOF
```
- запуск расчета числа пи
    ```shell
    # клонируем репозиторий с примерами
    git clone https://github.com/stockblog/webinar_spark_k8s
    
    # применяем один из файлов для запуска приложения - расчет числа пи
    `kubectl apply -f webinar_spark_k8s/yamls_configs/spark-pi.yaml` 
    # удалить задание
    kubectl delete -f webinar_spark_k8s/yamls_configs/spark-pi.yaml    
    # или так
      # поиск приложения
      kubectl get sparkapplications.sparkoperator.k8s.io
      # удаление приложения
      kubectl delete sparkapplications.sparkoperator.k8s.io s3read-write-test-secret-cfgmap
  
    # смотрим список приложений
    kubectl get sparkapplications.sparkoperator.k8s.io
    # описание приложения
    kubectl describe sparkapplications.sparkoperator.k8s.io spark-pi
    # статус подов
    kubectl get pods
    # список событий нэймспэйса - смотрим ошибки
    kubectl get events
    # смотрим состояние нод
    kubectl get nodes
    # смотрим логи запущенного пода
    kubectl logs spark-pi-driver | grep 3.1
    ```

- Запуск собственного приложения, которое читает и записывает файлы в S3
  ```shell
  # склонировать репозиторий. Ранее уже клонировали
  git clone https://github.com/stockblog/webinar_spark_k8s/ webinar_spark_k8s
  
  # создание креденшела для чтения из S3
  #REPLACE S3_ACCESS_KEY AND S3_SECRET_KEY WITH YOUR PARAMETERS из файла 1_cloud_storage.md
  kubectl create secret generic s3-secret --from-literal=S3_ACCESS_KEY='4pkcZCweajoJijr2ZxAjec' --from-literal=S3_SECRET_KEY='5YqnuFqvMEBN1dp3rmpCTF6ovzp1GEVUMuyw9nssHeHP'
  # проверяем
  kubectl get secret
  
  # создать бакеты в меню S3 облачное хранидище(без _ нижнего подчеркивания) - custom-job-spark-in и custom-job-spark-out
  # загружить в бакет custom-job-spark-input файл evo_train_new.csv из https://disk.yandex.ru/d/gn19jm6mVBnwzQ
  
  # Create ConfigMap for accessing data in S3
  #REPLACE S3_PATH AND S3_WRITE_PATH WITH YOUR PARAMETERS
  kubectl create configmap s3path-config --from-literal=S3_PATH='s3a://custom-job-spark-in/evo_train_new.csv' --from-literal=S3_WRITE_PATH='s3a://custom-job-spark-out/write/evo_train_csv/'
  # проверяем
  kubectl get configmap
  
  # Запуск задания
  kubectl apply -f ~/webinar_spark_k8s/yamls_configs/s3read_write_with_secret_cfgmap.yaml
  ```
  
- Подготовка к установе Spark History Server
  ```shell
  #create namespace for History Server
  kubectl create ns spark-history-server
  
  #create secret so History Server could write to S3. То же самой, что и на предыдущем шаге, но привязываем секрет к namespace spark-history-server
  kubectl create secret generic s3-secret --from-literal=S3_ACCESS_KEY='4pkcZCweajoJijr2ZxAjec' --from-literal=S3_SECRET_KEY='5YqnuFqvMEBN1dp3rmpCTF6ovzp1GEVUMuyw9nssHeHP' -n spark-history-server
  
  # Создаем бакет для Spark History Server - spark-history-server-surkov
   
  ```
- Редактируем файл webinar_spark_k8s/yamls_configs/values-hs.yaml
```yaml
s3:
  enableS3: true
  enableIAM: false
  logDirectory: s3a://spark-history-server-surkov/spark-hs
  # accessKeyName is an AWS access key ID. Omit for IAM role-based or provider-based authentication.
  secret: s3-secret
  accessKeyName: S3_ACCESS_KEY
  # secretKey is AWS secret key. Omit for IAM role-based or provider-based authentication.
  secretKeyName: S3_SECRET_KEY
  endpoint: https://hb.bizmrg.com

gcs:
  enableGCS: false
  logDirectory: gs://spark-history-server-surkov/

pvc:
  enablePVC: false

nfs:
  enableExampleNFS: false

service:
  type: LoadBalancer    
 ```

- Установка Spark History Server
  ```shell
  helm repo add stable https://charts.helm.sh/stable
  #Edit values-hs.yaml. You should specify your logDirectory param.
  helm install -f ~/webinar_spark_k8s/yamls_configs/values-hs.yaml my-spark-history-server stable/spark-history-server --namespace spark-history-server
  
  # Проверить что выдался внешнией IP
  kubectl get service -n spark-history-server
  # Логи для пода
  kubectl logs my-spark-history-server-7b59997fcd-n2w52 -n spark-history-server
  
  # Отредактировать файл ~/webinar_spark_k8s/yamls_configs/s3_hs_server_test.yaml
  
  # запустить отредактированное задание
  kubectl apply -f ~/webinar_spark_k8s/yamls_configs/s3_hs_server_test.yaml

  ```

