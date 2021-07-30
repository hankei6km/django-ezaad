# EzAAD

Django へ Azure App Service + SCIM2 でログインする.

## Quick start

### Django 側の設定

1. 以下のように設定を追加する

```python
    INSTALLED_APPS = [
        ...
        'oauth2_provider',
        'django_scim',
        'ezaad',
    ]
    MIDDLEWARE = [
        ...
        'oauth2_provider.middleware.OAuth2TokenMiddleware',
        'ezaad.middleware.SCIMAuthCheckMiddleware',
    ]
    AUTHENTICATION_BACKENDS = [
        # Django default backend
        'django.contrib.auth.backends.ModelBackend',
        # used for SCIM integration
        'oauth2_provider.backends.OAuth2Backend',
    ]
    AUTH_USER_MODEL = 'ezaad.User'
    SCIM_SERVICE_PROVIDER = {
        'USER_ADAPTER': 'ezaad.adapters.SCIMUser',
        'NETLOC': 'localhost',
        'AUTHENTICATION_SCHEMES': [
            {
                'type': 'oauth2',
                'name': 'OAuth 2',
                'description': 'Oauth 2 implemented with bearer token',
            },
        ],
    }
```

1. プロジェクトの `urls.py` の URLconf へ ezaad 等を含める

```python
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('scim/v2/', include('django_scim.urls', namespace='scim')),
    path('ezaad/', include('ezaad.urls')),
```

1. プロジェクトを Azure App Service へデプロイする

1. デプロイ先へ ssh で接続し `python manage.py migrate` 実行し ezaad のモデルを作成する

1. 併せて `python manage.py createsuperuser` を実行し管理者ユーザーを作成する(できれば SCIM 用のユーザーも作成する)

1. ブラウザーで `https://<youre project>.azurewebsites.net/admin/` を開き作成したユーザーでログインする

1. `https://<youre project>.azurewebsites.net/o/applications/` を開き以下のようにアプリケーションを登録する
    - Name: 任意
    - Client Type: Confidential
    - Authorization grant type: Resource owner password-base

1. 登録したアプリケーションの Client Id 等から以下のコマンドで Access Token を取得する(取得後は admin 画面からも確認可能)

```
curl -X POST -d "grant_type=password&username=<username>&password=<password>" -u"<Client id>:<client secret>" https://<youre project>.azurewebsites.net/admin/o/token/
```

### Azure 側での設定

1. Azure protal で Active Director / エンタープライズアプリケーションを開き、新しいアプリケーションの「ギャラリーに見つからないその他のアプリケーションを統合します (ギャラリー以外)」を選択

1. 認証パネルの認証の設定で「認証されていないアクセスを許可する」を選択(SCIM 用の接続を許可するため) 

1. ユーザーとグループパネルから同期させたいユーザーを追加

1. プロビジョニングパネルから作業を開始し、以下のように設定する
  - プロビジョニングモード: 自動
  - テナントの URL:  `https://<youre project>.azurewebsites.net/scim/v2/` 
  - シークレットトークン: 先の手順で取得した Access Token

1. 上記の設定完了後にプロビジョニングパネルを開き属性マッピングの編集を選択、Provision Azure Active Directory Users の属性マッピングを以下のように変更
  - customappsso 属性が externalId の項目の Azure Active Directory 属性を `objectId` へ変更

1. ジョブが完了したらブラウザーで `https://<youre project>.azurewebsites.net/admin/` を開き EZAAD の User を確認する

1. ユーザーが同期されていたらユーザーへ Stuff stats を許可する(その他の許可も必要であれば追加する)

1. ブラウザーで `https://<youre project>.azurewebsites.net/ezaad/login/` を開き同期させたユーザーでサインする


### その他

以下を参考に、refresh token を削除するジョブを設定する必要があります。

- [Management commands — Django OAuth Toolkit 1.5.0 documentation # cleartokens](https://django-oauth-toolkit.readthedocs.io/en/latest/management_commands.html#cleartokens)

## 制限

- マルチテナントでのテストは行っていない
- グループの同期はサポートしていない
- Access Token は手動で設定する必要がある(ギャラリーアプリにすれば解決できるらしいが未検証: https://feedback.azure.com/forums/169401-azure-active-directory/suggestions/31744375-scim-defects)

## License

[15five / django-scim2](https://github.com/15five/django-scim2) の [demo](https://github.com/15five/django-scim2/tree/master/demo) を元に作成.

Copyright (c) 2021 hankei6km

Licensed under the MIT License. See LICENSE in the project root.
