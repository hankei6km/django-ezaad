from urllib.parse import urlencode

from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

# from mysite import settings
from django.conf import settings


User = get_user_model()

def login_view(request):
    if str(request.user) != 'AnonymousUser':
        # django で login 状態 なので admin へ.
        return redirect('/admin')

    if 'X-MS-CLIENT-PRINCIPAL-ID' in request.headers:
        # Azaure WebApp で認証されている.
        # django へ login.
        try:
            # Azure AD 側の oid とアプリ側の scim_external_id が一致するユーザーを確認する
            # oid がどこま一意か: https://stackoverflow.com/questions/53346009/is-oid-unique-across-all-tenants-in-aad
            oid = request.headers[ 'X-MS-CLIENT-PRINCIPAL-ID']
            user = User.objects.get(scim_external_id=oid)
            login(request, user, 'django.contrib.auth.backends.ModelBackend')
        except User.DoesNotExist as e:
            # context = {'error': 'User.DoesNotExist', 'error_description': str(e)}
            # return render(request, 'app/auth_error.html', context)
            raise PermissionDenied
        # django へ login できたので admin へ.    
        return redirect('/admin')

    # webapp での認証処理.
    q = {
        'post_login_redirect_url': request.path
    }
    # 必ずこの path になる?
    u = f'/.auth/login/aad?{urlencode(q)}'
    return redirect(u)