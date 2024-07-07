Материал урока - https://lab.karpov.courses/learning/355/module/3435/lesson/30445/85594/401284/
[JupyterHub on Kubernetes](https://github.com/stockblog/jupyterhub_k8s_mcs_slurm_intel)


- установили kubectl
  ```shell
  curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
  chmod +x ./kubectl
  sudo mv ./kubectl /usr/local/bin/kubectl
  ```
  
  Установка более старой версии
  ```shell
  curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.25.10/bin/linux/amd64/kubectl
  
  chmod +x ./kubectl
  sudo mv ./kubectl /usr/local/bin/kubectl
  ```

- Задать пароль в конфигурационном файле
  ```text
  - name: "OS_PASSWORD"
    value: "VK_CLOUD_PASSWORD"
  ```
- Скопировать файл конфигурации на ВМ
  ```shell
  scp /home/u-user/IdeaProjects/education/data_engineer/data_engineer/6_cloud_storage/kubernetes-cluster-5599_kubeconfig.yaml ubuntu@212.111.84.26:~/kubernetes-cluster-5599_kubeconfig.yaml
  ```
- задали KUBECONFIG
  ```shell
  export KUBECONFIG=~/kube_config/kubernetes-cluster-5599_kubeconfig.yaml
  ```
- подключили доступ к API (а заодно двухфакторную аутентификацию). Для этого надо перейти в меню Управление доступами.
  https://cloud.vk.com/docs/base/k8s/connect/kubectl
  https://cloud.vk.com/docs/tools-for-using-services/api/rest-api/enable-api#416-tabpanel-1
- установили keystone-auth (шаг 2 из этой инструкции https://cloud.vk.com/docs/base/k8s/connect/kubectl)
```shell
curl -sSL \
  https://hub.mcs.mail.ru/repository/client-keystone-auth/latest/linux/client-install.sh \
| bash

source "/home/ubuntu/.bashrc"
```
* прописали путь к keystone-auth в PATH (export PATH=$PATH:/home/ubuntu/vk-cloud - у вас путь может быть другим - ПРОВЕРИТЬ)
* перезашли в консоль (после этого нужно снова задать KUBECONFIG) ИЛИ выполнили команду source /home/ubuntu/.bashrc (при установке keystone-auth будет подсказка с этой командой)
* убедились, что ВМ, k8s-кластер и storageclass находятся в одной зоне доступности (MS1 или GZ1)
* удалили Gatekeeper (https://cloud.vk.com/docs/base/k8s/install-tools/gatekeeper#udalenie)
  ```shell
  helm delete gatekeeper --namespace opa-gatekeeper
  
  kubectl delete crd -l gatekeeper.sh/system=yes
  ```

* nano config_basic.yaml. Тут есть пароль для пользователя admin в JupiterHub
  ```yaml
  singleuser:
    defaultUrl: "/lab"
    storage:
      dynamic:
        storageClass: csi-ceph-ssd-me1-retain
    cpu:
      limit: .5
      guarantee: .5
    memory:
      limit: .256
      guarantee: .512
  hub:
    config:
      Authenticator:
        admin_users:
          - admin
        allowed_users:
          - your_another_non_admin_user
  #DummyAuthenticator not for production
      DummyAuthenticator:
        password: insertyourpasswordhereMVeP2VXfr
      JupyterHub:
        authenticator_class: dummy
  ```
- Установить 
  ```shell
  helm upgrade --cleanup-on-fail \
    --install defaultinstall jupyterhub/jupyterhub --insecure-skip-tls-verify \
    --namespace jupyterhub \
    --create-namespace \
    --version=3.3.6 \
    --values config_basic.yaml \
    --timeout 20m0s
  ```



##### Полезные команды
- Информация о кластере
  `kubectl cluster-info`
- Информация о подах в пространстве jupyterhub
  `kubectl get pods -n jupyterhub`
- Статусы сервисов в пространстве jupyterhub
  `kubectl get service -n jupyterhub`
- Информация о поде hub-75d56487fd-qbjt7 из пространства jupyterhub
  `kubectl describe pod hub-75d56487fd-qbjt7 -n jupyterhub`
- Информация о поде(в описании будет список событий-event)
  `kubectl describe pod hub-67d75cf98f-ms77j -n jupyterhub`
- Получение списка storageclass
  `kubectl get storageclass`
- Просмотр логов пода
  `kubectl logs jupyter-admin -n jupyterhub`
- Получение списка событий пространства имен
  `kubectl get event -n jupyterhub`


- Обновление namespace
  - удаляем неймспейс
    `kubectl delete namespaces jupyterhub`
  - отменяем дефолтную неправильную зону
    kubectl patch storageclass csi-ceph-ssd-me1-retain  -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
  - включаем правильную зону
    kubectl patch storageclass csi-ceph-ssd-me1-retain  -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
- kubectl taint nodes <название вашей мастер-ноды> CriticalAddonsOnly:NoSchedule-
  `kubectl taint nodes kubernetes-cluster-5599-master-0 CriticalAddonsOnly:NoSchedule-`
  kubectl taint nodes <название вашей мастер-ноды> dedicated:NoSchedule-
  `kubectl taint nodes kubernetes-cluster-5599-master-0 dedicated:NoSchedule-`

13 января 2024
100257 
