
# 開発時
![image](https://user-images.githubusercontent.com/1237574/188300248-c1d95f68-dcd5-4e10-b476-047236ba4cf2.png)

# Google Cloud Logging連携時

■一覧
![image](https://user-images.githubusercontent.com/1237574/188300079-bab844bb-82e3-41ae-bcc1-5e400fc4b7d1.png)

■絞り込み
![image](https://user-images.githubusercontent.com/1237574/188300124-9cc5be04-678a-4a54-afe9-a23efb33534d.png)

■正常系（メッセージのみ）
![image](https://user-images.githubusercontent.com/1237574/188300112-ab23b521-63e0-430a-8ba5-63077a8be592.png)

■カスタムフィールド
![image](https://user-images.githubusercontent.com/1237574/188300136-c6bbcad9-ac5c-4847-b7f7-2e5115e7be97.png)

■スタックトレース
![image](https://user-images.githubusercontent.com/1237574/188300040-32b25adb-bc7b-4e6d-853d-abf0a81cc434.png)


```
{
  "insertId": "mr67gffznk9ev",
  "jsonPayload": {
    "message": "critical message"
  },
  "resource": {
    "type": "global",
    "labels": {
      "project_id": "loggersample"
    }
  },
  "timestamp": "2022-09-07T00:11:51.726848Z",
  "severity": "CRITICAL",
  "labels": {
    "python_logger": "develop.__main__"
  },
  "logName": "projects/loggersample/logs/python",
  "sourceLocation": {
    "file": "/home/user/repo/python_logger_core_sample/sample/cs_loggger.py",
    "line": "15",
    "function": "<module>"
  },
  "receiveTimestamp": "2022-09-07T00:11:52.009030332Z"
}
```

#シンク設定

GCSへログをルーティング

※以下はTerraformにて管理すること

## ルール
```
logName=~".*\/application"
```

![image](https://user-images.githubusercontent.com/1237574/189511879-4468f79f-62c8-40e6-ad69-e020a09f93bc.png)


## GCSへの表示

yyyy/MM/dd/*.json
![image](https://user-images.githubusercontent.com/1237574/189513602-70b7eb3e-e5bf-4a1a-9af7-8ccaae2af911.png)


# アラート設定

※以下はTerraformにて管理すること

設定

## ルール
```
logName=~".*\/application" AND
(severity="ERROR" OR severity="CRITICAL")```
```

![image](https://user-images.githubusercontent.com/1237574/189512992-40b410ad-0220-47ef-b5e2-59525909df05.png)

## 通知ポリシー

![image](https://user-images.githubusercontent.com/1237574/189513020-05817e6f-840d-4132-ac5e-18c0f46712f4.png)

## 通知設定
![image](https://user-images.githubusercontent.com/1237574/189513531-6da0108c-c5a8-4586-b2fe-07a47ed3bb9a.png)

```
通知：5分（最小値）
クルーズ：30分（最小値）
```

## 通知されたときの内容
![image](https://user-images.githubusercontent.com/1237574/189514027-26dc202e-cc51-40d7-8b74-fb61c7703b82.png)
